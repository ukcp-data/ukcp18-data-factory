import iris

import glob

files = glob.glob('fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p1/pr/mon/v20170331/pr_rcp85_ukcp18-land-gcm-uk-monthly_r1i1p1_mon_20*.nc')
files_60km_r1i1p1 = glob.glob('fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p1/pr/mon/v20170331/pr*')
files = glob.glob('fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p3/pr/mon/v20170331/pr_rcp85_ukcp18-land-gcm-uk*')
files = glob.glob('fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p[123]/tas/mon/v20170331/*.nc')
files_25km_percentile = glob.glob('fakedata/ukcp18/data/land-prob/25km/a1b/percentile/tas/mon/v20170331/tas_a1b_ukcp18-land-prob-25km_percentile_mon_201*')

files = files_60km_r1i1p1
files =files_25km_percentile
print files

cl = iris.load(files)
c = cl.concatenate()

print c

TEST_ENS_CONCAT = False
#TEST_ENS_CONCAT = True

if TEST_ENS_CONCAT:
    print "\nTrying to group ensemble members now...\n"
    files = ('fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p1/tas/mon/v20170331/tas_rcp85_ukcp18-land-gcm-uk-monthly_r1i1p1_mon_20100101-20101201.nc', 
            'fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p2/tas/mon/v20170331/tas_rcp85_ukcp18-land-gcm-uk-monthly_r1i1p2_mon_20100101-20101201.nc')

    print files

    ccl = iris.load(files)
    c = ccl.concatenate()
    print c
    #import pdb; pdb.set_trace()


print "---------------------------------"
ENSEMBLE_MEMBER = 'ensemble_member'

def clean_callback(cube, field, filename):
    if [True for coord in cube.coords() if coord.var_name == ENSEMBLE_MEMBER]: 
        del cube.metadata.attributes[ENSEMBLE_MEMBER]

if 0:
 cl = iris.load(files)
 cubes = (cl[2], cl[3])
 for cube in cubes:
    del cube.metadata.attributes[ENSEMBLE_MEMBER]

 cubes = iris.cube.CubeList(cubes)
 cubes.concatenate_cube()
 print cubes
 print cubes[0].metadata.attributes

fname = "fakedata/ukcp18/data/land-sim/60km/uk/rcp85/r1i1p3/tas/mon/v20170331/tas_rcp85_ukcp18-land-gcm-uk-monthly_r1i1p3_mon_19010101-21001201.nc"
cube = iris.load(fname)
print cube


