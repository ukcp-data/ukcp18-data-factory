import iris
iris.FUTURE.netcdf_promote = True

cubes = iris.load('fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p?/tas/mon/v20170331/tas_rcp85_ukcp18-land-gcm-uk-monthly_r1i1p?_mon_20100101-20101201.nc', 'air_temperature')

for cube in cubes:
    del cube.attributes['ensemble_member']

print cubes.concatenate_cube()
