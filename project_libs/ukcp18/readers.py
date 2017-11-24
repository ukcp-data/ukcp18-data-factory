import iris

import glob 
files = glob.glob("fakedata/ukcp18/data/land-prob/25km/a1b/percentile/pr/v20170331/pr*.nc")

cubes = iris.load(files, ["precipitation rate"])
cube = cubes.concatenate_cube()
print cube

print "Read a subset in space and time:"

print cube.coords("time")
import datetime as dt
from iris.time import PartialDateTime

constr = iris.Constraint(time=lambda tm: 360 < tm < 800)
subset = cube.extract(constr)
print
print subset.coords("time")

try:
    constr = iris.Constraint(time=PartialDateTime(2003, 1, 1)) 
    with iris.FUTURE.context(cell_datetime_objects=True):
        subset = cube.extract(constr)
    print
    print subset.coords("time")
except:
    print "CANNOT compare a PartialDateTime to a time value...yet."
    print "This MIGHT be a problem with Iris compatibility with netcdftime version!"

