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
            'time': {'start': [2000, 12, 15],
                     'end': [2005, 11, 15]},
            'facets':
                  {'scenario': ['rcp85'],
                   'prob_data_type': ['percentile']
            }
         },
    ('ukcp18', 'ukcp18-land-prob-uk-region-all'):
        {
            'time': {'start': [1960, 12, 15],
                     'end': [2099, 11, 15]},
            'facets':
                {'scenario': ['a1b'],
                 'prob_data_type': ['sample']
                 }
        },
    ('ukcp18', 'ukcp18-land-gcm-global-60km-mon'):
        {
            'time': {'start': [2010, 12, 15]},
            'facets':
                {'scenario': ['rcp85']}
        },
    ('ukcp18', 'ukcp18-land-gcm-uk-60km-mon'):
        {
            'time': {'start': [1901, 12, 15], 'end': [2099, 11, 15]},
            'facets':
                {'scenario': ['rcp85']}
        },
    ('ukcp18', 'ukcp18-land-gcm-uk-river-mon'):
        {
            'time': {'start': [1901, 12, 15], 'end': [2099, 11, 15]},
            'facets':
                {'scenario': ['rcp85']}
        },
    ('ukcp18', 'ukcp18-land-gcm-uk-region-mon'):
        {
            'time': {'start': [1901, 12, 15], 'end': [2099, 11, 15]},
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
                    ('ukcp18', 'ukcp18-land-gcm-global-60km-mon'),
                    ('ukcp18', 'ukcp18-land-gcm-uk-60km-mon'),
                    ('ukcp18', 'ukcp18-land-gcm-uk-river-mon')
    ]

    if len(args) == 0:
        print "Default args: {}".format(str(DEFAULT_ARGS))
        all_datasets = [DEFAULT_ARGS]
    elif args == ["--batch"]:
        print "Batch creating all..."
    elif len(args) == 1:
        all_datasets = [args[0].replace("recipes", "").replace("/", " ").split(".")[0].split()]
    elif len(args) == 2:
        all_datasets = [args]
    else:
        raise Exception("Must provide arguments: <project> <dataset_id>")

    for args in all_datasets:
        print "Working on:", args
        main(*args)
