#!/usr/bin/env python

cf = "C:/temp/vl041500000-2020-7-3-8-42/2020-7-3-8-42/cuts_test.txt"

from cuttools import cuttools

o1 = cuttools.loadCutsfile(cf)
print(o1)
