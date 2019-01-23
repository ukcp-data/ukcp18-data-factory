import netCDF4


def temporal(ncdf, time_name):
    times = list(netCDF4.num2date(list(ncdf.variables[time_name]),
                                      ncdf.variables[time_name].units))
    for tm in times:
        print tm.isoformat()     

fpath = 'inputs/source_ncs/ukcp18-land-gcm-global-60km-mon.nc'
fpath = 'fakedata/ukcp18/data/land-prob/uk/25km/rcp85/percentile/tasAnom/mon/v20180331/tasAnom_rcp85_land-prob_uk_25km_percentile_mon_20011201-20021130.nc'
ds = netCDF4.Dataset(fpath)

temporal(ds, 'time')
