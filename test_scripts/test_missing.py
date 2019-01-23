import cdms2 as cdms
import os

fpath = 'fakedata/ukcp18/data/land-prob/uk/25km/rcp85/percentile/tasAnom/mon/v20180331/tasAnom_rcp85_land-prob_uk_25km_percentile_mon_20011201-20021130.nc'

f = cdms.open('inputs/rubbish/a.nc')
f = cdms.open(fpath)

var_id = os.path.basename(fpath).split("_")[0]

data = f(var_id)
print data.shape
print type(data)

ms = [data.mask[i] for i in range(data.shape[0])]

import numpy

for m in ms:
    print numpy.array_equal(ms[0], m)

d = data[0,20:30,30,-1]

for i in range(data.shape[-1]):
    print data.getAxisList()[-1][i], data[0, 20:30, 30, i]

