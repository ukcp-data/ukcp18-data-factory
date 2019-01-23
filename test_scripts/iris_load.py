#!/usr/bin/env python

import iris
import sys

import time
s = time.time()
iris.load(sys.argv[1])
print("{:.5f} seconds".format((time.time() - s)))
