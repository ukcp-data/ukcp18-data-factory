#!/usr/bin/env python

"""
create_dataset.py
=================

"""

import sys, os

from data_factory.dataset_maker import DatasetMaker

_CONSTRAINTS_SETS = {
    ('ukcp18', 'ukcp18-land-prob-uk-25km-all'):
        {
            'time': {'start': [2000, 1, 15],
                     'end': [2005, 12, 15]},
            'facets':
                  {'scenario': ['rcp85'],
                   'prob_data_type': ['percentile']
            }
         },
    ('ukcp18', 'ukcp18-land-prob-uk-region-all'):
        {
            'time': {'start': [2010, 1, 15],
                     'end': [2010, 12, 15]},
            'facets':
                {'scenario': ['a1b'],
                 'prob_data_type': ['percentile', 'sample']
                 }
        },
    ('ukcp18', 'ukcp18_ls2_global_gridded'):
        {
            'time': {'start': [2010, 1, 1]},
            'facets':
                {'scenario': ['rcp85']}
        },
    ('ukcp18', 'ukcp18_ls2_uk_gridded'):
        {
            'time': {'start': [1901, 1, 1], 'end': [2100, 12, 30]},
            'facets':
                {'scenario': ['rcp85']}
        },
    ('ukcp18', 'ukcp18_ls2_uk_river_basin'):
        {
            'time': {'start': [1901, 1, 1], 'end': [2100, 12, 30]},
            'facets':
                {'scenario': ['rcp85']}
        }
}


def main(project, dataset_id, constraints=None):
    if dataset_id.find("-") < 0:
        raise Exception("Please modify the JSON recipe to follow new rules - using dataset IDs.")

    if not constraints: constraints = _CONSTRAINTS_SETS[(project, dataset_id)]

    faker = DatasetMaker(project=project, dataset_id=dataset_id, constraints=constraints)
    faker.generate(randomise=False, max_num=3)


if __name__ == "__main__":

    args = sys.argv[1:]

    DEFAULT_ARGS = ('ukcp18', 'ukcp18-land-prob-uk-region-all')
    DEFAULT_ARGS = ('ukcp18', 'ukcp18-land-prob-uk-25km-all')


    all_datasets = [('ukcp18', 'ukcp18-land-prob-uk-25km-all'),
                    ('ukcp18', 'ukcp18_ls2_global_gridded'),
                    ('ukcp18', 'ukcp18_ls2_uk_gridded'),
                    ('ukcp18', 'ukcp18_ls2_uk_river_basin')
    ]

    if len(args) == 0:
        print "Default args: {}".format(str(DEFAULT_ARGS))
        all_datasets = [DEFAULT_ARGS]
    elif args == ["--batch"]:
        print "Batch creating all..."
    elif len(args) == 2:
        all_datasets = [args]
    else:
        raise Exception("Must provide arguments: <project> <dataset_id>")

    for args in all_datasets:
        print "Working on:", args
        main(*args)
