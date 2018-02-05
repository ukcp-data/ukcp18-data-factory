# Guidance on construction of UKCP Land Strand 1 probabilistic datasets

## Overview

This guidance should be considered as provisional. It has been written to help
the scientists generating NetCDF files for Land Strand 1 so that they can 
provide data suitable for the CEDA Archive and the UKCP User Interface tools.

It covers the following topics:

 1. Data structure inside each file
 2. Splitting datasets across multiple files
 3. File-naming conventions
 4. Directory-naming convention	
 5. Variable and coordinate variable IDs
 6. Variable attributes
 7. Global attributes
 8. NetCDF properties
 
## 1. Data structure inside each file

There are two main file structures:
 1. 25km gridded data (on OSGB grid)
 2. spatially aggregated areas: admin regions, river basins, UK countries
 
The 25km gridded files (1) should be defined against the following coordinate variables:
  - `(time, projection_y_coordinate, projection_x_coordinate, <probabilistic_coordinate>)`

The spatially aggregated area files (2) should be defined against the following coordinate variables:
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
 - **temporal frequency** (i.e. "monthly", "seasonal", "annual")
 
The 25km gridded data variable should be split across multiple files as follows [with approx size]:
 - monthly (per year)  			[~400MB]
 - seasonal (per year) 			[~125MB]
 - annual (per year)			 [~42MB]

A monthly file will contain January to December of the given year.
A seasonal file will contain DJF, MAM, JJA, SON so the December will actually be pulled in from the previous year.
An annual file is generated from the seasonal data so it will in reality span from December (the year before) to November (in the year specified).
 
The spatially aggregated area data (i.e. admin regions, river basins, uk countries) [with approx size]:
 - monthly (all time steps)		[~400MB]
 - seasonal (all time steps)	[~125MB]
 - annual (all time steps)		 [~42MB]

## 3. File-naming convention

File names should follow the following convention:

 `<var_id>_<scenario>_<dataset_id>_<prob_data_type>_<frequency>_<time_period>.nc`
 
Values for most of the components can be found in the UKCP18 Controlled Vocabularies at:
 - var_id: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_variable.json (***needs an update)
     - FROM:  https://docs.google.com/spreadsheets/d/1Ij3R3skvYhKnMSqXB6KHaxH0BSST5R0DI8zp2Qi82vw/edit#gid=762056270
 - scenario: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_scenario.json
 - prob_data_type: one of "sample", "cdf", "pdf"
 - frequency: https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_frequency.json (***needs an update)
 
The `dataset_id` is constructed as follows:

 `<project>-<collection>-<domain>-<resolution>-<frequency>`
 
Values for those components will use the following vocabularies:
 - project: "ukcp18" (always)
 - scenario: as above
 - collection: "land-prob" (for all Land Strand 1 data)
 - domain: "uk" (for all Land Strand 1 data)
 - resolution: one of "25km", "country", "region", "river"
 - frequency: as above	
	
## 4. Directory-naming convention	

On the CEDA Archive, the data will be stored in the following structure:

 `/badc/<project>/data/<collection>/<domain>/<resolution>/<scenario>/<prob_data_type>/<var_id>/<frequency>/<version>/`
 
At the Met Office you could store it in a similar structure such as:

 `/project/<project>/data/<collection>/<domain>/<resolution>/<scenario>/<prob_data_type>/<var_id>/<frequency>/<version>/`

Values for the components match those given above, except `<version>`.

`<version>` follows the CMIP5 format of `vYYYYMMDD` where "YYYYMMDD" is the date when the data was created (or published).

## 5. Variables and coordinate variables

Our evolving table of variables is here:

 https://docs.google.com/spreadsheets/d/1Ij3R3skvYhKnMSqXB6KHaxH0BSST5R0DI8zp2Qi82vw/edit#gid=762056270

It is being honed and converted to this Controlled Vocabulary:

 https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_variable.json (***needs an update)

The content includes both variable IDs and common variable metadata.

Note that the table separates out absolute values from anomaly values (which have variable IDs suffixed
with "Anom" and _may_ have different units).

A common set of variable attributes are specified but, depending on the spatial representation, there might 
be others that should be added. Please see the example files for the additional attributes.

Note that some of the attributes will reference coordinate variables that should also be included in the
data files. Here are some CDL examples:

### 7.1 25km gridded file

```
$ ncdump -h tasAnom_a1b_ukcp18-land-prob-uk-25km-all_sample_mon_20100115-20101215.nc

netcdf tasAnom_a1b_ukcp18-land-prob-uk-25km-all_sample_mon_20100115-20101215 {
dimensions:
        time = 12 ;
        bnds = 2 ;
        projection_y_coordinate = 58 ;
        projection_x_coordinate = 36 ;
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
                tasAnom:description = "Surface temperature anomaly at 1.5m (°c)" ;
                tasAnom:baseline_period = "1981-2000" ;
                tasAnom:coordinates = "latitude longitude" ;
                tasAnom:long_name = "Anomaly of air temperature" ;
                tasAnom:standard_name = "air_temperature" ;
                tasAnom:units = "K" ;
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

// global attributes:
                :domain = "uk" ;
                :scenario = "a1b" ;
                :var_id = "tasAnom" ;
                :collection = "land-prob" ;
                :Conventions = "CF-1.6" ;
                :project = "ukcp18" ;
                :version = "v20170331" ;
                :frequency = "mon" ;
                :dataset_id = "ukcp18-land-prob-uk-25km-all" ;
                :resolution = "25km" ;
                :prob_data_type = "sample" ;
}

```

### 7.2 Spatially aggregated area files

```
$ ncdump -v geo_region tasAnom_a1b_ukcp18-land-prob-uk-region-all_sample_mon_19591215-20991115.nc

netcdf tasAnom_a1b_ukcp18-land-prob-uk-region-all_sample_mon_19591215-20991115 {
dimensions:
        region = 16 ;
        strlen = 21 ;
        time = UNLIMITED ; // (1680 currently)
        bnds = 2 ;
        sample = 2000 ;
variables:
        int sample(sample) ;
                sample:long_name = "sample" ;
        float tasAnom(time, region, sample) ;
                tasAnom:_FillValue = 1.e+20f ;
                tasAnom:anomaly_type = "absolute_change" ;
                tasAnom:description = "Surface temperature anomaly at 1.5m (°c)" ;
                tasAnom:coordinates = "geo_region" ;
                tasAnom:long_name = "Anomaly of air temperature" ;
                tasAnom:standard_name = "air_temperature" ;
                tasAnom:units = "K" ;
        char geo_region(region, strlen) ;
                geo_region:long_name = "Administrative Region" ;
                geo_region:standard_name = "region" ;
        double time_bounds(time, bnds) ;
        float time(time) ;
                time:units = "days since 1961-01-15 00:00:00" ;
                time:long_name = "Time" ;
                time:calendar = "360_day" ;
                time:standard_name = "time" ;
                time:bounds = "time_bounds" ;

// global attributes:
                :domain = "uk" ;
                :scenario = "a1b" ;
                :var_id = "tasAnom" ;
                :collection = "land-prob" ;
                :Conventions = "CF-1.6" ;
                :project = "ukcp18" ;
                :version = "v20180109" ;
                :frequency = "mon" ;
                :dataset_id = "ukcp18-land-prob-uk-region-all" ;
                :resolution = "region" ;
                :prob_data_type = "sample" ;
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

## 7. Global attributes

The recommended global 
 
 - Global attributes:
  - Mandatory:
   - title: A succinct description of what is in the dataset.
   - institution: use "Met Office Hadley Centre (MOHC), FitzRoy Road, Exeter, Devon, EX1 3PB, UK."
   - source: The method of production of the original data. If it was model-generated, source should name the model and its version, as specifically as could be useful.
   - history: History of major processing, with each component as "YYYY-MM-DD hh:mm:ss: <description_of_processing>\n"
   - references: Published or web-based references that describe the data or methods used to produce it.

The following global attribute set is currently recommended:

                :Conventions = "CF-1.7" ;  *** OR "1.6"
                :domain = "uk" ;
                :scenario = "a1b" ;
                :var_id = "prAnom" ;
                :collection = "land-prob" ;
                :project = "ukcp18" ;
                :version = "v20180109" ;
                :frequency = "mon" ;
                :dataset_id = "ukcp18-land-prob-uk-region-all" ;
                :resolution = "region" ;
                :prob_data_type = "sample" ;

source
institution
references etc
// global attributes:
		:baseline = "1981-2000" ;
		:institution = "Met Office Hadley Centre" ;
		:meaning_period = "djf" ;
		:references = "Murphy, J.M., B. B. B. Booth, M. Collins, G. R. Harris, D. M. H. Sexton 
                               and M. J. Webb, 2007: A methodology for probabilistic predictions of 
                               regional climate change from perturbed physics ensembles. Phil. Trans. 
                               R. Soc. A, 365, 1993-2028" ;
		:report = "Yet to be identified..." ;
		:scenario = "RCP85" ;
		:source = "Probabilistic climate prediction based on family of Met Office Hadley Centre 
                           climate models HadCM3, HadRM3 and HadSM3, plus climate models from other 
                           climate centres contributing to IPCC AR5 and CFMIP." ;
		:title = "Change in DJF mean surface air temperature relative to 1981-2000 for RCP85" ;
		:variable = "tas" ;
		:Conventions = "CF-1.5" ;


## 8. NetCDF properties

### 8.1 Compression

Do not use any compression options when writing NetCDF files. The "load" operation needs to be as 
fast as possible when opened by the User Interface. By using a single-precision (float32) for the 
main variable the volumes will be reduced significantly.

### 8.2 NetCDF version

Use the "NetCDF 4 Classic" format. You can check this using `ncdump -k`:

```
$ ncdump -k tasAnom_rcp85_ukcp18-land-prob-uk-25km-all_percentile_mon_20010115-20011215.nc
netCDF-4 classic model
```
