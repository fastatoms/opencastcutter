#!/usr/bin/env python

"""cutstream.py: Python script that cuts a dual-track open cast recording into clips."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


#Import class for video processing and create cuttools object
from cuttools import cuttools
ct = cuttools()


# -------------------------------------------------------------------------
# -- Instructions go below here

# Test cut of example open cast lecture
# Note:
#  - example tracks are only 30sec long
#  - the folder variable can be defined as relative path (relative to location of this python file)
#    or as an absolute path e.g. c:/videos/lecture01
#  - The filenames of the tracks in the cuts.txt must follow the same syntax.
#    Either relative path (from location of python file) or absolute path e.g. c:/videos/lecture01/track-0.mp4
folder = "tests"
cuts_file = "cuts.txt"


# -------------------------------------------------------------------------
# -- Program execution (no user input required below here)
ct.processCut(folder, cuts_file)

