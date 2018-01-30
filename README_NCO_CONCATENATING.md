# Using NCO to concatenate files over time

## Most important rule - UNLIMITED dimension

The dimension to concatenate over (normally time) should be set
as UNLIMITED in the NetCDF files.

## Example concatenation

`ncrcat` can be used to concatenate a set of files:

```
ncrcat fakedata/ukcp18/data/land-prob/uk/region/a1b/sample/prAnom/mon/v20180109/prAnom_a1b_ukcp18-land-prob-uk-region-all_sample_mon_19690115-19691215.nc fakedata/ukcp18/data/land-prob/uk/region/a1b/sample/prAnom/mon/v20180109/prAnom_a1b_ukcp18-land-prob-uk-region-all_sample_mon_19700115-19701215.nc out.nc
```

However, if you forget to specify the variables with the `-v` argument
then you might lose those in the output file. So, use the `-v`
argument and state them all, e.g.:

```
ncrcat -h -v sample,prAnom,geo_region,time_bounds,time fakedata/ukcp18/data/land-prob/uk/region/a1b/sample/prAnom/mon/v20180109/prAnom_a1b_ukcp18-land-prob-uk-region-all_sample_mon_19690115-19691215.nc fakedata/ukcp18/data/land-prob/uk/region/a1b/sample/prAnom/mon/v20180109/prAnom_a1b_ukcp18-land-prob-uk-region-all_sample_mon_19700115-19701215.nc out.nc
```

We also added in `-h` to prevent adding anything to the `history` global
attribute.

