# Guidance on construction of UKCP Land Strand 1 probabilistic datasets

## Change log

### Pending fixes
 - PUT THEM HERE
 
### Changes on 2018-10-12

 - Updated file-naming convention
 - Updated global attributes section

### Changes on 2018-04-18

 - Added section 6.2 on Global Attributes to avoid/remove.
 - Updated variable attributes (5.3) in the example NC files to reflect variables in
   controlled vocab file.
 - Added info about naming `var_id` in files.

### Changes on 2018-03-22

 - Added "creation_date" global attribute
 - Added section on "bounds" for coordinate variables

### Changes on 2018-03-14

 - Updated "project" global attribute
 - Updated file-naming convention
 - Removed "dataset_id" global attribute

### Changes on 2018-03-12

 - Changed numbering of sections (because index was out of sync with main sections).
 - Added `_FillValue` section.

### Changes on 2018-03-01

 - Added in the "cell_methods" attribute for the main variable:
  - `cell_methods = "time: mean" ;`

### Changes on 2018-02-27

 - CF-Conventions: agreed to use "CF-1.5" (in global attribute: "Conventions") 
   so that we can check against this convention with existing checkers
 - The following global attributes have been removed from the specification:
   - "var_id": agreed this duplicates the main variable in the file.
   - "report": agreed that reports will not be ready before data production; 
     the "references" attribute can point to relevant website to find reports.
   - "history": this rarely ever gets populated fully and so tends to provide 
     a partial history of the data production chain, rendering it meaningless.
 - The "institution" global attribute will include the value: 
    "Met Office Hadley Centre (MOHC), FitzRoy Road, Exeter, Devon, EX1 3PB, UK."
 - The following global attributes have been added to the list:
   - "institution_id": short ID for the institution ("MOHC")
   - "contact": a common contact point (*need input from FF on this)
   - "creator_name": name of the person who created the data
   - "creator_email": e-mail address of the person who created the data
   - "creation_date": date/time formatted as "<YYYY-mm-dd HH:MM:SS>"
 - The "season_year" variable must now exist in all monthly data sets (to aid 
   data extraction using Iris).
 - The Example 25km gridded file now has the correct number of X and Y 
   coordinates. These should now match those provided to everyone by Fai.
 - In the naming-conventions the following changes have been made:
   - The frequency values in files/attributes should be "mon", "seas" and 
     "ann"
   - The frequency was previously included in *both* the "dataset_id" and 
     as a field in its own right in the file-name. It has been removed from 
     the "dataset_id" component to avoid duplication in file names.
   - "ukcp18" has been removed from the file names to shorten them.
 - The date range in the file names has now been fixed to use the full daily 
   range used to generate the files. E.g. 20201201-20211130
 - The monthly gridded monthly data (1 year per file) has been changed to span 
   from Dec-Nov: E.g. 20201201-20211130
 - Fixed typo where "dataset_id" was shown as "var_id" 



## Overview

This guidance should be considered as provisional. It has been written to help
the scientists generating NetCDF files for Land Strand 1 so that they can 
provide data suitable for the CEDA Archive and the UKCP User Interface tools.

It covers the following topics:

 1. Data structure inside each file
 2. Splitting datasets across multiple files
 3. File-naming conventions
 4. Directory-naming convention	
 5. Variable and coordinate variables
 6. Global attributes
 7. NetCDF properties
 8. The "season_year" coordinate variable
 9. Seasonal and annual files
 10. Bounds on coordinate variables

## 1. Data structure inside each file

There are two main file structures:
 1. 25km gridded data (on OSGB grid)
 2. spatially aggregated areas: admin regions, river basins, UK countries
 
The **25km gridded files** (1) should be defined against the following coordinate variables:
  - `(time, projection_y_coordinate, projection_x_coordinate, <probabilistic_coordinate>)`

The **spatially aggregated area files** (2) should be defined against the following coordinate variables:
  - `(time, region, <probabilistic_coordinate>)`

**NOTE:** `<probabilistic_coordinate>` is to be one of:
 - `sample`: 4000 values - used for sampled data
 - `percentile`: 113 values - used for the CDF and PDF data.

## 2. Splitting datasets across multiple files

There are three types of probabilistic data:
 - Sampled data
 - CDF data
 - PDF data
 
The data should be split into separate files along the following lines:
 - **main variable** (such as maximum temperature or precip)
 - **probabilistic data type**
 - **spatial representation** (which are 25km gridded, admin regions, river basins and uk countries)
 - **temporal frequency** (i.e. "mon", "seas", "ann")
 
The **25km gridded data** variables should be split across multiple files as follows [with approx size]:
 - monthly (*per year*)  			[~400MB]
 - seasonal (*per year*) 			[~125MB]
 - annual (*per year*)			 	[~42MB]

A monthly file will contain December of the first year to November of the next year.
A seasonal file will contain DJF, MAM, JJA, SON so the December will actually be pulled in from the previous year.
An annual file is generated from the seasonal data so it will in reality span from December (the year before) to November (in the year specified).
 
The **spatially aggregated area** data (i.e. admin regions, river basins, uk countries) [with approx size]:
 - monthly (*all time steps*)		[~400MB]
 - seasonal (*all time steps*)		[~125MB]
 - annual (*all time steps*)		 [~42MB]

## 3. File-naming convention

File names should follow the following convention:

 `<var_id>_<scenario>_<collection>_<domain>_<resolution>_<prob_data_type>_<baseline_period>_<time_slice_type>_<frequency>_<time_period>.nc`
 
Values for most of the components can be found in the UKCP18 Controlled Vocabularies at:
 - var_id: use the keys in the data structure under:
   - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_variable.json
   - NOTE: this vocabulary is not finalised yet
 - scenario: see: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_scenario.json
 - collection: "land-prob" (for all Land Strand 1 data)
 - domain: "uk" (for all Land Strand 1 data)
 - resolution: one of "25km", "country", "region", "river"
 - prob_data_type: see: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_prob_data_type.json
 - frequency: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_frequency.json 
 
## 4. Directory-naming convention	

On the CEDA Archive, the data will be stored in the following structure:

 `/badc/<project>/data/<collection>/<domain>/<resolution>/<scenario>/<prob_data_type>/<baseline_period>/<time_slice_type>/<var_id>/<frequency>/<version>/`
 
At the Met Office you could store it in a similar structure such as:

 `/project/<project>/data/<collection>/<domain>/<resolution>/<scenario>/<prob_data_type>/<baseline_period>/<time_slice_type>/<var_id>/<frequency>/<version>/`

Values for the components match those given above, except `<version>`.

`<version>` follows the CMIP5 format of `vYYYYMMDD` where "YYYYMMDD" is the date when the data was created (or published).

## 5. Variables and coordinate variables

Our evolving table of variables is here:

 https://docs.google.com/spreadsheets/d/1Ij3R3skvYhKnMSqXB6KHaxH0BSST5R0DI8zp2Qi82vw/edit#gid=762056270

Note that the variable ID (`var_id`) used in the file name must also be that used inside the file. This  
known as the `var_name` in Iris. E.g. you should use:
 - "tasmaxAnom" instead of "air_temperature".
 - "hussAnom" instead of "specific_humidity".

It is being honed and converted to this Controlled Vocabulary:

 https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_variable.json

The content includes both variable IDs and common variable metadata.

Note that the table separates out absolute values from anomaly values (which have variable IDs suffixed
with "Anom" and _may_ have different units).

A common set of variable attributes are specified but, depending on the spatial representation, there might 
be others that should be added. Please see the example files for the additional attributes.

Information about coordinate variables is held in a separate vocabulary at:

 https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_coordinate.json

Check units for "latitude" and "longitude" coordinates are correct.

Note that some of the attributes will reference coordinate variables that should also be included in the
data files. Here are some CDL examples...

### 5.1 Example 25km gridded file

```
$ ncdump -h tasAnom_a1b_land-prob_uk_25km_sample_b8100_1y_mon_20101201-20111130.nc

netcdf tasAnom_a1b_land-prob_uk_25km_sample_b8100_1y_mon_20101201-20111130 {
dimensions:
        time = UNLIMITED ; // (12 currently)
        bnds = 2 ;
        projection_y_coordinate = 52 ;
        projection_x_coordinate = 39 ;
        sample = 2000 ;
variables:
        double projection_y_coordinate_bnds(projection_y_coordinate, bnds) ;
        double projection_x_coordinate(projection_x_coordinate) ;
                projection_x_coordinate:units = "m" ;
                projection_x_coordinate:standard_name = "projection_x_coordinate" ;
                projection_x_coordinate:bounds = "projection_x_coordinate_bnds" ;
                projection_x_coordinate:axis = "X" ;
        double longitude(projection_y_coordinate, projection_x_coordinate) ;
                longitude:units = "degree_east" ;
                longitude:standard_name = "longitude" ;
        int sample(sample) ;
                sample:long_name = "sample" ;
        float tasAnom(time, projection_y_coordinate, projection_x_coordinate, sample) ;
                tasAnom:_FillValue = 1.e+20f ;
                tasAnom:anomaly_type = "absolute_change" ;
                tasAnom:grid_mapping = "transverse_mercator" ;
                tasAnom:description = "Mean air temperature",
                tasAnom:plot_label = "Mean air temperature anomaly at 1.5m (°c)",
                tasAnom:baseline_period = "1981-2000" ;
                tasAnom:coordinates = "latitude longitude season_year" ;
                tasAnom:long_name = "Anomaly of air temperature" ;
                tasAnom:standard_name = "air_temperature" ;
                tasAnom:units = "degC" ;
                tasAnom:label_units = "°c" ;
                tasAnom:cell_methods = "time: mean" ;
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 2010-01-15 00:00:00" ;
                time:calendar = "360_day" ;
                time:standard_name = "time" ;
                time:bounds = "time_bounds" ;
        double latitude(projection_y_coordinate, projection_x_coordinate) ;
                latitude:units = "degree_north" ;
                latitude:standard_name = "latitude" ;
        int transverse_mercator ;
                transverse_mercator:latitude_of_projection_origin = 49. ;
                transverse_mercator:semi_major_axis = 6377563.396 ;
                transverse_mercator:scale_factor_at_central_meridian = 0.9996012717 ;
                transverse_mercator:longitude_of_central_meridian = -2. ;
                transverse_mercator:false_northing = -100000. ;
                transverse_mercator:grid_mapping_name = "transverse_mercator" ;
                transverse_mercator:semi_minor_axis = 6356256.909 ;
                transverse_mercator:false_easting = 400000. ;
                transverse_mercator:longitude_of_prime_meridian = 0. ;
        double projection_x_coordinate_bnds(projection_x_coordinate, bnds) ;
        double projection_y_coordinate(projection_y_coordinate) ;
                projection_y_coordinate:units = "m" ;
                projection_y_coordinate:standard_name = "projection_y_coordinate" ;
                projection_y_coordinate:bounds = "projection_y_coordinate_bnds" ;
                projection_y_coordinate:axis = "Y" ;
        int season_year(time) ;
                season_year:units = "1" ;
                season_year:long_name = "season_year" ;


// global attributes:   ...NOT SHOWN HERE...
}

```

### 5.2 Example spatially aggregated area files

```
$ ncdump -v season_year tasAnom_a1b_land-prob_uk_region_sample_b8100_1y_mon_19601201-20991130.nc | more
netcdf tasAnom_a1b_land-prob_uk_region_sample_b8100_1y_mon_19601201-20991130 {
dimensions:
        region = 16 ;
        strlen = 21 ;
        time = UNLIMITED ; // (1668 currently)
        bnds = 2 ;
        sample = 2000 ;
variables:
        int sample(sample) ;
                sample:long_name = "sample" ;
        int season_year(time) ;
                season_year:units = "1" ;
                season_year:long_name = "season_year" ;
        float tasAnom(time, region, sample) ;
                tasAnom:anomaly_type = "absolute_change" ;
                tasAnom:description = "Mean air temperature",
                tasAnom:plot_label = "Mean air temperature anomaly at 1.5m (°c)",
                tasAnom:baseline_period = "1981-2000" ;
                tasAnom:coordinates = "geo_region season_year" ;
                tasAnom:long_name = "Anomaly of air temperature" ;
                tasAnom:standard_name = "air_temperature" ;
                tasAnom:units = "K" ;
                tasAnom:label_units = "°c" ;
                tasAnom:cell_methods = "time: mean" ;               
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 1960-12-15 00:00:00" ;
                time:long_name = "Time" ;
                time:calendar = "360_day" ;
                time:standard_name = "time" ;
                time:bounds = "time_bounds" ;
        char geo_region(region, strlen) ;
                geo_region:long_name = "Administrative Region" ;
                geo_region:standard_name = "region" ;

// global attributes: ...NOT SHOWN HERE...

data:

 geo_region =
  "west_scotland",
  "south_west_england",
  "isle_of_man",
  "east_of_england",
  "west_midlands",
  "northern_ireland",
  "yorkshire_and_humber",
  "east_scotland",
  "east_midlands",
  "north_east_england",
  "london",
  "north_west_england",
  "north_scotland",
  "wales",
  "channel_islands",
  "south_east_england" ;
}

```

The `geo_region:long_name` attribute should have one of the following values:
 - "Administrative Region"
 - "Country" 
 - "River Basin"
 
The possible values for `geo_region` are defined in the vocabularies:
 - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_admin_region.json
 - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_country.json
 - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_river_basin.json

### 5.3 Variable attributes

For each main variable, check that these attributes are set:
 - anomaly_type
 - description 
 - plot_label 
 - baseline_period
 - coordinates
 - long_name
 - standard_name
 - units 
 - label_units 
 - cell_methods  
 - Refer to here for the correct contents:
   https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_variable.json#L1592 
	 
Additionally, if the data is on the OSGB grid:
 - _FillValue = 1.e+20f
 - grid_mapping = "transverse_mercator"

## 6. Global attributes

The global attributes for the project are categorised as either:
 - Mandatory
 - Recommended
 
### 6.1 Global attributes

The following global attributes are mandatory:

 - baseline_period: "1981-2000"
 - collection: "land-prob"
 - contact: "ukcpproject@metoffice.gov.uk"
 - Conventions: "CF-1.5"
 - creation_date: formatted as: "YYYY-MM-DDThh:mm:ss"
 - domain: "uk"
 - frequency: `<frequency>`
 - institution: use: "Met Office Hadley Centre (MOHC), FitzRoy Road, Exeter, Devon, EX1 3PB, UK."
 - institution_id: use: "MOHC"
 - prob_data_type: `<prob_data_type>`
 - project: use: "UKCP18"
 - references: Published or web-based references that describe the data or methods used to produce it.
 - resolution: `<resolution>`
 - scenario: `<scenario>`
 - source: The method of production of the original data. If it was model-generated, source should name the model and its version, as specifically as could be useful.
 - time_slice_type: `<time_slice_type>`
 - title: A succinct description of what is in the dataset.
 - version: `v<YYYYMMDD>` - where the date (`<YYYYMMDD>`) is an agreed date set the same for ALL files in this data set.
 
Additionally, you can add more global attributes as you wish.

### 6.2 Global attributes to REMOVE/AVOID

Please AVOID setting the following global attributes:

 - variable
 - STASH

## 7. NetCDF properties

### 7.1 Compression

Do not use any compression options when writing NetCDF files. The "load" operation needs to be as 
fast as possible when opened by the User Interface. By using a single-precision (float32) for the 
main variable the volumes will be reduced significantly.

### 7.2 NetCDF version

Use the "NetCDF 4 Classic" format. You can check this using `ncdump -k`:

```
$ ncdump -k tasAnom_rcp85_ukcp18-land-prob-uk-25km-all_percentile_mon_20010115-20011215.nc
netCDF-4 classic model
```

### 7.3 The `_FillValue` attribute 

The `_FillValue` attribute should *always* be:  1.e+20f

## 8. The "season_year" coordinate variable

The "season_year" coordinate variable must now exist in all monthly data sets 
(to aid data extraction using Iris). It should look like:

*Metadata:*

```
        int season_year(time) ;
                season_year:units = "1" ;
                season_year:long_name = "season_year" ;
```

It will also be in listed in the "coordinates" attribute string of the main 
variable in the file, e.g:

```
                tasAnom:coordinates = "geo_region season_year" ;
```

*Data:*

```
 season_year = 1961, 1961, 1961, 1961, 1961, 1961, 1961, 1961, 1961, 1961,
               1961, 1961 ;
```
 

## 9. Seasonal and annual files

More information will be provided regarding the formatting of seasonal and annual files and
the specific attributes that are relevant.

This is likely to include additional coordinate variables such as:

```
    char clim_season(time, string64) ;
        clim_season:units = "no_unit" ;
        clim_season:long_name = "clim_season" ;

	int64 season_year(time) ;
        season_year:units = "1" ;
        season_year:long_name = "season_year" ;
```

## 10. Bounds on coordinate variables

The following coordinates should include a `bounds` attribute that points to a 
separate bounds variable in the file, called either "<coord_var_id>_bounds" or
"<coord_var_id>_bnds":
 - time
 - latitude - when it is a direct coordinate of the main variable
 - longitude - when it is a direct coordinate of the main variable
 - projection_y_coordinate
 - projection_x_coordinate
