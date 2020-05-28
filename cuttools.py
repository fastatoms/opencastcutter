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

		#Video appearance settings
		vid_size = [1920, 1080]; #size of output video
		ol_size = [1316, 740]; #Size of whiteboard overlay

		#Obtain duration of the two tracks
		fpcmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffprobe");
		fpcmd = fpcmd + f" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 ";

		t0 = round(float(subprocess.check_output(fpcmd + track0_filename)));
		t1 = round(float(subprocess.check_output(fpcmd + track1_filename)));
		tend = min(t0,t1);

		
		fcmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg");
		fcmd = fcmd + f" -hide_banner -loglevel warning";
		fcmd = fcmd + f" -i {track1_filename} -i {track0_filename}";
		fcmd = fcmd + f" -filter_complex \"";
		
		fi ="";

		#Assemble command for color correction of the stage view
		fi = fi + f"[1:v]curves=psfile=stagecorr4.acv[in1_stage];";
			
		if nooverlay_intervals == []:
			print("Joining clips with continuous overlay. No interruption of overlay selected.")
			# Assemble command with overlay all the time
			fi = fi + f"[0:v]scale={ol_size[0]}:{ol_size[1]} [pip0];";
			fi = fi +f"[pip0]pad=width={vid_size[0]}:height={ol_size[1]}:x={round((vid_size[0]-ol_size[0])/2)}:y=0:color=black [pb0];";
			fi = fi +f"[in1_stage][pb0] overlay=0:0:enable=\'between(t,0,{tend})\'";
			No = 0;
			Nnoo = 1;
			overlay_interval=[];
		else:
			#Generate overlay intervals
			overlay_interval = [[0, nooverlay_intervals[0][0]]];
			Nnoo = len(nooverlay_intervals);
			for i in range(1,Nnoo):
				overlay_interval.append([nooverlay_intervals[i-1][1], nooverlay_intervals[i][0]]);
			overlay_interval.append([ nooverlay_intervals[Nnoo-1][1], tend]);
			
			#Assemble command to perform color correction on the screen display
			fi = fi + f"[1:v]colorlevels=rimax=0.90:gimax=0.90:bimax=0.90[in1_screen];";

			#Assemble command to do perspective correction in the intervals without overlay
			fi = fi + f"[in1_screen]scale=w=5760:h=3240[sc];[sc]split=2[sca][scb];";
			fi = fi + f"[sca]perspective=x0=510:y0=285:x1=2805:y1=330:x2=600:y2=1572:x3=2790:y3=1536[pea];";
			fi = fi + f"[pea]scale=w=960:h=540[psa];[psa]split={Nnoo}";
			for k in range(0,Nnoo):
				fi = fi + f"[psa{k}]";
			fi = fi + f";";
			fi = fi + f"[scb]perspective=x0=2832:y0=336:x1=5064:y1=366:x2=2811:y2=1539:x3=4956:y3=1620[peb];";
			fi = fi + f"[peb]scale=w=960:h=540[psb];[psb]split={Nnoo}";
			for l in range(0,Nnoo):
				fi = fi + f"[psb{l}]";
			fi = fi + f";";

			for j in range(0,Nnoo):
				if j==0:
					fi = fi + f"[in1_stage]";
				else:
					fi = fi + f"[nov{j-1}]";
				fi = fi + f"[psa{j}]overlay=0:0:enable=\'between(t,{nooverlay_intervals[j][0]},{nooverlay_intervals[j][1]})\'[nout{j}];";
				fi = fi + f"[nout{j}][psb{j}]overlay=960:1:enable=\'between(t,{nooverlay_intervals[j][0]},{nooverlay_intervals[j][1]})\'[nov{j}];";


			#Assemble command to add interrupted overlay
			No = len(overlay_interval);
			
			fi = fi + f"[0:v]scale={ol_size[0]}:{ol_size[1]} [ovr];";
			fi = fi + f"[ovr]pad=width={vid_size[0]}:height={ol_size[1]}:x={round((vid_size[0]-ol_size[0])/2)}:y=0:color=black [ovb];";
			fi = fi + f"[ovb]split={No}";
			for m in range(0,No):
				fi = fi + f"[pip{m}]";
			fi = fi + f";";
			for i in range(0,No):
				if i==0:
					fi = fi +f"[nov{Nnoo-1}]";
				else:
					fi = fi +f"[out{i-1}]";
				fi = fi +f"[pip{i}] overlay=0:0:enable=\'between(t,{overlay_interval[i][0]},{overlay_interval[i][1]})\'";
				if i<(No-1):
					fi = fi +f"[out{i}];"
				
		
		#Quality settings
		#fcmd = fcmd + f"\" -map 0:a -profile:v main -level 3.1 -b:v 440k -ar 44100 -ab 128k -s 1920x1080 -vcodec h264 -acodec aac -y {clip_name}";
		fcmd = fcmd + fi +"\"";
		fcmd = fcmd + f" -map 0:a -profile:v main -c:v libx264 -preset slow -crf 22 -c:a copy -y {clip_name}";

		print("========== Join tracks function called ==========");
		print(f"Overlay intervals: {No}");
		print(repr(overlay_interval));
		print(f"No overlay intervals: {Nnoo}");
		print(repr(nooverlay_intervals));
		print("This is the FFMPEG command to be executed:");
		print(fcmd);
		print(f"===== Starting encoding now. {datetime.now()}=====");

		#Execute FFMPEG command
		try:
			rtn = subprocess.check_call(fcmd);
			print(f"===== Done. Successfully saved clip {clip_name} time: {datetime.now()}=====");
		except subprocess.CalledProcessError as grepexc:
			print(f"***** ERROR writing clip {clip_name} *****");
			print(grepexc.returncode);


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
