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
    Loads a coordinate variable from the source data and returns it.

    :param prob_data_type:
    :return:
    """
    fpath = "{}/source_others/a1b_tas_jja_EAW_1961-1990.dat".format(BASEDIR)

    with open(fpath, 'rb') as reader:
        data = cPickle.load(reader)

    key = prob_data_map[prob_data_type]
    if key == 'prob':
        return np.array((data[key] * 100), np.float)
    else:
        return np.array(data[key], np.int32)


def load_samples():
    """
    Load the values of the 'sample' coordinate variable.

    :return: numpy array
    """
    return load_coord_var('sample')[:]


def load_percentiles():
    """
    Load the values of the 'percentile' coordinate variable.

    :return: numpy array
    """
    return load_coord_var('percentile')


def _get_ls1_prob_site_data(var_id, year, scenario="a1b",
                            prob_data_type="sample", ##grid_res="25km",
                            temp_avg_type="mon"):
    """
    Extract and return example probabilistic data and a numpy array.

    :param var_id: variable id [string]
    :param year: year [int]
    :param scenario: scenario [string]
    :param prob_data_type: probability data type [string]
    :param grid_res: grid resolution [string]
    :param temp_avg_type: temporal average type (frequency) [string]
    :return: numpy array.
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

    # Remove "Anom" from var_id - might not be there
    var_id = var_id.replace("Anom", "")

    for temporal_average in ("djf", "jja"):
        fname = "a1b_{var_id}_{temporal_average}_EAW_1961-1990.dat".format(
            scenario=scenario, var_id=var_id, temporal_average=temporal_average)
        fpath = os.path.join(BASEDIR, "source_others", fname)

        print "Reading data from: {0}".format(fpath)

        with open(fpath, 'rb') as reader:
            data[temporal_average] = cPickle.load(reader)

    if year < 1975: 
        # Set year to start year available in example data
        year = 1975

    year_index = [int(y) for y in data['jja']['time']].index(year)

    prob_data_key = prob_data_map[prob_data_type] + "data"

    prob_data_djf = data['djf'][prob_data_key][:, year_index]
    prob_data_jja = data['jja'][prob_data_key][:, year_index]

    prob_data_over_times = [(prob_data_djf * mult) + (prob_data_jja * (1 - mult)) for mult in mults]
    return np.array(prob_data_over_times)


def modify_ls1_array(variable, date_times, **facets):
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
##    grid_res = facets["resolution"]
    temp_avg_type = facets["frequency"]
    year = date_times[0].year

    eg_data = _get_ls1_prob_site_data(var_id, year, scenario=scenario,
                                          prob_data_type=prob_data_type, ##grid_res=grid_res,
                                          temp_avg_type=temp_avg_type)

    array = variable[:]#.data
    spatial_dims = list(array.shape[1:])

    # Now broadcast the array to new fourth dimension
    len_prob_dim = eg_data.shape[1]
    new_shape = list(array.shape) + [len_prob_dim]

    if isinstance(array, MaskedArray):
        new_array = numpy.ma.resize(array, new_shape)
    else:
        new_array = numpy.resize(array, new_shape)

    dims_list = tuple(list(variable.dimensions) + [prob_data_type])

    print "Building the new array..."
    if 0: # For DEBUGGING
        new_array = np.zeros(new_shape)
        return new_array, dims_list

    for t_index, values in enumerate(eg_data):
        print "...setting values for {} out of {} time steps...".format(t_index + 1, new_shape[0])
        for y_index in range(spatial_dims[0]):
            mult = (spatial_dims[0] + 0.5) / spatial_dims[0]

            # Work out shape of random array to be broadcasted
            # Will either be (len_x, len_prob_dim) or just (len_prob_dim)
            sub_shape = [len_prob_dim]
            if len(spatial_dims) > 1:
                sub_shape = spatial_dims[1:] + sub_shape

            random_array = _get_broadcasted_random_array(sub_shape)
            incremented_values = mult * random_array * values
            new_array[t_index][y_index] = incremented_values
            if not var_id.startswith('tas'):
                values = incremented_values

    print
    return new_array, dims_list


def _get_broadcasted_random_array(shape):
    """
    Broadcast array randomly to new shape.

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
