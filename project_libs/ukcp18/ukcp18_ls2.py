"""
ukcp18_ls2.py
=============

Helper functions for working with UKCP18 Land Strand 2.
"""

# Standard library imports
import os
import time

# Third-party imports
import numpy as np
import numpy.random as npr
import numpy.ma
from numpy.ma.core import MaskedArray

BASEDIR = 'inputs'

# Global variables
ALL_ENSEMBLE_MEMBERS = [
      "r001i1p00000",
      "r001i1p00090",
      "r001i1p00605",
      "r001i1p00834",
      "r001i1p01113",
      "r001i1p01554",
      "r001i1p01649",
      "r001i1p01843",
      "r001i1p01935",
      "r001i1p02089",
      "r001i1p02123",
      "r001i1p02242",
      "r001i1p02305",
      "r001i1p02335",
      "r001i1p02491",
      "r001i1p02753",
      "r001i1p02832",
      "r001i1p02868",
      "r001i1p02884",
      "r001i1p02914"
]


def _modify_variable(variable, date_times, **facets):
    """
    Modify the array provided based on example input data.

    :param variable:
    :param time_step:
    :param facets:
    :return: Tuple of: (new_array, dimensions_list)
    """
    var_id = facets["var_id"]
    ensemble_member = ALL_ENSEMBLE_MEMBERS.index(facets["ensemble_member"])
    ref_year = 2010.
    year_multiplier = (date_times[0].year - ref_year) / 100. + 1.

    array = variable[:]
    len_e, len_t = array.shape[:2]
    spatial_shape = list(array.shape[2:])

    required_n_times = len(date_times)
    endless_time_indices = []
    for _ in range(1000): endless_time_indices.extend(range(len_t))

    # Set variable multipliers
    var_multipliers = {'pr': 1, 'tas': 2.5}
    var_additions = {'pr': 0, 'tas': 270}
    ensemble_multipliers = [(100 + i) / 100. for i in range(-20, 20)]

    # Create new array
    new_shape = tuple([len_e, required_n_times] + spatial_shape)

    if isinstance(array, MaskedArray):
        new_array = numpy.ma.resize(array, new_shape)
    else:
        new_array = numpy.resize(array, new_shape)

    #print "Build the new array..."
    for t_index in range(required_n_times):
        #print("...setting values for {} out of {} time steps...".format(t_index + 1, required_n_times))
        in_range_t_index = endless_time_indices[t_index]
        data = array[:, in_range_t_index]

        new_data = (data * var_multipliers[var_id] + var_additions[var_id]) * year_multiplier * \
                   ensemble_multipliers[ensemble_member - 1]
        random_array = npr.random(data.shape) / 10. + 1

        result = new_data * random_array
        new_array[:, t_index] = result

    print
    vd = variable.dimensions
#    dims_list = tuple([vd[0], , vd[2], vd[3]])

    return new_array, vd


def modify_global_60km(variable, date_times, **facets):
    """
    Modify the array provided based on example input data.

    :param variable:
    :param time_step:
    :param facets:
    :return: Tuple of: (new_array, dimensions_list)
    """
    return _modify_variable(variable, date_times, **facets)


def modify_uk_60km(variable, date_times, **facets):
    """
    Modify the array provided based on example input data.

    :param variable:
    :param time_step:
    :param facets:
    :return: Tuple of: (new_array, dimensions_list)
    """
    return _modify_variable(variable, date_times, **facets)


def modify_uk_region(variable, date_times, **facets):
    """
    Modify the array provided based on example input data.

    :param variable:
    :param time_step:
    :param facets:
    :return: Tuple of: (new_array, dimensions_list)
    """
    return _modify_variable(variable, date_times, **facets)


def get_ensemble_values(**facets):
    """

    :param facets:
    :return: array of values
    """
    current_ensemble_member = facets['ensemble_member']
    ensemble_array = np.array([ALL_ENSEMBLE_MEMBERS.index(current_ensemble_member)])
    return ensemble_array
