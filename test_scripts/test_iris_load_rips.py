import os
import time

import iris
import pytest



def _get_file_list(threshold=40):
    files = []

    for dirpath, _2, filenames in os.walk('fakedata/ukcp18/data/land-gcm/uk/60km/rcp85'):
        for f in filenames:

            if not f.startswith('tas'): continue
            fpath = os.path.join(dirpath, f)
            files.append(fpath)

            if len(files) >= threshold: 
                return files

    return files


def _timeit(f, *args, **kwargs):
    start = time.time()
    res = f(*args, **kwargs)
    end = time.time()

    print "Ran: {}(); took: {:.2f} seconds".format(f, (end - start))
    return res

#@pytest.mark.timeout(3)
def test_iris_load_file_list_fast():
    "Tests to see that Iris can load data quickly."
#    iris.load('fakedata/ukcp18/data/land-gcm/uk/60km/rcp85/*/
  
    files = _get_file_list()
    for f in files[:3]:
        print(f)

    print("...")

    for f in files[-3:]:
        print(f)

    cubes = _timeit(iris.load, files)
#    print cubes 


test_iris_load_file_list_fast()
