#!/usr/bin/env python

"""testcut.py: First test script to cut an open cast dual stream."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


import os, time, subprocess
from datetime import datetime
from datetime import timedelta


track0 = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-0.mp4";
track1 = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/tracl-1.mp4";


#Offset of track-1 relative to track-0.
#  Positive numbers mean that things happen LATER in track-1 compared to track-0
t_offset = 8.5;


#Now define a bunch of cuts
#The first cut mark indicates the start of the output videos
#The last cut mark indicates the end of the output videos
t_cut_str = ["00:00:00", "00:00:20", "00:01:23", "00:05:15", "01:01:00"];


# Convert cuts into numbers
t0_cut=[];
for ts in t_cut_str:
	t0_cut.append(datetime.strptime(ts,"%H:%M:%S"));



#Define the cutting function 
def cutTrack(track_filename, track_cuts):
	track_name, track_ext = os.path.splitext(track_filename);
	print("Now working on track: %s"%(track_filename));
	N = len(track_cuts);
	for i in range(N-1):
		cut_start = track_cuts[i].strftime("%H:%M:%S.%f");
		cut_end = track_cuts[i+1].strftime("%H:%M:%S.%f");
		clip_name = track_name + "-%02d"%(i) + track_ext;
		ffmpeg_cmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg");
		ffmpeg_cmd = ffmpeg_cmd + f" -hide_banner -loglevel warning -i {track_filename}";
		ffmpeg_cmd = ffmpeg_cmd +f" -c copy -ss {cut_start} -to {cut_end} -y {clip_name}";
		#print(ffmpeg_cmd); #This is the command that will be executed in the shell
		rtn = subprocess.check_call(ffmpeg_cmd);
		if rtn== 0:
			print("Successfully saved clip No.: %2d of %2d"%(i+1, N-1));
		else:
			print("ERROR writing clip No. : %2d of %2d"%(i+1, N-1));
	print("I am done with track 1");

def addCutOffset(track_cuts,cut_offset):
	# Create cut array for stream 2
	t_o=[];
	for ts in track_cuts:
		t_o.append(ts + timedelta(seconds=cut_offset));
	return t_o;


#Now do the cutting
#cutTrack(track0,t0_cut);

t1_cut = addCutOffset(t0_cut,t_offset);
print(t1_cut);
