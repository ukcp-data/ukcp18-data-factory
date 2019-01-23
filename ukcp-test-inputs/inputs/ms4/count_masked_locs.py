#!/usr/bin/env python

import sys
import iris
import numpy

fpath = sys.argv[1]

cube = iris.load(fpath)[0]

ma = cube.data

mcount = 0
gcount = 0
for y in range(ma.shape[0]):
    for x in range(ma.shape[1]):
        point = ma[y, x]
        if numpy.ma.is_masked(point):
            mcount += 1
        else: 
            gcount += 1

print('{} points have data out of {}.'.format(gcount, (mcount + gcount)))
