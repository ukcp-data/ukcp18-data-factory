import os
import re
from itertools import product
from datetime import datetime, timedelta
import json

from netCDF4 import Dataset
import numpy 
from nc4_maker import *


OUTPUT_DIR = "output"
RECIPE_DIR = "recipes"


def _add_year(t):
    t[0] += 1

def _add_month(t):
    if t[1] < 12:
        t[1] += 1
    else:
        t[1] = 1
        _add_year(t)

def _add_day(t):
    if t[2] < 30:
        t[2] += 1
    else:
        t[2] = 1
        _add_month(t)


def generate_time_series(td):
    # Assumes 360day calendar
    delta_n, unit = td['delta']
    current_time = td['start']
    value = 0

    while current_time < td['end']:
        yield (value, datetime(*current_time))
        value += 1

        if unit == "year":
            add_func = _add_year
        elif unit == "month":
            add_func = _add_month
        elif unit == "day":
            add_func = _add_day

        for i in range(delta_n): add_func(current_time)
          

def read_config(id):
    config_file = os.path.join(RECIPE_DIR, id)
    with open(config_file) as reader:
        return json.load(reader)

def clone_dataset(id):
    config = read_config(id)
    ds = Dataset(config['source']['source_file'])
    variables = ds.variables
    dimensions = ds.dimensions
    #global_attrs = dict([(key, getattr(ds, key)) for key in ds.ncattrs()])
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

    generator = generate_time_series(config['time'])

    time_array = []
    date_times = []

    print config['time']['per_file']
  
    for i, (value, dt) in enumerate(generator):
        if i >= config['time']['per_file']: break
        time_array.append(value)
        date_times.append(dt)
        print value, dt 
    """
    'time': {
        'start': [2000, 1, 1],
        'end': [2020, 12, 1],
        'format': '%Y%m',
        'delta': (1, "month"),
        'per_file': 12,
        'attributes': {
            'units': 'days since 2000-01-01 00:00:00',
            'calendar': '360day',
            'standard_name': 'time'
            }
        }
    }
""" 
     
    time_format = config['time']['format']
    fname_time_comp = "{}-{}".format(date_times[0].strftime(time_format),
                                     date_times[-1].strftime(time_format))
    file_name_tmpl = file_name_tmpl.replace('__TIME_PERIOD__', fname_time_comp)

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

        elif var_id == config['source']['source_time_var']:
            var_attrs = config['time']['attributes'] 
            data = numpy.array(time_array, 'f')
            dtype = numpy.float32

        output.create_variable(new_var_id, data, dtype, value.dimensions, 
                               fill_value=fill_values[var_id], attributes=var_attrs)
        
    output.create_global_attrs(**d)

    output.close()
    print "Wrote: {}".format(fpath)


if __name__ == '__main__':

    clone_dataset("ukcp18/ukcp18_ls1_gridded.json")
