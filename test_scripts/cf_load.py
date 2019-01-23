#!/usr/bin/env python

import cf
import sys

import time
s = time.time()
cf.read(sys.argv[1])
print("{:.5f} seconds".format((time.time() - s)))
