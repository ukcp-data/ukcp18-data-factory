"""
ukcp18_ls1.py
=============

Helper functions for working with UKCP18 Land Strand 1.
"""

# Standard library imports

# Third-party imports
import numpy as np
import numpy.random as npr

import numpy
import cPickle

BASEDIR = '/data/ukcp18-ls1/ls1-bundle'


def _get_ls1_prob_site_data(var_id, year, scenario="a1b",
                            prob_data_type="sample", grid_res="25km",
                            temp_avg_type="mon"):
    """
    "facets": {
        "__order__": ["project", "dataset", "scenario", "temp_avg"],
        "project": ["ukcp18"],
        "data_group": ["land_probabilistic"],
        "grid_res": ["25km"],
        "scenario": ["a1b", "rcp45", "rcp60", "rcp85"],
        "prob_data_type": ["sample", "percentile"],
        "var_id": ["pr", "tasmax"],
        "temp_avg_type": ["mon"],
        "version": ["v20170331"]
    """
    basedir = BASEDIR

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
        fpath = "{basedir}/{scenario}/{var_id}/{temporal_average}/{scenario}_{var_id}_{temporal_average}_EAW_1961-1990.dat".format(
            basedir=basedir, scenario=scenario, var_id=var_id, temporal_average=temporal_average)

        print "Reading data from: {0}".format(fpath)

        with open(fpath, 'rb') as reader:
            data[temporal_average] = cPickle.load(reader)

    year_index = [int(y) for y in data['jja']['time']].index(year)

    prob_data_map = {'sample': 'sampdata',
                     'percentile': 'probdata'}

    prob_data_key = prob_data_map[prob_data_type]

    prob_index = 100
    prob_data_djf = data['djf'][prob_data_key][prob_index, year_index]
    prob_data_jja = data['jja'][prob_data_key][prob_index, year_index]

    prob_data_over_times = [(prob_data_djf * mult) + (prob_data_jja * (1 - mult)) for mult in mults]
    return np.array(prob_data_over_times)


def get_all_data():
    for scenario in ("a1b",):
        for var_id in ("tas", "pr"):
            for temporal_average in ("djf", "jja"):
                print "\n-------------------"
        get_data(**vars())


def modify_gridded_5km(array, date_times, **facets):
    """
    Modify the array provided based on example input data.

    :param array:
    :param time_step:
    :param facets:
    :return: None
    """
    len_t, len_y, len_x = array.shape
    new_array = array.copy()

    var_id = facets["var_id"]
    scenario = facets["scenario"]
    prob_data_type = facets["prob_data_type"]
    grid_res = facets["grid_res"]
    temp_avg_type = facets["temp_avg_type"]
    year = date_times[0].year

    eg_data = _get_ls1_prob_site_data(var_id, year, scenario=scenario,
                                          prob_data_type=prob_data_type, grid_res=grid_res,
                                          temp_avg_type=temp_avg_type)

    for t_index, value in enumerate(eg_data):
        for y in range(len_y):
            mult = (len_y + 0.5) / len_y
            values = mult * (npr.random(len_x) / 10. + 1) * value
            new_array[t_index][y] = values

    return new_array


if __name__ == "__main__":

    print _get_ls1_prob_site_data('tas', 20, scenario="a1b",
                            prob_data_type="mon", grid_res="25km",
                            temp_avg_type="mon")