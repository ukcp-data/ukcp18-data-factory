
# Guidance on construction of UKCP Land Strand 2 simulations

## Change log

### Changes on 2018-03-21

 - Added "creation_date" global attribute
 - Added section on "bounds" for coordinate variables

### Changes on 2018-03-06

 - First version

## Overview

This guidance should be considered as provisional. It has been written to help
the scientists generating NetCDF files for Land Strand 2 so that they can 
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
 10. Climatology files
 11. Bounds on coordinate variables

## 1. Data structure inside each file

There are 3 main file structures:
 1. 60km gridded global data (on regular latitude/longitude grid)
 2. 60km gridded UK data (on OSGB grid)
 3. spatially aggregated areas: admin regions, river basins, UK countries
 
The **60km gridded global files** (1) should be defined against the following coordinate variables:
  - `(ensemble_member, time, latitude, longitude)`

The **60km gridded UK files** (2) should be defined against the following coordinate variables:
  - `(ensemble_member, time, projection_y_coordinate, projection_x_coordinate)`
  
The **spatially aggregated area files** (3) should be defined against the following coordinate variables:
  - `(ensemble_member, time, region)`

## 2. Splitting datasets across multiple files

The **60km gridded global files** (1) should be split by:
 - main variable (such as "tas")
 - scenario (only RCP85 at present)
 - ensemble member 
 - temporal frequency (i.e. "mon", "seas", "ann")

The **60km gridded UK files** (2) should be split by:
 - main variable (such as "tas")
 - scenario (only RCP85 at present)
 - ensemble member 
 - temporal frequency (i.e. "mon", "seas", "ann")
  
The **spatially aggregated area files** (3) should be split by:
 - main variable (such as "tas")
 - scenario (only RCP85 at present)
 - ensemble member 
 - temporal frequency (i.e. "mon", "seas", "ann")
 - spatial representation (which are admin regions, river basins and uk countries)

The time-steps should be grouped as follows:

 i. **60km gridded global files:**
 - monthly (*entire time series in one file*)	[~1.4GB]
 - seasonal (*entire time series in one file*)	[~350MB]
 - annual (*entire time series in one file*)	[~116MB]

 ii. **60km gridded UK files:**
 - monthly (*entire time series in one file*)	[~12MB]
 - seasonal (*entire time series in one file*)	[~3MB]
 - annual (*entire time series in one file*)	[~1MB]
 
 iii. **spatially aggregated area files:**
 - monthly (*entire time series in one file*)	[~1MB]
 - seasonal (*per year*) 			[~0.25MB]
 - annual (*per year*)			 	[~0.1MB]

## 3. File-naming convention

File names should follow the following convention:

 `<var_id>_<scenario>_<collection>_<domain>_<resolution>_<ensemble_member>_<frequency>_<time_period>.nc`
 
Values for most of the components can be found in the UKCP18 Controlled Vocabularies at:
 - var_id: use the keys in the data structure under:
   - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_variable.json
   - NOTE: this vocabulary is not finalised yet
 - scenario: as above
 - collection: "land-gcm" (for all Land Strand 2 data)
 - domain: "uk" (for all Land Strand 1 data)
 - resolution: one of "country", "region", "river"
 - scenario: see: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_scenario.json
 - prob_data_type: see: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_prob_data_type.json
 - frequency: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_frequency.json 
	
## 4. Directory-naming convention	

On the CEDA Archive, the data will be stored in the following structure:

 `/badc/<project>/data/<collection>/<domain>/<resolution>/<scenario>/<ensemble_member>/<var_id>/<frequency>/<version>/`
 
At the Met Office you could store it in a similar structure such as:

 `/project/<project>/data/<collection>/<domain>/<resolution>/<scenario>/<ensemble_member>/<var_id>/<frequency>/<version>/`

Values for the components match those given above, except `<version>`.

`<version>` follows the CMIP5 format of `vYYYYMMDD` where "YYYYMMDD" is the date when the data was created (or published).

## 5. Variables and coordinate variables

Our evolving table of variables is here:

 https://docs.google.com/spreadsheets/d/1Ij3R3skvYhKnMSqXB6KHaxH0BSST5R0DI8zp2Qi82vw/edit#gid=762056270

It is being honed and converted to this Controlled Vocabulary:

 https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_variable.json 

The content includes both variable IDs and common variable metadata.

Note that the table separates out absolute values from anomaly values (which have variable IDs suffixed
with "Anom" and _may_ have different units).

**Land Strand 2 will deliver only absolute values rather than anomalies.** (The User
Interface will generate anomalies by subtracting the climatologies from the absolute
values).

A common set of variable attributes are specified but, depending on the spatial representation, there might 
be others that should be added. Please see the example files for the additional attributes.

Information about coordinate variables is held in a separate vocabulary at:

 https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_coordinate.json

Note that some of the attributes will reference coordinate variables that should also be included in the
data files. Here are some CDL examples.

### 5.1 Example 60km gridded global file (on regular latitude/longitude grid)

```
netcdf tas_rcp85_land-gcm_global_60km_r001i1p00000_mon_19001201-20991130 {
dimensions:
        time = UNLIMITED ; // (2376 currently)
        bnds = 2 ;
        ensemble_member = 1 ;
        latitude = 324 ;
        longitude = 432 ;
variables:
        float latitude(latitude) ;
                latitude:units = "degrees_north" ;
                latitude:long_name = "Latitude" ;
                latitude:standard_name = "latitude" ;
                latitude:axis = "Y" ;
        float ensemble_member(ensemble_member) ;
                ensemble_member:units = "" ;
                ensemble_member:long_name = "Ensemble member" ;
        float tas(ensemble_member, time, latitude, longitude) ;
                tas:_FillValue = 1.e+20f ;
                tas:units = "K" ;
                tas:long_name = "air temperature" ;
                tas:standard_name = "air_temperature" ;
                tas:anomaly_type = "none" ;
        float longitude(longitude) ;
                longitude:units = "degrees_east" ;
                longitude:long_name = "Longitude" ;
                longitude:standard_name = "longitude" ;
                longitude:axis = "X" ;
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 2010-12-15 00:00:00" ;
                time:long_name = "Time" ;
                time:calendar = "360_day" ;
                time:standard_name = "time" ;
                time:bounds = "time_bounds" ;
```

### 5.2 Example  2. 60km gridded UK data (on OSGB grid)

```
netcdf tas_rcp85_land-gcm_uk_60km_r001i1p00000_mon_19001201-20991130 {
dimensions:
        ensemble_member = 1 ;
        time = UNLIMITED ; // (2376 currently)
        bnds = 2 ;
        projection_y_coordinate = 25 ;
        projection_x_coordinate = 15 ;
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
        int season_year(time) ;
                season_year:units = "1" ;
                season_year:long_name = "season_year" ;
        float tas(ensemble_member, time, projection_y_coordinate, projection_x_coordinate) ;
                tas:_FillValue = 1.e+20f ;
                tas:grid_mapping = "transverse_mercator" ;
                tas:coordinates = "latitude longitude season_year" ;
                tas:long_name = "air temperature" ;
                tas:standard_name = "air_temperature" ;
                tas:units = "K" ;
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 1901-12-15 00:00:00" ;
                time:long_name = "Time" ;
                time:calendar = "360_day" ;
                time:standard_name = "time" ;
                time:bounds = "time_bounds" ;
        double latitude(projection_y_coordinate, projection_x_coordinate) ;
                latitude:units = "degree_north" ;
                latitude:standard_name = "latitude" ;
        float ensemble_member(ensemble_member) ;
                ensemble_member:units = "" ;
                ensemble_member:long_name = "Ensemble member" ;
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
```

The `geo_region:long_name` attribute should have one of the following values:
 - "Administrative Region"
 - "Country"
 - "River Basin"
 
The possible values for `geo_region` are defined in the vocabularies:
 - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_admin_region.json
 - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_country.json
 - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_river_basin.json

### 5.3 Example spatially aggregated area files: admin regions, river basins, UK countries

```
netcdf tas_rcp85_land-gcm_uk_river_r001i1p00000_mon_19001201-20991130 {
dimensions:
        ensemble_member = 1 ;
        region = 26 ;
        strlen = 21 ;
        time = UNLIMITED ; // (2376 currently)
        bnds = 2 ;
variables:
        float ensemble_member(ensemble_member) ;
                ensemble_member:units = "" ;
                ensemble_member:long_name = "Ensemble member" ;
        float tas(ensemble_member, time, region) ;
                tas:_FillValue = 1.e+20f ;
                tas:units = "K" ;
                tas:long_name = "air temperature" ;
                tas:standard_name = "air_temperature" ;
                tas:coordinates = "geo_region season_year" ;
        char geo_region(region, strlen) ;
                geo_region:long_name = "River basin" ;
                geo_region:standard_name = "region" ;
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 1901-12-15 00:00:00" ;
                time:calendar = "360_day" ;
                time:standard_name = "time" ;
                time:bounds = "time_bounds" ;
```

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
 - domain: "uk" or "global"
 - ensemble_member: <ensemble_member>
 - frequency: <frequency>
 - institution: use: "Met Office Hadley Centre (MOHC), FitzRoy Road, Exeter, Devon, EX1 3PB, UK."
 - institution_id: use: "MOHC"
 - project: use: "UKCP18"
 - references: Published or web-based references that describe the data or methods used to produce it.
 - resolution: <resolution>
 - scenario: <scenario>
 - source: The method of production of the original data. If it was model-generated, source should name the model and its version, as specifically as could be useful.
 - title: A succinct description of what is in the dataset.
 - version: "v<YYYYMMDD>" - where the date ("<YYYYMMDD>") is an agreed date set the same for ALL files in this data set.

## 7. NetCDF properties

### 7.1 Compression

Do not use any compression options when writing NetCDF files. The "load" operation needs to be as 
fast as possible when opened by the User Interface. By using a single-precision (float32) for the 
main variable the volumes will be reduced significantly.

### 7.2 NetCDF version

Use the "NetCDF 4 Classic" format. You can check this using `ncdump -k`:

```
$ ncdump -k tas_rcp85_land-gcm_uk_river_r001i1p00000_mon_19011215-20991115.nc
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
               1961, 1961, 1962, 1962, ...... ;
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

## 10. Climatology files

More information to be provided for the plans for climatology files.

## 11. Bounds on coordinate variables

The following coordinates should include a `bounds` attribute that points to a 
separate bounds variable in the file, called either "<coord_var_id>_bounds" or
"<coord_var_id>_bnds":
 - time
 - latitude - when it is a direct coordinate of the main variable
 - longitude - when it is a direct coordinate of the main variable
 - projection_y_coordinate
 - projection_x_coordinate