
# Standard library imports
import os, re
from itertools import product
#from datetime import datetime, timedelta
import json

# Third-party imports
from netCDF4 import Dataset
import numpy

# Local imports
from time_series_generator import TimeSeriesGenerator
from nc4_maker import *


OUTPUT_DIR = "output"
RECIPE_DIR = "recipes"

TP_NAME = '__time_period__'


def read_config(id):
    config_file = os.path.join(RECIPE_DIR, id)
    if not os.path.isfile(config_file):
        raise Exception("[ERROR] file '{}' not found.".format(config_file))

    with open(config_file) as reader:
        return json.load(reader)


def clone_dataset(id):

    # Parse configuration and read source file
    config = read_config(id)
    ds = Dataset(config['source']['source_file'])
    variables = ds.variables
    dimensions = ds.dimensions

    fill_values = dict([(var_id, getattr(ds.variables[var_id], "_FillValue", None)) for var_id 
                       in ds.variables.keys()])

    pattn = re.compile(r'\{(.+?)\}')
    file_name_tmpl = config['path_template']
    facet_order = []

    for match in pattn.findall(file_name_tmpl):
        if match not in facet_order:
            facet_order.append(match)

    
    if TP_NAME in facet_order:
        time_facet_index = facet_order.index(TP_NAME)
        facet_order.remove(TP_NAME)
    
    facet_lists = [config['facets'][facet_name] for facet_name in facet_order] 
    perms = product(*facet_lists)
    p = perms.next()

    facet_dict = dict([(key, p[i]) for i, key in enumerate(facet_order)])
    file_name_tmpl = file_name_tmpl.replace('{{{}}}'.format(TP_NAME), '__TIME_PERIOD__')

    # Set up time dimension
    tc = config['time']
    generator = TimeSeriesGenerator(tc['start'], tc['end'], tc['delta'],
                                    tc['attributes']['calendar'],
                                    format='datetime')

    time_array = []
    date_times = []

    for i, (value, dt) in enumerate(generator):
        if i >= config['time']['per_file']: break
        time_array.append(value)
        date_times.append(dt)

    # Define output file path
    time_format = config['time']['format']
    fname_time_comp = "{}-{}".format(date_times[0].strftime(time_format),
                                     date_times[-1].strftime(time_format))
    file_name_tmpl = file_name_tmpl.replace('__TIME_PERIOD__', fname_time_comp)

    fpath = os.path.join(OUTPUT_DIR, file_name_tmpl.format(**facet_dict))

    write_output_file(config, fpath, variables, dimensions, fill_values, time_array, facet_dict)


def write_output_file(config, fpath, variables, dimensions, fill_values, time_array, facet_dict):

    # Create output file and write contents to it
    output = NetCDF4Maker(fpath)

    dim_args = [(key, len(value)) for (key, value) in dimensions.items()]
    output.create_dimensions(*dim_args) 

    for var_id, variable in variables.items():

        if var_id == config['source']['source_var']:
            new_var_id = facet_dict['var_id']
            var_info = config['variables'][new_var_id]
            var_attrs = var_info['attributes']
            data = variable[:] * var_info['conversion_factor']
            dtype = getattr(numpy, var_info['dtype'])

        elif var_id == config['source']['source_time_var']:
            new_var_id = 'time'
            var_attrs = config['time']['attributes'] 
            data = numpy.array(time_array, 'f')
            dtype = numpy.float32

        else:
            new_var_id = var_id
            data = variable[:]
            dtype = variable.dtype
            var_attrs = dict([(key, getattr(variable, key)) for key in variable.ncattrs() if key
                              not in ('_FillValue',)])

        output.create_variable(new_var_id, data, dtype, variable.dimensions,
                               fill_value=fill_values[var_id], attributes=var_attrs)
        
    output.create_global_attrs(**facet_dict)

    output.close()
    print "Wrote: {}".format(fpath)


if __name__ == '__main__':

    clone_dataset("ukcp18/ukcp18_ls1_gridded.json")
