import iris
f = iris.load('fakedata/ukcp18/data/land-sim/river_basin/uk/rcp85/r1i1p20/tas/mon/v20170331/tas_rcp85_ukcp18-land-gcm-uk-river-monthly_r1i1p20_mon_19010101-21001201.nc')

cube = f[0]

river_basins = cube.coord('region').points
print river_basins

data_for_clyde = cube.extract(iris.Constraint(region = 'clyde'))

print data_for_clyde.coord('region').points