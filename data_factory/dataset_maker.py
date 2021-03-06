"""
dataset_maker.py
================

Holds the DatasetMaker class for building example files.

"""


# Standard library imports
import os, re
import importlib
from itertools import product
import json
import random
import calendar
import logging

# Third-party imports
from netCDF4 import Dataset
import numpy

# Local imports
from time_series_generator import TimeSeriesGenerator
from nc4_maker import *


logging.basicConfig()
log = logging.getLogger(__name__)


RECIPE_DIR = "recipes"
TP_NAME = '__time_period__'


class DatasetMaker(object):
    """
    Class to generate example datasets of synthetic data.
    """

    def __init__(self, project, dataset_id, constraints=None, base_dir="fakedata"):
        """
        :param project: project id [string]
        :param dataset_id: dataset id [string]
        :param constraints: dictionary of constraints to reduce the amount of data generated.
        :param base_dir: base directory for outputs.
        """
        self.project = project
        self.dataset_id = dataset_id
        self.base_dir = base_dir

        # Set constraints as empty dictionary at start
        self.constraints = {}

        # Load main settings from JSON file
        self._load_options()

        # Update with constraints sent in as argument
        self.set_constraints(constraints)

        # Set time units
        self._set_time_units_from_settings()


    def _load_options(self):
        """
        Reads the configuration file for a given project/dataset and stores
        that information in `self.settings` ready for use.

        :return: None
        """
        # Check constraints and options
        config_file = os.path.join(RECIPE_DIR, self.project, "{}.json".format(self.dataset_id))

        if not os.path.isfile(config_file):
            raise Exception("[ERROR] file '{}' not found.".format(config_file))

        with open(config_file) as reader:
            self.settings = json.load(reader)

        # Read in any other JSON files from "__include_files__" property
        include_files = self.get_setting("__include_files__", default={})

        if include_files:
            for fpath in include_files:

                with open(fpath) as reader:
                    print "Parsing extra settings from: {}".format(fpath)
                    _settings = json.load(reader)

                    for key in _settings.keys():

                        # Only override if setting does NOT already exist
                        if key not in self.settings:
                            self.settings[key] = _settings[key]


        # Update settings using "__includes__" in the JSON
        self._add_includes_to_settings()


    def _add_includes_to_settings(self):
        """
        Searches for the "__include__" option in the settings and replaces
        with common sections in the "__inclusions__" part of the JSON.

        :return:
        """
        INCLUSIONS_KEY = "__inclusions__"
        INCLUDE_KEY = "__include__"
        inclusions = self.settings.get(INCLUSIONS_KEY, {})

        def update_dct_from_inclusions(dct):
            """
            Updates current dct key if set as an "__include__".

            :param dct: a dictionary (part of settings)
            :return: None
            """
            for key, value in dct.items():
                if type(value) is dict:
                    update_dct_from_inclusions(value)
                    continue

                elif key == INCLUSIONS_KEY or key != INCLUDE_KEY:
                    continue

                # Only main "__include__" will get here, now update it
                for dkey, dvalue in inclusions[value].items():
                    dct[dkey] = dvalue

                # And remove the include item to tidy up
                del dct[INCLUDE_KEY]

        # Start with whole settings and then recursively call the updater function
        dct = self.settings
        update_dct_from_inclusions(dct)


    def _set_time_units_from_settings(self):
        """
        Sets the time units based on first date in settings/constraints.

        :return: None
        """
        # Set the time units for all output files based on the first time step requested
        start_time = self.get_setting('time', 'start')
        time_units = "days since {:04d}-{:02d}-{:02d} 00:00:00".format(*start_time)

        self.settings['time']['attributes']['units'] = time_units


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
        # Set up facet order
        pattn = re.compile(r'\{(.+?)\}')
        file_name_tmpl = self.get_setting('path_template')
        self.facet_order = []

        for match in pattn.findall(file_name_tmpl):
            if match not in self.facet_order:
                self.facet_order.append(match)

        if TP_NAME in self.facet_order:
            self.facet_order.remove(TP_NAME)

        # Set up facets super list
        self.facet_super_lists = []

        for facet_name in self.facet_order:
            # Handle dataset_id differently
            if facet_name == 'dataset_id':
                value = ['__TO_BE_DETERMINED_FROM_TEMPLATE__']
            else:
                value = self.get_setting('facets', facet_name)

            self.facet_super_lists.append(value)


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
            log.info("Setting constraints")
            self.set_constraints(constraints)

        # Load up input data
        log.info("Loading input data")
        self._load_input_data()

        # Set up facets
        log.info("Setting up facets")
        self._setup_facets()

        # Get all permutations of all facets
        facet_permutations = [prod for prod in product(*self.facet_super_lists)]

        # Randomise order if specified
        if randomise:
            random.shuffle(facet_permutations)

        file_count = 0
        stop = False

        time_array_len = -1

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
            time_items = [_tm for _tm in time_generator]
            for value, dt in time_items:

                count_per_file += 1
                time_array.append(value)
                date_times.append(dt)

                if count_per_file == self.get_setting('time', 'per_file') or \
                        (value, dt) == time_items[-1]:

                    self.current['date_times'] = date_times

                    # Get output path and write output file
                    output_path = self._get_output_path(time_array, date_times, file_name_tmpl)
                    self._write_output_file(output_path, time_array, date_times)
                    file_count += 1

                    time_array_len = len(time_array) # for reporting

                    # Reset some settings ready for next file to be populated
                    count_per_file = 0
                    date_times = []
                    time_array = []

                if file_count >= max_num:
                    stop = True
                    break

        print "Ran {} files; for {} time steps per file".format(file_count, time_array_len)


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

        start = date_times[0]
        end = date_times[-1]

        # Check if we should set dates in file name to day 1 of month at start
        # and last day of final month (rather than day used in file).
        span_month_days = self.get_setting('time', 'span_month_days', default=False)
        _calendar = self.get_setting('time', 'attributes', 'calendar')

        if span_month_days:

            _start_time_format = time_format.replace('%d', '01')

            if _calendar == "360_day":
                _end_time_format = time_format.replace('%d', '30')
            else:
                days_in_end_month = calendar.monthrange(end.year, end.month)
                _end_time_format = time_format.replace('%d', '{}'.format(days_in_end_month))

            start = start.strftime(_start_time_format)
            end = end.strftime(_end_time_format)

        else:
            start, end = [_dt.strftime(time_format) for _dt in start, end]

        fname_time_comp = "{}-{}".format(start, end)

        # Add in the current time range to the file name template
        file_name_tmpl = file_name_tmpl.replace('__TIME_PERIOD__', fname_time_comp)

        # Generate the 'dataset_id' value from the 'dataset_id_template' facet
        self.current['facets']['dataset_id'] = \
            self.get_setting('dataset_id_template').format(**self.current['facets'])

        # Work out file path
        fpath = os.path.join(self.base_dir, file_name_tmpl.format(**self.current['facets']))
        return fpath


    def _get_coord_var_id_from_dim_id(self, dim_id):
        """
        Returns coordinate variable ID from facet lookup of dimension ID.

        :param dim_id: dimension ID
        :return: coordinate variable ID
        """
        facet_id = dim_id.split(":")[-1]
        coord_var_id = self.current['facets'][facet_id]
        return coord_var_id


    def _load_extra_coord_vars(self):
        """
        Call out to external code to get extra coordinate variables required for this
        variable.

        :return: a dictionary of coordinate variables.
        """
        var_id = self.current['facets']['var_id']
        required_dims = self.get_setting('variables', var_id, 'dimensions')

        coord_vars = {}

        for dim in required_dims:

            if dim.find("facet:") == 0:
                coord_var_id = self._get_coord_var_id_from_dim_id(dim)

                # Import modifier module then call the loader function
                lookup = self.get_setting('variables', var_id, 'coord_var_loaders', coord_var_id)

                coord_var = self._evaluate_lookup(lookup)
                coord_vars[coord_var_id] = coord_var

        return coord_vars


    def _get_modified_variable(self, variable):
        """
        Call out to external code to modify the array if specified in settings.
        Returns a tuple of: (new_array, dimensions_list).

        :param variable: netCDF4 Variable (from input data).
        :return: Tuple of: (new_array, dimensions_list).
        """
        var_info = self.get_setting('variables', self.current['facets']['var_id'])

        modifier = var_info.get('array_modifier', None)
        conversion_factor = var_info.get('conversion_factor', None)

        # Call modifier code if set
        if modifier != None:
            new_array, dims_list = self._evaluate_lookup(modifier, *[variable, self.current["date_times"]],
                                                         **self.current["facets"])

        # Apply conversion factor if set
        elif conversion_factor != None:
            new_array = variable[:] * conversion_factor
            dims_list = variable.dimensions

        else:
            return variable[:], variable.dimensions

        return new_array, dims_list


    def _resolve_variable_arrays_by_facet(self, var_id):
        """

        :param var_id:
        :return: array
        """
        lookup = self.get_setting('variables_by_facet', var_id)

        # Import modifier module then send the variable to the modifier function
        array = self._evaluate_lookup(lookup, **self.current["facets"])
        return array


    def _evaluate_lookup(self, lookup, *args, **kwargs):
        """
        Resolves a lookup and imports and evaluates a call, returning the response.

        :param lookup: look-up string (module import then "#" then function.
        :param args: list of arguments
        :param kwargs: dictionary of keyword arguments
        :return: return call to the relevant function with arguments.
        """
        path, func = lookup.split('#')

        # Import module then send the args and kwargs to the function
        module = importlib.import_module(path)
        response = getattr(module, func)(*args, **kwargs)

        return response


    def get_global_attributes(self):
        """
        Looks up and generates a dictionary of global attributes for the NC file.

        return: dictionary of global attributes to write.
        """
        global_attrs = self.get_setting("global_attributes").copy()
        facets = self.current['facets']

        # Update global attrs if any values are calculated dynamically
        CALC_FROM = 'calculate_from:'
        DO_NOT_SET = '__DO_NOT_SET__'

        for key in global_attrs.keys():
            if key == DO_NOT_SET: continue
            value = global_attrs[key]

            if value.startswith(CALC_FROM):
                lookup = value.replace(CALC_FROM, "")
                value = self._evaluate_lookup(lookup, **facets)
                global_attrs[key] = value
            elif key in facets:
                global_attrs[key] = facets[key]

        # Now add facets but ignore omissions
        not_to_set = global_attrs.get(DO_NOT_SET, [])

        for key, value in facets.items():
            if key in not_to_set: continue
            global_attrs[key] = value

        # Remove DO NOT SET value if there
        if DO_NOT_SET in global_attrs: del global_attrs[DO_NOT_SET]

        return global_attrs


    def _write_output_file(self, fpath, time_array, date_times):
        """
        Writes the output file to: `fpath`.

        Uses information saved in the settings and input data
        and associates them with the times in the `time_array`.

        :param time_array: list of time values (as numbers)
        :param date_times: list of datetimes
        :return: None
        """
        print "Starting to write to: {}".format(fpath)
        # Create output file and write contents to it
        output = NetCDF4Maker(fpath, verbose=False)

        # Get the dimensions from the input file
        dim_args = []

        for key, value in self.input_data['dimensions'].items():
            if value.isunlimited():
                length = None
            else:
                length = len(value)

            # Override length of time which is dynamic - set to "unlimited"
            if key == "time":
                length = None
#                length = len(time_array)

            dim_args.append((key, length))

        # Load up any extra coordinate variables also required by this dataset
        extra_coord_vars = self._load_extra_coord_vars()

        # Add extra coord vars to dimensions list
        for key, value in extra_coord_vars.items():
            dim_args.append((key, len(value)))

        # Write dimensions
        output.create_dimensions(*dim_args)

        # Loop through the files in the input data and modify them before writing
        # as specified in the settings
        # Also loop through the extra_coord_vars
        all_vars = {}

        for dct in (self.input_data['variables'], extra_coord_vars):
            for key, value in dct.items():
                all_vars[key] = value

        # Now loop through and create all variables
        for var_id, variable in all_vars.items():

            if var_id == "climatology_bounds":
                print "IGNORING WRITING: climatology_bounds - for now!"
                continue

            if var_id == "season_year":
                # Assumes Met Office-style DJF, MAM, JJA, SON seasons
                new_var_id = var_id
                dtype = numpy.int32
                var_attrs = {'long_name': 'season_year', 'units': '1'}

                # Extract
                years = []
                for _dt in date_times:
                    _year = _dt.year
                    if _dt.month == 12:
                        _year += 1
                    years.append(_year)

                data = numpy.array(years, 'int32')
                dims_list = ['time']

            elif var_id == self.get_setting('source', 'source_var'):
                new_var_id = self.current['facets']['var_id']
                var_info = self.get_setting('variables', new_var_id)
                var_attrs = var_info['attributes']
                dtype = getattr(numpy, var_info['dtype'])

                # Modify array if necessary
                data, dims_list = self._get_modified_variable(variable)

            elif var_id == self.get_setting('source', 'source_time_var'):
                new_var_id = 'time'
                var_attrs = self.get_setting('time', 'attributes')
                data = numpy.array(time_array, 'f')
                dims_list = variable.dimensions
                dtype = numpy.float32

                # Add time bounds
                self._add_time_bounds(output, data, var_attrs)

            else:
                new_var_id = var_id
                data = variable[:]
                dtype = variable.dtype

                # Resolve the variable array if required
                if self.get_setting('variables_by_facet', new_var_id, default=[]):
                    data = self._resolve_variable_arrays_by_facet(new_var_id)

                if hasattr(variable, "dimensions"):
                    dims_list = variable.dimensions
                # Assume that it is a coordinate variable that will have its own dimension
                else:
                    dims_list = [new_var_id]

                if hasattr(variable, "ncattrs"):
                    var_attrs = dict([(key, getattr(variable, key)) for key in variable.ncattrs() if key
                                  not in ('_FillValue',)])
                else:
                    var_attrs = {'long_name': new_var_id}

            print "Now writing variable: {}".format(new_var_id)
            fill_value = getattr(variable, "_FillValue", None)
            output.create_variable(new_var_id, data, dtype, dims_list,
                                   fill_value=fill_value, attributes=var_attrs)

        global_attrs = self.get_global_attributes()
        output.create_global_attrs(**global_attrs)

        output.close()
        print "Wrote: {}".format(fpath)


    def _add_time_bounds(self, output, time_data, time_var_attrs):
        """
        Write the `time_bounds` variable to the output file.
        Also modify the attributes dictionary: time_var_attrs

        :param output: output writer job
        :param data: time array
        :param var_attrs: time attributes
        :return: None
        """
        var_id = "time_bounds"
        time_var_attrs["bounds"] = var_id
        interval = (time_data[1] - time_data[0]) / 2.

        values = [[value - interval, value + interval] for value in time_data[:]]
        array = numpy.array(values)

        output.create_variable(var_id, array, "float64", ["time", "bnds"])


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


    def get_setting(self, *options, **kwargs):
        """
        Looks up a setting in `self.constraints`. If not held there it looks it up in
        `self.settings`. The `options` are defined using a tuple of keys, such as:
        ("variable", "precip", long_name").
        If the setting cannot be found then an exception is raised.

        :param options: setting specifier [tuple].
        :param kwargs: keyword arguments - to provide default.
        :return: The value of the setting.
        """
        default = kwargs.get('default', None)

        value = self._resolve_nested_lookup(self.constraints, options, default=default)

        if value:
            return value

        value = self._resolve_nested_lookup(self.settings, options, default=default)

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
