#!/usr/bin/env python

"""testjoin.py: Test joining of tracks"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


from cuttools import cuttools
from datetime import datetime


exp_overlay=[[10, 20],[40,80]];
clip0 = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-0-00_Wiederholung.mp4";
clip1 = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-1-00_Wiederholung.mp4";

cuttools.joinTracks(clip0, clip1,exp_overlay);

print("I am done with EVERYTHING!");
