"""
ukcp18_ls2.py
=============

Helper functions for working with UKCP18 Land Strand 2.
"""

# Standard library imports
import os

# Third-party imports
import numpy as np
import numpy.random as npr
import numpy.ma
from numpy.ma.core import MaskedArray

BASEDIR = 'inputs'


def modify_global_60km(variable, date_times, **facets):
    """
    Modify the array provided based on example input data.

    :param variable:
    :param time_step:
    :param facets:
    :return: Tuple of: (new_array, dimensions_list)
    """
    new_array = variable[:]
    dims_list = variable.dimensions
    return new_array, dims_list


