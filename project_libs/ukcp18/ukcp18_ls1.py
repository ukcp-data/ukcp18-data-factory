"""
ukcp18_ls1.py
=============

Helper functions for working with UKCP18 Land Strand 1.
"""

# Standard library imports
import os

# Third-party imports
import numpy as np
import numpy.random as npr
import numpy.ma
from numpy.ma.core import MaskedArray

import cPickle

BASEDIR = 'inputs'
prob_data_map = {'sample': 'samp',
                 'percentile': 'prob'}

def load_coord_var(prob_data_type):
    """

    :param prob_data_type:
    :return:
    """
    fpath = "{}/a1b_tas_jja_EAW_1961-1990.dat".format(BASEDIR)

    with open(fpath, 'rb') as reader:
        data = cPickle.load(reader)

    key = prob_data_map[prob_data_type]
    return data[key]


def load_samples():
    """

    :return:
    """
    return load_coord_var('sample')


def load_percentiles():
    """

    :return:
    """
    return load_coord_var('percentile')


def _get_ls1_prob_site_data(var_id, year, scenario="a1b",
                            prob_data_type="sample", grid_res="25km",
                            temp_avg_type="mon"):
    """

    :param var_id:
    :param year:
    :param scenario:
    :param prob_data_type:
    :param grid_res:
    :param temp_avg_type:
    :return:
    """
    # Structure the output data based on the temporal average type
    if temp_avg_type == "mon":
        mults = [1, 0.95, 0.8, 0.6, 0.5, 0.3, 0.1, 0, 0.1, 0.3, 0.7, 0.9]
    elif temp_avg_type == "seas":
        mults = [1, 0.5, 0, 0.6]
    elif temp_avg_type == "ann":
        mults = [0.5]
    else:
        raise Exception("Temporal average type must be one of: mon, seas, ann.")

    data = {}

    for temporal_average in ("djf", "jja"):
        fname = "{scenario}_{var_id}_{temporal_average}_EAW_1961-1990.dat".format(
            scenario=scenario, var_id=var_id, temporal_average=temporal_average)
        fpath = os.path.join(BASEDIR, fname)

        print "Reading data from: {0}".format(fpath)

        with open(fpath, 'rb') as reader:
            data[temporal_average] = cPickle.load(reader)

    year_index = [int(y) for y in data['jja']['time']].index(year)

    prob_data_key = prob_data_map[prob_data_type] + "data"

    prob_data_djf = data['djf'][prob_data_key][:, year_index]
    prob_data_jja = data['jja'][prob_data_key][:, year_index]

    prob_data_over_times = [(prob_data_djf * mult) + (prob_data_jja * (1 - mult)) for mult in mults]
    return np.array(prob_data_over_times)


def modify_gridded_5km(variable, date_times, **facets):
    """
    Modify the array provided based on example input data.

    :param variable:
    :param time_step:
    :param facets:
    :return: Tuple of: (new_array, dimensions_list)
    """
    var_id = facets["var_id"]
    scenario = facets["scenario"]
    prob_data_type = facets["prob_data_type"]
    grid_res = facets["grid_res"]
    temp_avg_type = facets["temp_avg_type"]
    year = date_times[0].year

    eg_data = _get_ls1_prob_site_data(var_id, year, scenario=scenario,
                                          prob_data_type=prob_data_type, grid_res=grid_res,
                                          temp_avg_type=temp_avg_type)

    array = variable[:]
    mask = array.mask.copy()
    print mask.shape

    len_t, len_y, len_x = array.shape
#    new_array = array.copy()

    # Now broadcast the array to new fourth dimension
    len_prob_dim = eg_data.shape[1]
    new_shape = list(array.shape) + [len_prob_dim]

    if isinstance(array, MaskedArray):
        new_array = numpy.ma.resize(array, new_shape)
    else:
        new_array = array.resize(new_shape)

    dims_list = tuple(list(variable.dimensions) + [prob_data_type])

    print "Building the new array..."
    if 0:
        new_array = np.zeros(new_shape)
        return new_array, dims_list

    for t_index, values in enumerate(eg_data):
        print "...setting values for {} out of {} time steps...".format(t_index + 1, new_shape[0])
        for y_index in range(len_y):
            mult = (len_y + 0.5) / len_y

            random_array = _get_broadcasted_random_array((len_x, len_prob_dim))
            values = mult * random_array * values
            new_array[t_index][y_index] = values

    print mask.shape
    new_array.mask = mask
    print
    print "MASK", new_array.mask.shape
    return new_array, dims_list


def _get_broadcasted_random_array(shape):
    """

    :param shape:
    :return:
    """
    arr = npr.random(shape) / 10. + 1
    return arr

if __name__ == "__main__":

    import datetime
    print _get_ls1_prob_site_data('tas', datetime.datetime.now(), scenario="a1b",
                            prob_data_type="mon", grid_res="25km",
                            temp_avg_type="mon")