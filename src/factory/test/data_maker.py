#from netCDF4 import Dataset
from itertools import product
import re


config = {
    'eg_file': 'x.nc',
    'variables': {
        'precip': {'__conversion_factor__': 4,
                   'standard_name': 'precipitation_rate',
                   'units': 'mm day-1'},
        'tasmax': {'__conversion_factor__': 100,
                   'standard_name': 'air_temperature',
                   'units': 'K'},
    },
    'facets': {
        '__order__': ['project', 'dataset', 'scenario', 'temp_avg'],
        'project': ['ukcp18'],
        'dataset': ['25km-daily', 'obs-global'],
        'scenario': ['rcp45', 'rcp60', 'rcp85'],
        'temp_avg': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    },
    'path_template': {
        'directory': '{project}/{dataset}/{scenario}/{temp_avg}',
        'file_name': '{project}_{dataset}_{scenario}_{temp_avg}_{__time_period__}.nc'
    },
    'time_period': {
        'dates': [
            '20010101', '20010201', '20010301', '20010401', '20010501', '20010601'
        ]
    }
}


def clone_dataset(config=config):
    ds = Dataset(config['eg_file'])
    vars = ds.variables
    dims = ds.dimensions
    global_attrs = dict([getattr(ds, key) for key in ds.ncattrs()])

    pattn = re.compile(r'\{(.+?)\}')
    facet_order = pattn.findall(config['path_template']['file_name'])
    tp_name = '__time_period__'

    if tp_name in facet_order:
        time_facet_index = facet_order.index(tp_name)
        facet_order.remove(tp_name)

    perms = product([config['facets'][facet_name] for facet_name in facet_order])

    for p in perms:
        print p