"""
dataset_maker.py
================

Holds the DatasetMaker class for building example files.

"""


# Standard library imports
import os, re
from itertools import product
import json
import random

# Third-party imports
from netCDF4 import Dataset
import numpy

# Local imports
from time_series_generator import TimeSeriesGenerator
from nc4_maker import *


RECIPE_DIR = "recipes"
TP_NAME = '__time_period__'


class DatasetMaker(object):
    """

    """

    def __init__(self, project, dataset_id, constraints=None, base_dir="fakedata"):
        """

        :param project:
        :param dataset_id:
        :param constraints:
        :param base_dir:
        """
        self.project = project
        self.dataset_id = dataset_id
        self.base_dir = base_dir

        self._load_options()

        # Set constraints as empty dictionary
        self.constraints = {}
        self.set_constraints(constraints)

    def _load_options(self):
        """
        Reads the configuration file for a given project/dataset and stores
        that information ready for use.

        :return:
        """
        # Check constraints and options
        config_file = os.path.join(RECIPE_DIR, self.project, "{}.json".format(self.dataset_id))

        if not os.path.isfile(config_file):
            raise Exception("[ERROR] file '{}' not found.".format(config_file))

        with open(config_file) as reader:
            self.settings = json.load(reader)


    def _load_input_data(self):
        """
        Loads input data from data file specified in settings.

        :return: None
        """
        self.input_data = {}

        ds = Dataset(self.get_setting('source', 'source_file'))
        self.input_data['ds'] = ds
        self.input_data['variables'] = ds.variables
        self.input_data['dimensions'] = ds.dimensions


    def _setup_facets(self):
        """
        Reads settings to generate facet information.

        :return: None
        """
        pattn = re.compile(r'\{(.+?)\}')
        file_name_tmpl = self.get_setting('path_template')
        facet_order = []

        for match in pattn.findall(file_name_tmpl):
            if match not in facet_order:
                facet_order.append(match)

        if TP_NAME in facet_order:
            facet_order.remove(TP_NAME)

        self.facet_super_lists = [self.get_setting('facets', facet_name) for facet_name in facet_order]
        self.facet_order = facet_order


    def _get_time_generator(self):
        """
        Returns a generator for all date/times required.

        :return: TimeSeriesGenerator instance.
        """
        time_generator = TimeSeriesGenerator(
            self.get_setting('time', 'start'),
            self.get_setting('time', 'end'),
            self.get_setting('time', 'delta'),
            self.get_setting('time', 'attributes', 'calendar'),
            format='datetime')

        return time_generator


    def generate(self, constraints=None, max_num=999999, randomise=False):
        """
        Generator to return the next file path based on an optional set of `constraints`.
        Specifying `max_num` will return after yielding the number given.
        Setting `randomise` to True will return them in a random order.

        :param constraints:
        :param max_num:
        :param randomise:
        :return:
        """
        if constraints:
            self.set_constraints(constraints)

        # Load up input data
        self._load_input_data()

        # Set up facets
        self._setup_facets()

        # Get all permutations of all facets
        facet_permutations = [prod for prod in product(*self.facet_super_lists)]

        # Randomise order if specified
        if randomise:
            random.shuffle(facet_permutations)

        file_count = 0
        stop = False

        # Loop through all permutations
        for facets in facet_permutations:

            if stop: break

            # Create instance dictionary to store current options
            self.current = {}
            self.current['facets'] = dict([(key, facets[i]) for i, key in enumerate(self.facet_order)])

            file_name_tmpl = self.get_setting('path_template').replace('{{{}}}'.format(TP_NAME), '__TIME_PERIOD__')

            # Set up time generator to step through time values
            time_generator = self._get_time_generator()

            time_array = []
            date_times = []

            count_per_file = 0

            # Loop through time steps and write a new file whenever the number of times
            # matches the number allowed per file
            for value, dt in time_generator:
                if count_per_file == self.get_setting('time', 'per_file'):

                    self.current['date_times'] = date_times

                    # Get output path and write output file
                    output_path = self._get_output_path(time_array, date_times, file_name_tmpl)
                    self._write_output_file(output_path, time_array)
                    file_count += 1

                    # Reset some settings ready for next file to be populated
                    count_per_file = 0
                    date_times = []
                    time_array = []

                count_per_file += 1
                time_array.append(value)
                date_times.append(dt)

                if file_count > max_num:
                    stop = True
                    break

        print "Ran {} files; for {} time steps per file".format(file_count, len(time_array))


    def _get_output_path(self, time_array, date_times, file_name_tmpl):
        """
        Work out output file path and return full path.

        :param time_array:
        :param date_times:
        :param file_name_tmpl:
        :return: path for output file.
        """
        # Define output file path
        time_format = self.get_setting('time', 'format')
        fname_time_comp = "{}-{}".format(date_times[0].strftime(time_format),
                                         date_times[-1].strftime(time_format))

        # Add in the current time range to the file name template
        file_name_tmpl = file_name_tmpl.replace('__TIME_PERIOD__', fname_time_comp)
        fpath = os.path.join(self.base_dir, file_name_tmpl.format(**self.current['facets']))
        return fpath


    def _get_modified_array(self, array):
        """
        Call out to external code to modify the array if specified in settings.
        Returns None - array is modified in place.

        :param variable: netCDF4 Variable (from input data).
        :return: new array
        """
#        if 1: return

        var_info = self.get_setting('variables', self.current['facets']['var_id'])

        # Call modifier code if set
        modifier = var_info.get('array_modifier', None)
        if modifier != None:
            path, func = modifier.split('#')

            # Import modifier module then send the variable to the modifier function
            imp = 'import {}'.format(path)
            exec(imp)
            new_array = eval('{}.{}(array, self.current["date_times"], **self.current["facets"])'.format(path, func))
            print new_array.min(), new_array.max()

        # Apply conversion factor if set
        conversion_factor = var_info.get('conversion_factor', None)
        if conversion_factor != None:
            new_array = array * conversion_factor

        return new_array


    def _write_output_file(self, fpath, time_array):
        """

        :param fpath:
        :param variables:
        :param dimensions:
        :param fill_values:
        :param time_array:
        :param facet_dict:
        :return:
        """
        # Create output file and write contents to it
        output = NetCDF4Maker(fpath)

        # Create the dimensions in the output file
        dim_args = [(key, len(value)) for (key, value) in self.input_data['dimensions'].items()]
        output.create_dimensions(*dim_args)

        # Loop through the files in the input data and modify them before writing
        # as specified in the settings
        for var_id, variable in self.input_data['variables'].items():

            if var_id == self.get_setting('source', 'source_var'):

                new_var_id = self.current['facets']['var_id']
                var_info = self.get_setting('variables', new_var_id)
                var_attrs = var_info['attributes']
                dtype = getattr(numpy, var_info['dtype'])

                # Modify array if necessary
                data = self._get_modified_array(variable[:])

            elif var_id == self.get_setting('source', 'source_time_var'):
                new_var_id = 'time'
                var_attrs = self.get_setting('time', 'attributes')
                data = numpy.array(time_array, 'f')
                dtype = numpy.float32

            else:
                new_var_id = var_id
                data = variable[:]
                dtype = variable.dtype
                var_attrs = dict([(key, getattr(variable, key)) for key in variable.ncattrs() if key
                                  not in ('_FillValue',)])

            fill_value = getattr(self.input_data['variables'][var_id], "_FillValue", None)
            print new_var_id, data.min(), data.max()
            output.create_variable(new_var_id, data, dtype, variable.dimensions,
                                   fill_value=fill_value, attributes=var_attrs)

        output.create_global_attrs(**self.current['facets'])

        output.close()
        print "Wrote: {}".format(fpath)

    def set_constraints(self, constraints=None):
        """
        Sets constraints that override the settings to reduce the number of output files.
        Takes a dictionary that can include the following keys:
            ['time']['start'|'end'] - can only override start/end of time
            ['variables']['*'] - can override any part of variables settings
            ['facets']['*'] - can override any part of facets settings

        :param constraints: dictionary of dictionaries specifying data files to be produced.
        :return: None
        """
        if not constraints:
            return

        if type(constraints) != dict:
            raise Exception("Constraints must be provided as a dictionary.")

        allowed_constraints = ("time", "variables", "facets")

        for key, value in constraints.items():
            if key not in allowed_constraints:
                raise Exception("Constraints on '{}' are not permitted.".format(key))

            self.constraints[key] = constraints[key]

    def _resolve_nested_lookup(self, dct, keys, default=None):
        """
        Resolves and returns item held in nested dictionary `dct` based on a tuple of
        `keys` as the lookup.
        Returns `default` if not found.

        :param dct: nested dictionary.
        :param keys: tuple of keys.
        :return: value or default.
        """
        value = dct
        for key in keys:
            try:
                value = value[key]
            except:
                return default

        return value

    def get_setting(self, *options):
        """
        Looks up a setting in `self.constraints`. If not held there it looks it up in
        `self.settings`. The `options` are defined using a tuple of keys, such as:
        ("variable", "precip", long_name").
        If the setting cannot be found then an exception is raised.

        :param options: setting specifier [tuple].
        :return: The value of the setting.
        """
        value = self._resolve_nested_lookup(self.constraints, options)

        if value != None:
            return value

        value = self._resolve_nested_lookup(self.settings, options)

        if value == None:
            raise Exception("Could not find value in constraints or settings for: '{}'.".format(options))

        return value


    def __iter__(self):
        """

        :return:
        """
        return self

    def __next__(self):
        """
        Returns next file path.
        :return:
        """
        # Returns next path
        # use itertools.product here

    def next(self):
        """

        :return:
        """
        return self.__next__()