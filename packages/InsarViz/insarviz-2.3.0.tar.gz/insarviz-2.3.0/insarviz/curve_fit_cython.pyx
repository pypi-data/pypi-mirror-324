#!/usr/bin/env python3

"""
The model chosen to represent the surface displacements comes from this publication:
Fourteen-Year Acceleration Along the Japan Trench, 10.1029/2020JB021226, page 5

The model has:
-a linear component: xr+v(t-tr), xr the reference position, v the initial velocity, tr the reference time (1997/01/01)

-a seasonal component: s1*sin(2pi(t-tr))+c1*cos(2pi(t-tr))+s2*sin(4pi(t-tr))+c2*sin(4pi(t-tr))

-an earthquake component: sum of mi*H(t-ti),
 mi is the amplitude of transients for each seismic and ti the starting time of the seismic
 H(t-ti) equal to 0 if t<ti and 1 if t>=ti
 for earthquake with post seismic you have to multiply the earthquake component by log(1+(t-ti)/Tr
 Tr is the characteristic time of the post seismic, the default value is 100 days

-a slow deformation component: sum of ds*J(t-ts)
 ds is the amplitude for each slow deformation and ts the starting time of the slow deformation
 J(t-ts) equal to 0 if t<ts, to -1/2*cos(pi*tnorm)+1/2 if ts<=t<=ts+td, to 1 if t>ts+td,
 td is the duration of the slow deformation events, and tnorm=(t-ts)/td

Algorithm:
=========

The purpose of the algorithm is to determine the value of the following parameters: xr, v, s1, c1, s2, c2, mi, ds

Examples:
=========
python curve_fit.py -c 1891:4297 -f "D:/data_insarviz/CNES_DTs_geo_8rlks_cog.tiff" -l -s -e 100 2018/02/16 1 -p
"""

# classical imports
import argparse
import logging
import numpy as np
cimport numpy as np 

from numpy import cos, pi, sin, zeros, log

from pathlib import Path
import sys

from scipy.optimize import curve_fit

import matplotlib.pyplot as plt
from datetime import datetime as dt
import datetime
from cpython.datetime cimport datetime as dt
import time

from insarviz.Loader import Loader
import cython

import multiprocessing
from multiprocessing import Pool
from functools import partial

import rasterio

logger = logging.getLogger(__name__)

ctypedef np.float64_t npfloat
ctypedef np.float32_t npfloat32
ctypedef np.ndarray nparray
	
cython: wraparound=False
cython: boundscheck=False
cython: cdivision=True

cdef class curve_fit_algorithm:
    cdef public str fit_mode
    cdef public tuple reference_time
    cdef public np.float64_t reference_time_float
    cdef public float characteristic_time
    cdef public list duration_time
    cdef public list post_seismic
    cdef public list earthquake_init_time
    cdef public list slow_deformation_init_time
    
    cdef public np.ndarray user_func_time
    cdef public np.ndarray user_func_data
    cdef public np.ndarray user_data_list
    
    cdef object class_loader
    cdef public list date_in_str
    cdef public np.ndarray band
    cdef public np.ndarray time_data
    cdef public np.ndarray date
    cdef public np.ndarray where_nan
    cdef public np.ndarray band_with_nan
    
    cdef public np.ndarray arg
    
    def __init__(self, fit_mode, reference_time=(0,0,0), characteristic_time=100,
                 duration_time=[], post_seismic=[], earthquake_init_time=[], slow_deformation_init_time=[],
                 user_func_time_list=[], user_func_data_list=[]):
        """
            Parameters
            ----------
            fit_mode: str, l for linear, s for seasonal, e for earthquake, j for slow deformation

            reference_time: tuple of int (yyyy,mm,dd), the default value is first_data
            characteristic_time: float, characteristic time of the earthquake in days

            earthquake_init_time: list of tuple of int (yyyy,mm,dd), list of earthquake starting time, for fit mode e
            slow_deformation_init_time: list of tuple of int (yyyy,mm,dd), list of slow deformation starting time, for fit mode j
            post_seismic: list of bool, list of booleans representing whether the earthquake is with a seismic post or not
            duration_time: list of float, duration of the slow deformation in days
            
            user_func_time: list of tuple of int (yyyy,mm,dd)
            user_func_data: list of float
        """

        if reference_time != (0,0,0):
            self.reference_time_float = self.decimal_year(dt(*reference_time))
        else:
            self.reference_time_float = 0
        
        self.reference_time = reference_time

        self.fit_mode = fit_mode

        self.characteristic_time = characteristic_time / 365
        self.duration_time = [e/365 for e in duration_time]
        self.post_seismic = post_seismic

        self.earthquake_init_time = [self.decimal_year(dt(*date)) for date in earthquake_init_time]
        self.slow_deformation_init_time = [self.decimal_year(dt(*date)) for date in slow_deformation_init_time]
        
        self.user_func_time = np.array([self.decimal_year(dt(*date)) for date in user_func_time_list])
        self.user_func_data = np.array(user_func_data_list)
        
        print("This is the cython version of curve_fit")

    def load_date(self, str filename):
        """
            Methode to load the date

            Parameters
            ----------
            filename: str, the name of the data folder

            Returns
            -------
            None
        """
        self.class_loader = Loader()
        self.class_loader.open(filename)
        
        if None in self.class_loader.dataset.descriptions:
           # dates are not available (no metadata/aux file):
           self.date_in_str = [dt.strftime(dt(year=2000, month=1, day=1) + datetime.timedelta(days=d), "%Y%m%d")
                                for d in range(self.class_loader.__len__())]
        else:
            try:
                self.date_in_str = self.class_loader._dates()
            except TypeError:
                self.date_in_str = self.class_loader._dates

        self.date = np.array([(int(d[0:4]), int(d[4:6]), int(d[6:])) for d in self.date_in_str])
        self.time_data = np.array([self.decimal_year(dt(*e)) for e in self.date])

        if self.reference_time == (0,0,0):
            self.reference_time_float = self.time_data[0]

    def load_data_band(self, int xpos, int ypos):
        """
            Methode to load the band data

            Parameters
            ----------
            xpos: int, x position of a point in the data
            ypos: int, y position of a point in the data

            Returns
            -------
            None
        """
        cdef np.ndarray band
        
        band = self.class_loader.load_profile(xpos, ypos)

        self.where_nan = np.logical_not(np.isnan(band))
        
        self.band = band[self.where_nan]
        self.band_with_nan = band

    cpdef float decimal_year(self, dt date):
        """
            Methode to transforme a date in decimal year

            Parameters
            ----------
            date: datetime.datetime object

            Returns
            -------
            float32, date in decimal year
        """

        cdef int year = date.year
        cdef dt start = dt(year=year, month=1, day=1)
        cdef dt end = dt(year=year + 1, month=1, day=1)

        return float(year) + (self.s(date) - self.s(start)) / (self.s(end) - self.s(start))
    
    cdef float s(self, dt dt_date):
        """
            Transforme a datetime.datetime object in float
            
            Parameters
            ----------
            dt_date: datetime.datetime object 
            Returns
            -------
            float, the result of the function
        """
        return time.mktime(dt_date.timetuple())

    cdef npfloat slow_impulse(self, npfloat times, float duration_time, float init_time):
        """
            Parameters
            ----------
            times: float
            duration_time: float, duration of the slow deformation
            init_time: float, the initial time of the slow deformation

            Returns
            -------
            float, the result of the function
        """
        return (-1 / 2 * cos(pi * (times - init_time) / duration_time) + 1 / 2) * \
               (init_time <= times) * (times <= init_time + duration_time) + (times > init_time + duration_time)

    cdef npfloat linear_func(self, npfloat times, npfloat velocity, npfloat reference_position):
        """
            Methode of the linear model

            Parameters
            ----------
            times: float
            velocity, reference_position: float, unknown parameter of the function

            Returns
            -------
            float, the result of the function
        """
        return velocity * (times - self.reference_time_float) + reference_position

    cdef npfloat acceleration_func(self, npfloat times, npfloat acceleration):
        """
            Methode of the linear model

            Parameters
            ----------
            times: float
            acceleration: float, unknown parameter of the function

            Returns
            -------
            float, the result of the function
        """
        return 0.5 * acceleration * (times - self.reference_time_float) ** 2

    cdef npfloat seasonal_func(self, npfloat times, npfloat s1, npfloat c1, npfloat s2, npfloat c2):
        """
            Methode of the seasonal model

            Parameters
            ----------
            times: float
            s1, c1, s2, c2: float, unknown parameter of the function

            Returns
            -------
            float, the result of the function
        """
        return s1 * cos(2. * pi * (times - self.reference_time_float)) \
             + c1 * sin(2. * pi * (times - self.reference_time_float)) \
             + s2 * cos(4. * pi * (times - self.reference_time_float)) \
             + c2 * sin(4. * pi * (times - self.reference_time_float))

    cdef npfloat earthquake_func(self, npfloat times, npfloat transient_amplitude, bint post, npfloat32 init_time):
        """
            Methode of the earthquake model

            Parameters
            ----------
            times: float
            transient_amplitude: float, unknown parameter of the function
            post: bool, presence of a post-earthquake
            init_time, float the init time of the earthquake

            Returns
            -------
            result: float, the result of the function
        """

        if post:
            return transient_amplitude * (times >= init_time) \
                          * log(abs(1 + (times - init_time) / self.characteristic_time))
        else:
            return transient_amplitude * (times >= init_time)

    cdef npfloat slow_deformation_func(self, npfloat times, npfloat amplitude, float duration, float init_time):
        """
            Methode of the slow deformation model

            Parameters
            ----------
            times: float
            amplitude: float, unknown parameter of the function
            duration: float, duration of the deformation
            init_time, float the init time of the deformation

            Returns
            -------
            result: float, the result of the function
        """
        
        return amplitude * self.slow_impulse(times, duration, init_time)
    
    def func(self, np.ndarray[np.float64_t] times, *arg):
        """
            Function of the trajectory model

            Parameters
            ----------
            times: np.array
            arg: tuple of parameters

            Returns
            -------
            result: np.array, the result of the function
        """
        
        cdef np.float64_t velocity
        cdef np.float64_t reference_position
        cdef np.float64_t acceleration
        cdef np.float64_t s1, c1, s2, c2
        cdef np.float64_t user_amplitude

        cdef tuple transient_amplitude_list
        cdef tuple amplitude_list
        
        cdef int i

        cdef np.ndarray[np.float64_t] result = zeros((times.shape[0],))
        
        
        if 'l' in self.fit_mode:
            velocity, reference_position = arg[0:2]

            result += np.vectorize(self.linear_func)(self, times, velocity, reference_position)
        if 'a' in self.fit_mode:
            acceleration = arg[2]

            result += np.vectorize(self.acceleration_func)(self, times, acceleration)
        if 's' in self.fit_mode:
            s1, c1, s2, c2 = arg[3:7]

            result += np.vectorize(self.seasonal_func)(self, times, s1, c1, s2, c2)
        if 'u' in self.fit_mode:
            user_amplitude = arg[7]
            
            #assert len(result)==len(self.user_data_list), "you must to update self.user_data_list " \
                                                      #"to have the same length with time_data_array and result"
                                                      
            result += user_amplitude * self.user_data_list
        if 'e' in self.fit_mode:
            transient_amplitude_list = arg[8:8 + len(self.earthquake_init_time)]

            for i in range(len(self.earthquake_init_time)):
                result += np.vectorize(self.earthquake_func)(self, times, transient_amplitude_list[i], self.post_seismic[i],
                                                             self.earthquake_init_time[i])
        if 'j' in self.fit_mode:
            amplitude_list = arg[8 + len(self.earthquake_init_time):
                                 8 + len(self.earthquake_init_time) + len(self.slow_deformation_init_time)]

            for i in range(len(self.slow_deformation_init_time)):
                result += np.vectorize(self.slow_deformation_func)(self, times, amplitude_list[i], self.duration_time[i],
                                                                   self.slow_deformation_init_time[i])
        
        return result

    def fit(self, np.ndarray[np.float64_t] time_data_array, np.ndarray[np.float32_t] band_data_array, 
            np.ndarray weight, int start_time=0, int end_time=-1):
        """
            Methode to fit curve

            Parameters
            ----------
            time_data_array: ndarray, array of time in decimal year
            band_data_array: ndarray, array of the position of the surface in function of time
            weight: ndarray, array of weight for each data of band_data_array
            start_time: int, index of the first date in time_data_array
            end_time: int, index of the last date in time_data_array

            Returns
            -------
            None
        """
        cdef int number_of_parameters = 8 + len(self.earthquake_init_time) + len(self.slow_deformation_init_time)
        cdef np.ndarray popt
        cdef np.ndarray pcov
        
        cdef list user_data_list = []
        cdef int i
        
        if 'u' in self.fit_mode:
            for i in range(len(self.user_func_time)):
                if self.user_func_time[i] in time_data_array[start_time:end_time]:
                    user_data_list.append(self.user_func_data[i])

        self.user_data_list = np.array(user_data_list)

        if end_time == -1:
            popt, pcov = curve_fit(self.func, time_data_array[start_time:], band_data_array[start_time:],
                               p0=[1.] * number_of_parameters, sigma=weight[start_time:])
        else:
            popt, pcov = curve_fit(self.func, time_data_array[start_time:end_time], band_data_array[start_time:end_time],
                               p0=[1.] * number_of_parameters, sigma=weight[start_time:end_time])

        self.arg = popt

    def plot(self, time_data_array, band_data_array, arg, start_time=0, end_time=-1):
        """
            Methode to plot the fit curve,

            Parameters
            ----------
            time_data_array: array, array of time in decimal year
            band_data_array: array, array of the position of the surface in function of time

            arg: list of float, the different parameters of self.func you can use self.arg
            start_time: int, index of the first date in time_data_array
            end_time: int, index of the last date in time_data_array

            Returns
            -------
            None
        """

        plt.plot(time_data_array, band_data_array, label="data")
        if end_time == -1:
            plt.plot(time_data_array[start_time:], self.func(time_data_array, *arg)[start_time:],
                     label="curve fit")
        else:
            plt.plot(time_data_array[start_time:end_time], self.func(time_data_array, *arg)[start_time:end_time],
                     label="curve fit")

        plt.legend()
        plt.show()


def multi_trend_fit(arg, fit_mode, reference_time=(0,0,0), characteristic_time=100,
                 duration_time=[], post_seismic=[], earthquake_init_time=[], slow_deformation_init_time=[]):

    start_line, start_column, chunk_size, max_col, img_name = arg
    class_curve_fit = curve_fit_algorithm(fit_mode, reference_time, characteristic_time,
                                              duration_time , post_seismic, earthquake_init_time,
                                              slow_deformation_init_time)

    number_of_parameters = 8 + len(earthquake_init_time) + len(slow_deformation_init_time)

    class_curve_fit.load_date(img_name)
    res = np.zeros((chunk_size, max_col - start_column, number_of_parameters))
    for x in range(start_line, start_line + chunk_size):
        # print(f"{multiprocessing.current_process()} processing row  {x}")
        for y in range(start_column, max_col):
            class_curve_fit.load_data_band(x, y)
            if class_curve_fit.band.size == 0:
                res[x-start_line, y-start_column, :] = [0.0] * number_of_parameters
                continue
            class_curve_fit.fit(class_curve_fit.time_data[class_curve_fit.where_nan],
                                class_curve_fit.band,
                                np.ones(len(class_curve_fit.band)))
            res[x-start_line, y-start_column, :] = class_curve_fit.arg
    return res
