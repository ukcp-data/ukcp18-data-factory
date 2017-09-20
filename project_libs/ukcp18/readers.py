import iris

#constraint = 

import glob 
files = glob.glob("fakedata/ukcp18/data/land_probabilistic/25km/a1b/percentile/pr/v20170331/pr*.nc")

cubes = iris.load(files, ["precipitation rate"])
cube = cubes.concatenate_cube()
print cube
