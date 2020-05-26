#!/usr/bin/env python

"""testjoin.py: Test joining of tracks"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


from cuttools import cuttools
from datetime import datetime

#load a list of clips to join
clips_file = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/clips.txt";
cuts = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/cuts.txt";


#Now clip_exp_t is a list of lists that shows the experiment start and end as seconds from start of each clip.
# If a clip contains no experiment, the entry is []
# If a clip contains one experiment, the entry is [[exp_start(sec), seconds_end(seconds)]]
# If a clip contains two or more experiments, the entry is [[exp1_start(seconds), exp1_end(seconds)], [exp2_start(seconds)...

exp_overlay=[[10, 20],[40,80]];
clip0 = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-0-00_Wiederholung.mp4";
clip1 = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-1-00_Wiederholung.mp4";

cuttools.joinTracks(clip0, clip1,exp_overlay);

print("I am done with EVERYTHING!");
