"""

"""

# Standard library imports
import os
from collections import OrderedDict as OD

# Third-party imports
from netCDF4 import Dataset
import numpy as np
import time as mytime
from datetime import datetime, timedelta
from netCDF4 import num2date, date2num


class NetCDF4Maker(object):

    def __init__(self, fpath, verbose=False):

        self.verbose = verbose

        # Create the dataset
        self._check_output_dir(fpath)
        self.ds = Dataset(fpath, 'w', format='NETCDF4_CLASSIC')

        self.dimensions = []
        self.coord_variables = []
        self.variables = []

        self.global_attrs = OD()
        self.closed = False

    def _check_output_dir(self, fpath):
        """
        Get the output directory for the file `fpath` and make sure the directory
        exists.

        :param fpath: file path [string]
        :return: None
        """
        output_dir = os.path.dirname(fpath)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    def close(self):
        # Need to close to write to the file
        self.ds.close()
        self.closed = True

    def __del__(self):
        if not self.closed:
            self.close()

    def create_dimensions(self, *dims):
        """
        :param dims: sequence of length-2 items as (<dim_name>, <dim_length>)
              - one <dim_length> can be None (unlimited).
        :return: list of netCDF4 dimensions
        """
        # Create dimensions
        for dim_name, dim_length in dims:
            if self.verbose: print "Creating: {}".format(dim_name)
            self.dimensions.append(self.ds.createDimension(dim_name, dim_length))

        return self.dimensions

    def create_coordinate_variables(self, *coords):
        """
        :param dims: sequence of length items as
                (<var_id>, <data_array>, <numpy_dtype>, <dim_names>)
              with optional additional items:
                (<ref_time>, <attributes_dict>)
              - <data_array> is a Numpy or Masked Array
              - <dim_names> is a tuple of strings.
        :return: list of netCDF4 variables
        """
        # Create coordinate variables
        for var_id, numpy_dtype, dim_names, ref_time, attributes in coords:
            self.coord_variables.append(
                self.create_variable(var_id, data_array, numpy_dtype, dim_names,
                                     ref_time, attributes))

        return self.coord_variables

    def _set_time_values(self, variable, ref_time, data_array):
        """
        :param variable: NetCDF Variable object
        :param ref_time: datetime object
        :param data_array: monotonic Numpy array
        :return: None
        """
        # Fill in times
#        ????
        dates = []
        for n in range(5):
            dates.append(ref_time + n * timedelta(hours=12))

        times[:] = date2num(dates, units=times.units, calendar=times.calendar)

        return None

    def create_variable(self, var_id, data_array, numpy_dtype, dim_names,
                        fill_value=None, ref_time=None, attributes=None):
        """
        :param var_id: variable ID (string)
        :param data_array: Numpy or Masked Array
        :param numpy_dtype: Numpy datatype
        :param dim_names: tuple of strings
        :param fill_value: missing value indicator
        :param ref_time: reference time if time axis (default: None)
        :param attributes: list of tuples of (key, value) pairs
        :return: netCDF4 variable
        """
        if self.verbose: print "Var id: {}".format(var_id)
        
        if var_id == 'meaning_period': numpy_dtype = 'int32'

        variable = self.ds.createVariable(var_id, numpy_dtype, dim_names, fill_value=fill_value)

        # Set the array values on the variable
        variable[:] = data_array

        if ref_time:
            self._set_time_values(times)

        if attributes:
            for attr, value in attributes.items():
                setattr(variable, attr, value)

        self.variables.append(variable)
        return variable

    def create_global_attrs(self, **attrs):
        """
        :param attrs: list of tuples of (key, value) pairs
        :return: None
        """
        for attr, value in attrs.items():
            setattr(self.ds, attr, value)

