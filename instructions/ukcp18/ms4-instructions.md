# Guidance on construction of UKCP Marine Strand datasets

## Change log

### Changes on 2018-03-14

 - Updated "project" global attribute
 - Updated file-naming convention
 - Removed "dataset_id" global attribute

### Changes on 2018-03-07

 - First version
 
### Changes on 2018-03-13

 - Removed/revoked section specifying direction of latitude values
 - Removed "prob_data_type" global attribute

### Questions/issues

 1. Please can you provide a list of names (strings) for the coordinate variables so that
    we can put them in the netCDF files as string arrays:
   - model
   - event
   - scenario
   - mean_sea_level_change (5 values)
   - mean_sea_level_change (21 values)
   - percentile
   - estimate
   - return_period
   - return_level
 2. Please check the variables and coordinates listed in section 1
   - are they correct? 

## Overview

This guidance should be considered as provisional. It has been written to help
the scientists generating NetCDF files for the Marine Strand so that they can 
provide data suitable for the CEDA Archive and the UKCP User Interface tools.

It covers the following topics:

 1. Data structures inside each file
 2. Sizes and split across files
 3. File-naming conventions
 4. Directory-naming convention	
 5. Variable and coordinate variables
 6. Global attributes
 7. NetCDF properties

## 1. Data structures inside each file

There are a number of different file structures relating to the different Marine Strand products. In
this section we refer to the products using the codes defined in the CEDA Datasets spreadsheet 
(https://docs.google.com/spreadsheets/d/1oNmJAYLGt6UrenY8XH_4gTyZGlFVW9plgyK75L3BN0Y/edit#gid=1180832079):

 - MS4.01	UKCP18 Historical Simulations of Gridded Sea Surface Elevation around the UK from 1950-2006
 - MS4.02	UKCP18 Future Simulations of Gridded Sea Surface Elevation around the UK from 2007-2100
 - MS4.03	UKCP18 Short Event Case Studies of Historical and Future Sea Surface Elevation around the UK
 - MS4.04	UKCP18 Simulated Impact of Mean Sea Level Change on Tidal Characteristics around the UK
 - MS4.05	UKCP18 Time-series Analyses of Sea Surface Elevation around the UK for 2007-2100
 - MS4.06	UKCP18 Spatially continuous Time-mean Sea Level Projections around the UK for 2007-2100
 - MS4.07	Mean Sea Level	at selected tide gauge locations since 1950 - NOT CONFIRMED
 - MS4.08	UKCP18 Time-mean Sea Level Projections  at selected tide gauge locations for 2007-2300
 - MS4.09	UKCP18 projected future extreme still water level at selected tide gauge locations for 2020, 2050 and 2100

### MS4.01

Variables: 
 - tideAnom
 - tideSurgeAnom

Coordinates of main variables:
  - `time(3600), model(5), latitude(135), longitude(150)` 

### MS4.02	

Variables: 
 - as MS4.01
 
Coordinates of main variables:
  - `time(2232), model(5), latitude(135), longitude(150)` - less years than MS4.01

### MS4.03	

Variables: 
 - as MS4.01
 
Coordinates of main variables:
  - `time(1680), event(3), mean_sea_level_change(5), latitude(135), longitude(150)` - less years than MS4.01

### MS4.04	

Variables: 
 - tideAnom

Coordinates of main variables:
  - `time(672), mean_sea_level_change(21), latitude(135), longitude(150)` 
  
### MS4.05	
	
Variables: 
 - ???

Coordinates of main variables:
  - `time(1), model(5), latitude(135), longitude(150)` 	

### MS4.06	
	
Variables: 
 - sseAnom

Coordinates of main variables:
  - `time(94), scenario(3), percentile(3), latitude(135), longitude(150)` 
  
### MS4.07???
	
???

### MS4.08	

Variables: 
 - sseAnom

Coordinates of main variables:
  - `time(294), scenario(3), percentile(3), latitude(135), longitude(150)` 


### MS4.09	
 
Variables: 
 - stillWaterReturnLevel

Coordinates of main variables:
  - `time(3), estimate(3), return_period(16), return_level(16), latitude(135), longitude(150)` 

## 2. Sizes and split across files

The estimated sizes of each data set and file are:

 - MS4.01: 2,781MB	(278MB) - split by variable(2) and model(5)
 - MS4.02: 1,724MB	(172MB) - split by variable(2) and model(5)
 - MS4.03: 3,893MB	(1,298MB) - split by variable(2) and event(3)
 - MS4.04: 1,090MB	(1,090MB) - NO SPLIT - only 1 variable
 - MS4.05: 0.39MB	(0.39MB) - NO SPLIT - only 1 variable
 - MS4.06: 65MB	(22MB) - split by scenario(3) - only 1 variable
 - MS4.07: ???	???
 - MS4.08: 204MB	(68MB) - split by scenario(3) - only 1 variable
 - MS4.09: 178MB	(178MB) - NO SPLIT - only 1 variable

## 3. File-naming convention

File names should follow the following convention:

 `<var_id>_<collection>_<component-1>_<component-2>_<time_period>.nc`
 
Values for most of the components can be found in the UKCP18 Controlled Vocabularies at:
 - var_id: use the keys in the data structure under:
   - https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_variable.json
   - NOTE: this vocabulary is not finalised yet
 - collection: "marine-sim" (for all Marine Strand data)
 - component-1: such as "hist", "future", "event", "impact", "timeseries"
 - component-2: one of "hour", "6min", "15min, "analysis", "2100", "2300", "extremes"
	
## 4. Directory-naming convention	

On the CEDA Archive, the data will be stored in the following structure:

 `/badc/<project>/data/<collection>/<component-1>/<component-2>/<var_id>/<version>/`
 
At the Met Office you could store it in a similar structure such as:

 `/project/<project>/data/<collection>/<component-1>/<component-2>/<var_id>/<version>/`

Values for the components match those given above, except `<version>`.

`<version>` follows the CMIP5 format of `vYYYYMMDD` where "YYYYMMDD" is the date when the data was created (or published).

## 5. Variables and coordinate variables

Our evolving table of variables is here:

 https://docs.google.com/spreadsheets/d/1Ij3R3skvYhKnMSqXB6KHaxH0BSST5R0DI8zp2Qi82vw/edit#gid=762056270

It is being honed and converted to this Controlled Vocabulary:

 https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_variable.json (**needs an update**)

The content includes both variable IDs and common variable metadata.

Note that the table separates out absolute values from anomaly values (which have variable IDs suffixed
with "Anom" and _may_ have different units).

A common set of variable attributes are specified but, depending on the spatial representation, there might 
be others that should be added. Please see the example files for the additional attributes.

Information about coordinate variables is held in a separate vocabulary at:

 https://github.com/ukcp-data/UKCP18_CVs/blob/master/UKCP18_coordinate.json - *** Needs UPDATING***

Note that some of the attributes will reference coordinate variables that should also be included in the
data files. 

## 6. Global attributes

The global attributes for the project are categorised as either:
 - Mandatory
 - Recommended
 
### 6.1 Global attributes

The following global attributes are mandatory:

 - collection: "marine-sim"
 - contact: "ukcpproject@metoffice.gov.uk"
 - Conventions: "CF-1.5"
 - domain: "uk"
 - frequency: <frequency> *** TO DISCUSS - SHOULD IT BE IN NAMING CONVENTION? ***
 - institution: use: "Met Office Hadley Centre (MOHC), FitzRoy Road, Exeter, Devon, EX1 3PB, UK."
 - institution_id: use: "MOHC"
 - project: use: "UKCP18"
 - references: Published or web-based references that describe the data or methods used to produce it.
 - source: The method of production of the original data. If it was model-generated, source should name the model and its version, as specifically as could be useful.
 - title: A succinct description of what is in the dataset.
 - version: `v<YYYYMMDD>` - where the date (`<YYYYMMDD>`) is an agreed date set the same for ALL files in this data set.
   
Additionally, you can add more global attributes as you wish.

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

### 7.4 General NetCDF Advice

Here are some general points regarding good CF-netCDF practice:

 - Variable IDs:
  - the **main** variable ID should be written in camelCase (starting with a lower-case letter) without underscores.
    - this is required because it will appear in file names that use underscores as the delimiter
 
 - Variable attributes:
  - `long_name`: 
    - Start with a capital letter
    - Use spaces (not underscores)
  - `standard_name`: if you use a CF Standard Name then the value must be in the official standard name table here:
     http://cfconventions.org/Data/cf-standard-names/49/build/cf-standard-name-table.html
   
 - Historical attributes to remove:
  - um_stash_source: remove this attribute
  - grid_mapping: remove this attribute
  - coordinates: remove this attribute
 
 - `time` as the UNLIMITED dimension:
   - set as the UNLIMITED dimension - it enables better time-handling in software

 - Historical Variables:
   - latitude_longitude: remove this variable
   - forecast_period: remove this variable



