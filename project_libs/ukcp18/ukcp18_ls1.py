"""
ukcp18_ls1.py
=============

Helper functions for working with UKCP18 Land Strand 1.
"""

# Standard library imports

# Third-party imports
import numpy as np
import numpy.random as npr


def modify_gridded_5km(array, var_id, time_step):
    """

    :param array:
    :param var_id:
    :param time_step:
    :return:
    """
    resp = array.copy()

    len_t, len_y, len_x = array.shape

    for t in range(len_t):
        eg_data = _read_example_grid(var_id, time_step)

        for y in range(len_y):
            mult = len_y + 0.5
            values = mult * (npr.random(len_x) / 10. + 1) * eg_data[t]
            array[t][y] = values

#???DOES THE MASK REMAIN???
    return resp