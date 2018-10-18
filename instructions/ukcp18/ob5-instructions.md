# Guidance on construction of UKCP Observations Strand datasets

## Change log

### Changes on 2018-10-17

 - First version

## Overview

This guidance should be considered as provisional. It has been written to help
the scientists generating NetCDF files for the Observations Strand of UKCP18
so that they can provide data suitable for the CEDA Archive.

It covers the following topics:

 1. Overview and catalogue
 2. Data structure inside each file
 3. Splitting datasets across multiple files
 4. File-naming conventions
 5. Directory-naming convention	
 6. Variable and coordinate variables
 7. Global attributes
 8. NetCDF properties
 9. Bounds on coordinate variables

## 1. Overview and catalogue

There are two main file structures:
 1. Gridded data (on OSGB grid): 60km
 2. Gridded data (on OSGB grid): 25km
 3. Gridded data (on OSGB grid): 12km
 4. Gridded data (on OSGB grid): 2.2km
 5. Admin regions
 6. River basins
 7. UK countries
 
Each of the above will be represented in a single "Dataset" record in the CEDA catalogue. 

Each record will include all time frequencies:
 1. Daily: only a subset of variables
 2. Monthly: all variables
 3. Seasonal: all variables
 4. Annual: all variables

Additionally, we categorise the climatologies as having "extra" frequencies:
 5. Monthly climatologies: all variables
 6. Seasonal climatologies: all variables
 7. Annual climatologies: all variables

## 2. Data structure inside each file
 
The **gridded files** (1) should be defined against the following coordinate variables:
  - `(time, projection_y_coordinate, projection_x_coordinate)`

The **spatially aggregated area files** (2) should be defined against the following coordinate variables:
  - `(time, region)`
  
## 3. Splitting datasets across multiple files

There are 4 temporal frequencies:
  
The data should be split into separate files along the following lines:
 - **main variable** (such as maximum temperature or precip)
 - **spatial representation**
 - **temporal frequency** (i.e. "mon", "seas", "ann", "day", "mon-clim", "seas-clim", "ann-clim")
 
The **gridded data** variables should be split across multiple files as follows:
 - split into individual years: e.g. 201201-201212
 
The **spatially aggregated area** data should be:
 - all time steps in a single file: e.g. 189101-201612

## 4. File-naming convention

File names should follow the following convention:

 `<var_id>_<collection>_<domain>_<resolution>_<frequency>_<time_period>.nc`
 
Values for most of the components can be found in the UKCP18 Controlled Vocabularies at:
 - var_id: use the keys in the data structure under:
   - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_variable.json
 - collection: "land-obs"
 - domain: "uk" (for all Land Strand 1 data)
 - resolution: one of "60km", "25km", "12km", "2km", "country", "region", "river"
 - frequency: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_frequency.json 
 - time_period: format depends on "frequency" as follows:
   - day: YYYYMMDD-YYYYMMDD
   - mon: YYYYMM-YYYYMM
   - seas: YYYYMM-YYYYMM
   - ann: YYYY-YYYY (or YYYY if only one year)

NOTE: the climatological period is represented simply in the `<time_period>` component of the file, 
e.g. "19610101-1991231" 

An example file name would be:

 `tasmin_land-obs_uk_25km_mon_201001-201012.nc`
 
## 5. Directory-naming convention	

On the CEDA Archive, the data will be stored in the following structure:

 `/badc/<project>/data/<collection>/<domain>/<resolution>/<var_id>/<frequency>/<version>/`
 
At the Met Office you could store it in a similar structure such as:

 `/project/<project>/data/<collection>/<domain>/<resolution>/<var_id>/<frequency>/<version>/`

Values for the components match those given above, except `<version>`.

`<version>` follows the CMIP5 format of `vYYYYMMDD` where "YYYYMMDD" is the date when the data was created (or published).

An example directory would be:

 `/badc/ukcp18/data/land-obs/uk/25km/tasmin/mon/v20181101/`

## 6. Variables and coordinate variables

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

### 6.1 Example 25km gridded file

```
$ ncdump -h tasmin_land-obs_uk_25km_mon_201001-201012.nc

netcdf tasmin_land-obs_uk_25km_mon_201001-201012 {
dimensions:
        time = UNLIMITED ; // (12 currently)
        bnds = 2 ;
        projection_y_coordinate = 52 ;
        projection_x_coordinate = 39 ;
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
        float tasmin(time, projection_y_coordinate, projection_x_coordinate) ;
                tasmin:_FillValue = 1.e+20f ;
                tasmin:grid_mapping = "transverse_mercator" ;
                tasmin:description = "Minimum air temperature",
                tasmin:plot_label = "Minimum air temperature at 1.5m (°c)",
                tasmin:coordinates = "latitude longitude" ;
                tasmin:long_name = "Minimum air temperature" ;
                tasmin:standard_name = "air_temperature" ;
                tasmin:units = "degC" ;
                tasmin:label_units = "°c" ;
                tasmin:cell_methods = "time: mean" ;
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 1961-01-01 00:00:00" ;
                time:calendar = "standard" ;             
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


// global attributes:   ...NOT SHOWN HERE...
}

```

### 6.2 Example spatially aggregated area files

```
$ ncdump -v tasmin_land-obs_uk_region_mon_201001-201012.nc
netcdf tasmin_land-obs_uk_region_mon_201001-201012 {
dimensions:
        region = 16 ;
        strlen = 21 ;
        time = UNLIMITED ; // (12 currently)
        bnds = 2 ;
variables:
        float tasmin(time, region) ;
                tasmin:description = "Minimum air temperature",
                tasmin:plot_label = "Minimum air temperature at 1.5m (°c)",
                tasmin:coordinates = "geo_region" ;
                tasmin:long_name = "Minimum air temperature" ;
                tasmin:standard_name = "air_temperature" ;
                tasmin:units = "degC" ;
                tasmin:label_units = "°c" ;
                tasmin:cell_methods = "time: mean" ;               
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 1960-01-01 00:00:00" ;
                time:long_name = "Time" ;
                time:calendar = "standard" ;
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

### 6.3 Variable attributes

For each main variable, check that these attributes are set:
 - description 
 - plot_label 
 - coordinates
 - long_name
 - standard_name
 - units 
 - label_units 
 - cell_methods  
 - Refer to here for the correct contents:
   https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_CVs/UKCP18_variable.json
	 
Additionally, if the data is on the OSGB grid:
 - _FillValue = 1.e+20f
 - grid_mapping = "transverse_mercator"

## 7. Global attributes

The global attributes for the project are categorised as either:
 - Mandatory
 - Recommended
 
### 7.1 Global attributes

The following global attributes are mandatory:

 - collection: "land-obs"
 - contact: "ukcpproject@metoffice.gov.uk"
 - Conventions: "CF-1.5"
 - creation_date: formatted as: "YYYY-MM-DDThh:mm:ss"
 - domain: "uk"
 - frequency: `<frequency>`
 - institution: use: "Met Office Hadley Centre (MOHC), FitzRoy Road, Exeter, Devon, EX1 3PB, UK."
 - institution_id: "MOHC"
 - prob_data_type: `<prob_data_type>`
 - project: "UKCP18"
 - references: Published or web-based references that describe the data or methods used to produce it.
 - resolution: `<resolution>`
 - source: The method of production of the original data. If it was model-generated, source should name the model and its version, as specifically as could be useful.
 - title: A succinct description of what is in the dataset.
 - version: `v<YYYYMMDD>` - where the date (`<YYYYMMDD>`) is an agreed date set the same for ALL files in this data set.
 
Additionally, you can add more global attributes as you wish.

### 7.2 Global attributes to REMOVE/AVOID

Please AVOID setting the following global attributes:

 - variable
 - STASH

## 8. NetCDF properties

### 8.1 Compression

Do **not** use any compression options when writing NetCDF files. The "load" operation needs to be as 
fast as possible when opened by the User Interface. By using a single-precision (float32) for the 
main variable the volumes will be reduced significantly.

### 8.2 NetCDF version

Use the "NetCDF 4 Classic" format. You can check this using `ncdump -k`:

```
$ ncdump -k tasAnom_rcp85_ukcp18-land-prob-uk-25km-all_percentile_mon_20010115-20011215.nc
netCDF-4 classic model
```

### 8.3 The `_FillValue` attribute 

The `_FillValue` attribute should *always* be:  1.e+20f

## 9. Bounds on coordinate variables

The following coordinates should include a `bounds` attribute that points to a 
separate bounds variable in the file, called either "<coord_var_id>_bounds" or
"<coord_var_id>_bnds":
 - time
 - latitude - when it is a direct coordinate of the main variable
 - longitude - when it is a direct coordinate of the main variable
 - projection_y_coordinate
 - projection_x_coordinate