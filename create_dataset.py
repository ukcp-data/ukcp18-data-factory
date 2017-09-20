#!/usr/bin/env python

"""
create_dataset.py
=================

"""

import sys, os

#from data_factory.data_maker import clone_dataset
from data_factory.dataset_maker import DatasetMaker


def main(project, dataset_id):
    constraints = {'time':
                       {'start': [2010, 1, 1]},
                   'facets':
                       {'scenario': ['a1b'],
                        'prob_data_type': ['percentile']}
#                         'prob_data_type': ['percentile', 'sample']}
                   }
    faker = DatasetMaker(project=project, dataset_id=dataset_id, constraints=constraints)
    faker.generate(randomise=False, max_num=100)


if __name__ == "__main__":

    args = sys.argv[1:]

    if len(args) == 0:
        print "Default args: ['ukcp18', 'ukcp18_ls1_gridded']"
        args = ['ukcp18', 'ukcp18_ls1_gridded']
    elif len(args) != 2:
        raise Exception("Must provide arguments: <project> <dataset_id>")

    main(*args)
