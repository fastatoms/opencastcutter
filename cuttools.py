#!/usr/bin/env python

"""cuttools.py: Class containing cutting tools."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


import os, time, subprocess
from datetime import datetime
from datetime import timedelta


class cuttools:
	#Define the cutting function 
	def cutTrack(track_filename, track_cuts, clip_titles):
		track_name, track_ext = os.path.splitext(track_filename);
		print("Now working on track: %s"%(track_filename));
		N = len(track_cuts);
		for i in range(N-1):
			cut_start = track_cuts[i].strftime("%H:%M:%S.%f");
			cut_end = track_cuts[i+1].strftime("%H:%M:%S.%f");
			clip_title = "_" + clip_titles[i].replace(" ","_");
			clip_name = track_name + "-%02d"%(i) + clip_title + track_ext;
			ffmpeg_cmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg");
			ffmpeg_cmd = ffmpeg_cmd + f" -hide_banner -loglevel warning -i {track_filename}";
			ffmpeg_cmd = ffmpeg_cmd +f" -c copy -ss {cut_start} -to {cut_end} -y {clip_name}";
			#print(ffmpeg_cmd); #This is the command that will be executed in the shell
			try:
				rtn = subprocess.check_call(ffmpeg_cmd);
				print("Successfully saved clip No.: %2d of %2d, cut mark %s"%(i+1, N-1, cut_start));
			except subprocess.CalledProcessError as grepexc:
				print("ERROR writing clip No. : %2d of %2d"%(i+1, N-1));
				print(grepexc.returncode);

		print("I am done.");

	def addCutOffset(track_cuts,cut_offset):
		# Create cut array for stream 2
		t_o=[];
		for ts in track_cuts:
			t_o.append(ts + timedelta(seconds=cut_offset));
		return t_o;

	def printCuts(track_cuts):
		for ts in track_cuts:
			print(ts.strftime("%H:%M:%S.%f"));

	def str2Cut(string_cuts):
		t_o=[];
		for ts in string_cuts:
			t_o.append(datetime.strptime(ts,"%H:%M:%S"));
		return t_o;
