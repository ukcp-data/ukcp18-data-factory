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
ALL_ENSEMBLE_MEMBERS = ['r1i1p{}'.format(i) for i in range(20)]


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
    len_e, len_t, len_y, len_x = array.shape

    # Set variable multipliers
    var_multipliers = {'pr': 1, 'tas': 2.5}
    var_additions = {'pr': 0, 'tas': 270}
    ensemble_multipliers = [(100 + i) / 100. for i in range(-20, 20)]

    print "Build the new array..."
    for t_index in range(len_t):
        print "...setting values for {} out of {} time steps...".format(t_index + 1, len_t)
        data = array[:, t_index]

   ###     print "CHECK:", ensemble_multipliers, ensemble_member
        new_data = (data * var_multipliers[var_id] + var_additions[var_id]) * year_multiplier * ensemble_multipliers[ensemble_member - 1]
        random_array = npr.random(data.shape) / 10. + 1
        result = new_data * random_array
        array[:, t_index] = result

    print
    return array, variable.dimensions


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


def get_ensemble_values(**facets):
    """

    :param facets:
    :return: array of values
    """
    current_ensemble_member = facets['ensemble_member']
    ensemble_array = np.array([ALL_ENSEMBLE_MEMBERS.index(current_ensemble_member)])
    return ensemble_array