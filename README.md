# ukcp18-data-factory

Data Factory for creating example data

## Example usage

```

```

## Testing that data can be read

### UKCP18 LS1 example

uick test for concatenating multiple files into one cube:

`python project_libs/ukcp18/readers.py`

## Some useful conversion commands

Use `ncks` to sub-sample across variable dimensions. E.g. 5km to 60km data:

```
ncks -d projection_x_coordinate,,,12 -d projection_y_coordinate,,,12 -v example_var osgb_5km.nc osgb_60km.nc
```

Subset global data to 1970 only at monthly scale on 15th of each month:

```
ncks -d time,14,365,30 -v precipitation_flux r001i1p00090_19701979_pr.nc pr_global_ls2_mon_197001-197012.nc
```
