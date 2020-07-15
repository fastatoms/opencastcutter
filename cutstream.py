#!/usr/bin/env python

"""cutstream.py: Python script that cuts a dual-track open cast recording into clips."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


#Import class for video processing and create cuttools object
from cuttools import cuttools
ct = cuttools()


# -------------------------------------------------------------------------
# -- Instructions go below here

#Test cut of additional lecture
folder = "C:/temp/vl041500000-2020-7-3-8-42/2020-7-3-8-42"
cuts_file = "cuts_test.txt"


# -------------------------------------------------------------------------
# -- Program execution (no user input required below here)
ct.processCut(folder, cuts_file)

