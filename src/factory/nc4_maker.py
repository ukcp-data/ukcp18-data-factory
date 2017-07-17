"""

"""

# Standard library imports
from collections import OrderedDict as OD

# Third-party imports
from netCDF4 import Dataset
import numpy as np
import time as mytime
from datetime import datetime, timedelta
from netCDF4 import num2date, date2num


class NetCDF4Maker(object):

    def __init__(self, fpath):
        # Create the dataset
        self.ds = Dataset(fpath, 'w', format='NETCDF4_CLASSIC')
        self.dimensions = []
        self.coord_variables = []
        self.variables = []
        self.global_attrs = OD()
        self.closed = False

    def close(self):
        # Need to close to write to the file
        self.ds.close()
        self.closed = True

    def __del__(self):
        if not self.closed:
            self.close()

    def create_dimensions(self, *dims):
        """
        :dims sequence of length-2 items as (<dim_name>, <dim_length>)
              - one <dim_length> can be None (unlimited).
        :return: list of netCDF4 dimensions
        """
        # Create dimensions
        for dim_name, dim_length in dims:
            print "Creating: {}".format(dim_name)
            self.dimensions.append(self.ds.createDimension(dim_name, dim_length))

        return self.dimensions

    def create_coordinate_variables(self, *coords):
        """
        :dims sequence of length items as
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
        :variable NetCDF Variable object
        :ref_time datetime object
        :data_array monotonic Numpy array
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
                        ref_time=None, attributes=None):
        """
        :var_id variable ID (string)
        :data_array Numpy or Masked Array
        :numpy_dtype Numpy datatype
        :dim_names tuple of strings
        :ref_time reference time if time axis (default: None)
        :attributes list of tuples of (key, value) pairs
        :return: netCDF4 variable
        """
        print "Var id: {}".format(var_id)
        variable = self.ds.createVariable(var_id, numpy_dtype, dim_names)
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
        :attrs list of tuples of (key, value) pairs
        :return: None
        """
        for attr, value in attrs.items():
            setattr(self.ds, attr, value)

