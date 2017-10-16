#!/usr/bin/env python

"""
create_dataset.py
=================

"""

import sys, os

from data_factory.dataset_maker import DatasetMaker

_CONSTRAINTS_SETS = {
    ('ukcp18', 'ukcp18_ls1_gridded'):
        {
            'time': {'start': [2010, 1, 1]},
            'facets':
                  {'scenario': ['a1b'],
                   'prob_data_type': ['percentile']
            }
         },
    ('ukcp18', 'ukcp18_ls2_gridded'):
        {
            'time': {'start': [2010, 1, 1]},
            'facets':
                {'scenario': ['rcp85']}
        }
}


def main(project, dataset_id, constraints=None):
    if not constraints: constraints = _CONSTRAINTS_SETS[(project, dataset_id)]

    faker = DatasetMaker(project=project, dataset_id=dataset_id, constraints=constraints)
    faker.generate(randomise=True, max_num=10)


if __name__ == "__main__":

    args = sys.argv[1:]
    DEFAULT_ARGS = ['ukcp18', 'ukcp18_ls1_gridded']
    DEFAULT_ARGS = ['ukcp18', 'ukcp18_ls2_gridded']

    if len(args) == 0:
        print "Default args: {}".format(str(DEFAULT_ARGS))
        args = DEFAULT_ARGS
    elif len(args) != 2:
        raise Exception("Must provide arguments: <project> <dataset_id>")

    main(*args)
