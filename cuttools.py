#!/usr/bin/env python

"""cuttools.py: Class containing cutting tools."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


import os, time, subprocess
from datetime import datetime
from datetime import timedelta


class cuttools:
	def cutTrack(track_filename, track_cuts, clip_titles):
		#This function cuts two tracks into synchronized clips
		track_name, track_ext = os.path.splitext(track_filename);
		cliplist =[];

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
				cliplist.append(clip_name);
				print("Successfully saved clip No.: %2d of %2d, cut mark %s"%(i+1, N-1, cut_start));
			except subprocess.CalledProcessError as grepexc:
				print("ERROR writing clip No. : %2d of %2d"%(i+1, N-1));
				print(grepexc.returncode);

		print("I am done.");
		return cliplist;

	def joinTracks(track0_filename, track1_filename, nooverlay_intervals):
		#This function joins two clips by adding an overlay of track1 to track0
		#The nooverlay_intervals is used to indicate time intervals where an overlay should NOT be displayed
		track_name, track_ext = os.path.splitext(track0_filename);
		clip_name = track_name + "_joined" + track_ext;

		#Obtain duration of the two tracks
		fpcmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffprobe");
		fpcmd = fpcmd + f" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ";

		t0 = round(float(subprocess.check_output(fpcmd + track0_filename)));
		t1 = round(float(subprocess.check_output(fpcmd + track1_filename)));
		tend = min(t0,t1);

		
		fcmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg");
		fcmd = fcmd + f" -hide_banner -loglevel warning"
		fcmd = fcmd + f" -i {track1_filename} -i {track0_filename}";
			
		if nooverlay_intervals == []:
			print("Joining clips with continuous overlay. No interruption of overlay selected.")
			# Assemble command with overlay all the time
			fcmd = fcmd + f" -filter_complex \"[0:v]scale=iw*0.7:ih*0.7 [pip0]; [1:v][pip0] overlay=main_w-overlay_w-3:3:enable=\'between(t,0,{tend})\'";
		else:
			#Generate overlay intervals
			overlay_interval = [[0, nooverlay_intervals[0][0]]];
			Nnoo = len(nooverlay_intervals);
			for i in range(1,Nnoo):
				print(i);
				overlay_interval.append([nooverlay_intervals[i-1][1], nooverlay_intervals[i][0]]);
			overlay_interval.append([ nooverlay_intervals[Nnoo-1][1], tend]);
			print(repr(overlay_interval));

			#Assemble command with interrupted overlay
			fcmd = fcmd + f" -filter_complex \"[0:v]scale=iw*0.7:ih*0.7 [pip0]; [1:v][pip0] overlay=main_w-overlay_w-3:3:enable=\'between(t,{overlay_interval[0][0]},{overlay_interval[0][1]})\'"
			No = len(overlay_interval);
			print(f"Number of overlay intervals: {No}");
			for i in range(1,No):
				fcmd = fcmd +f" [out{i}]; [0:v]scale=iw*0.7:ih*0.7 [pip{i+1}]; [out{i}][pip{i+1}] overlay=main_w-overlay_w-3:3:enable=\'between(t,{overlay_interval[i][0]},{overlay_interval[i][1]})\'";
		
		#Quality settings
		#fcmd = fcmd + f"\" -map 0:a -profile:v main -level 3.1 -b:v 440k -ar 44100 -ab 128k -s 1920x1080 -vcodec h264 -acodec aac -y {clip_name}";
		fcmd = fcmd + f"\" -map 0:a -profile:v main -c:v libx264 -preset slow -crf 22 -c:a copy -y {clip_name}";

		print("This is the FFMPEG command to be executed:");
		print(fcmd);

		#Execute FFMPEG command
		try:
			rtn = subprocess.check_call(fcmd);
			print(f"Successfully saved clip {clip_name}");
		except subprocess.CalledProcessError as grepexc:
			print(f"ERROR writing clip {clip_name}");
			print(grepexc.returncode);

		print("I am done.");

	def addCutOffset(track_cuts,cut_offset):
		# This function adjusts the cut marks for stream 2 by adding the timing offset 
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
