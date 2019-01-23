import iris

fpath = 'fakedata/ukcp18/data/land-prob/uk/25km/rcp85/percentile/tasAnom/mon/latest/tasAnom_rcp85_land-prob_uk_25km_percentile_mon_20021201-20031130.nc'
fpath = 'fakedata/ukcp18/data/land-prob/uk/25km/rcp85/percentile/tasAnom/mon/latest/tasAnom_rcp85_land-prob_uk_25km_percentile_mon_20081201-20091130.nc'
f = iris.load(fpath)

cube = f[1]

d = cube.extract(iris.Constraint(percentile=90))[0]

print d
print d.data

print("\nTest 1: Can extract data at 90th %ile: PASS\n\n")

import numpy
if len(d.shape) == 3:
  for i in range(12):
    numpy.array_equal(d[0].data.mask, d[i].data.mask)

  print("Test 2: Mask is the same at every time step: PASS\n\n")


