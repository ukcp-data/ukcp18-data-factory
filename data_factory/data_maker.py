from netCDF4 import Dataset
import os
import numpy 
from itertools import product
from nc4_maker import *
import re


OUTPUT_DIR = "output"


config = {
    'source': {
        'source_file': '../../ukcp09-obs-sample/data/meantemp_1981-2010_LTA.nc',
        'source_var': 'monthly_meantemp'
    },
    'variables': {
        'precip': {'conversion_factor': 4,
                   'dtype': 'float32',
                   'attributes': {
                       'standard_name': 'precipitation_rate',
                       'units': 'mm day-1'
                       },
                  },
        'tasmax': {'conversion_factor': 100,
                   'dtype': 'float32',
                   'attributes': {
                       'standard_name': 'air_temperature',
                       'units': 'K'
                       },
                  },
    },
    'facets': {
        '__order__': ['project', 'dataset', 'scenario', 'temp_avg'],
        'project': ['ukcp18'],
        'dataset': ['25km-daily', 'obs-global'],
        'scenario': ['rcp45', 'rcp60', 'rcp85'],
        'temp_avg': ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'],
        'var_id': ['precip', 'tasmax']
    },
    'path_template': '{project}/{dataset}/{scenario}/{temp_avg}/{var_id}/{var_id}_{project}_{dataset}_{scenario}_{temp_avg}_{__time_period__}.nc',
    'time_periods': {
        'dates': [
            '20010101', '20010201', '20010301', '20010401', '20010501', '20010601'
        ]
    }
}


def clone_dataset(config=config):
    ds = Dataset(config['source']['source_file'])
    variables = ds.variables
    dimensions = ds.dimensions
    global_attrs = dict([(key, getattr(ds, key)) for key in ds.ncattrs()])
    fill_values = dict([(var_id, getattr(ds.variables[var_id], "_FillValue", None)) for var_id 
                       in ds.variables.keys()])

    pattn = re.compile(r'\{(.+?)\}')
    file_name_tmpl = config['path_template']
    facet_order = []

    for match in pattn.findall(file_name_tmpl):
        if match not in facet_order:
            facet_order.append(match)

    tp_name = '__time_period__'
    
    if tp_name in facet_order:
        time_facet_index = facet_order.index(tp_name)
        facet_order.remove(tp_name)
    
    facet_lists = [config['facets'][facet_name] for facet_name in facet_order] 
    perms = product(*facet_lists)
    p = perms.next()

    d = dict([(key, p[i]) for i, key in enumerate(facet_order)])
    file_name_tmpl = file_name_tmpl.replace('{{{}}}'.format(tp_name), '__TIME_PERIOD__')

    file_name_tmpl = file_name_tmpl.replace('__TIME_PERIOD__', config['time_periods']['dates'][0])

    fpath = os.path.join(OUTPUT_DIR, file_name_tmpl.format(**d))
    output = NetCDF4Maker(fpath)

    dim_args = [(key, len(value)) for (key, value) in dimensions.items()]
    output.create_dimensions(*dim_args) 

    for var_id, value in variables.items():
        var_attrs = dict([(key, getattr(value, key)) for key in value.ncattrs() if key
                               not in ('_FillValue',)])
        new_var_id = var_id
        data = value[:]
        dtype = value.dtype

        if var_id == config['source']['source_var']:
            new_var_id = d['var_id']
            var_info = config['variables'][new_var_id]
            var_attrs = var_info['attributes']
            data = value[:] * var_info['conversion_factor']
            dtype = getattr(numpy, var_info['dtype'])

        output.create_variable(new_var_id, data, dtype, value.dimensions, 
                               fill_value=fill_values[var_id], attributes=var_attrs)
        
    output.create_global_attrs(**global_attrs)

    output.close()
    print "Wrote: {}".format(fpath)


if __name__ == '__main__':

    clone_dataset()
