#!/usr/bin/env python

"""cuttools.py: Class containing cutting tools for opencastcutter."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


import os, time, subprocess
from datetime import datetime
from datetime import timedelta
from platform import system

class cuttools():
	def __init__(self):
		#Video appearance settings
		self.vid_size = [1920, 1088] #size of output video
		self.ol_size = [1296, 736] #Size of whiteboard overlay

		#Perspective adjustment settings for screens in stage view
		self.perpective_adjust = "on" #options are: "on", "off"
		self.perspective_adjust_settings = {"screen_left_coords": [[170, 96], [935, 111], [200, 528], [930, 516]],
											"screen_right_coords": [[944, 113],[1688, 123], [937, 517], [1652, 544]],
											"interpolation_factor": 3}

		#Color adjustment
		self.color_adjust_stage = "medium"  # options are: "off", "medium", "strong"
		self.color_adjust_screen = "lighten" # options are: "off", "lighten", "medium", "strong"
		self.color_adjust_settings = {"off": "null",
									  "medium": "curves=psfile=filters/stagecorr_medium.acv",
									  "strong":"curves=psfile=filters/stagecorr_strong.acv",
									  "lighten": "colorlevels=rimax=0.95:gimax=0.95:bimax=0.95"}
		self.debug = False # either True or False. Toggles amoung of text output 

	def cutTrack(self, track_filename, track_cuts, clip_titles):
		#This function cuts a track into clips
		track_name, track_ext = os.path.splitext(track_filename)
		cliplist =[]

		print("================================================================")
		print(f"=======   Now cutting track: {track_filename}")
		N = len(track_cuts)
		for i in range(N-1):
			cut_start = track_cuts[i].strftime("%H:%M:%S.%f")
			cut_end = track_cuts[i+1].strftime("%H:%M:%S.%f")
			clip_title = "_" + clip_titles[i].replace(" ","_")
			clip_name = track_name + "-%02d"%(i) + clip_title + track_ext
			#Begin ffmpeg command (with different path depending on operating system)
			if system() == "Windows":
				ffmpeg_cmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg")
			else:
				ffmpeg_cmd = "ffmpeg"
			ffmpeg_cmd = ffmpeg_cmd + f" -hide_banner -loglevel warning -i \"{track_filename}\""
			ffmpeg_cmd = ffmpeg_cmd +f" -c copy -ss {cut_start} -to {cut_end} -y \"{clip_name}\""
			#print(ffmpeg_cmd) #This is the command that will be executed in the shell
			try:
				rtn = subprocess.check_call(ffmpeg_cmd)
				cliplist.append(clip_name)
				print("       Successfully saved clip No.: %2d of %2d, cut mark %s"%(i+1, N-1, cut_start))
			except subprocess.CalledProcessError as grepexc:
				print("       ERROR writing clip No. : %2d of %2d"%(i+1, N-1))
				print(grepexc.returncode)

		print("===========    DONE creating clips.    =========================")
		print("================================================================")
		return cliplist

	def joinTracks(self, track0_filename, track1_filename, nooverlay_intervals):
		#This function joins two clips by adding an overlay of track1 to track0
		#The nooverlay_intervals is used to indicate time intervals where an overlay should NOT be displayed
		track_name, track_ext = os.path.splitext(track0_filename)
		clip_name = track_name + "_joined" + track_ext

		#Video appearance settings
		vid_size = self.vid_size #size of output video
		ol_size = self.ol_size #Size of whiteboard overlay

		#Obtain duration of the two tracks
		fpcmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffprobe")
		fpcmd = fpcmd + f" -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "

		t0 = round(float(subprocess.check_output(fpcmd + f"\"{track0_filename}\"")))
		t1 = round(float(subprocess.check_output(fpcmd + f"\"{track1_filename}\"")))
		tend = min(t0,t1)

		#Begin ffmpeg command (with different path depending on operating system)
		if system() == "Windows":
			ffmpeg_cmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg")
		else:
			ffmpeg_cmd = "ffmpeg"
		fcmd = fcmd + f" -hide_banner -loglevel warning"
		fcmd = fcmd + f" -i \"{track1_filename}\" -i \"{track0_filename}\""
		fcmd = fcmd + f" -filter_complex \""
		
		fi =""

		#Assemble command for color correction of the stage view
		fi = fi + f"[1:v]{self.color_adjust_settings.get(self.color_adjust_stage)}[in1_stage];"
			
		if nooverlay_intervals == []:
			print("Joining clips with continuous overlay. No interruption of overlay selected.")
			# Assemble command with overlay all the time
			fi = fi + f"[0:v]scale={ol_size[0]}:{ol_size[1]} [pip0];"
			fi = fi +f"[pip0]pad=width={vid_size[0]}:height={ol_size[1]}:x={round((vid_size[0]-ol_size[0])/2)}:y=0:color=black [pb0];"
			fi = fi +f"[in1_stage][pb0] overlay=0:0:enable=\'between(t,0,{tend})\'"
			No = 0
			Nnoo = 1
			overlay_interval=[]
		else:
			#Generate overlay intervals (with or without perspective adjustment of screen images)
			overlay_interval = [[0, nooverlay_intervals[0][0]]]
			Nnoo = len(nooverlay_intervals)
			for i in range(1,Nnoo):
				overlay_interval.append([nooverlay_intervals[i-1][1], nooverlay_intervals[i][0]])
			overlay_interval.append([ nooverlay_intervals[Nnoo-1][1], tend])
			
			if self.perpective_adjust=="on": #(here,the switch betweenn perspective-corrected and non-corrected happens)

				#Assemble command to perform color correction on the screen display
				fi = fi + f"[1:v]{self.color_adjust_settings.get(self.color_adjust_screen)}[in1_screen];"

				#calculate screen corners in scaled video
				pss = self.perspective_adjust_settings.get("interpolation_factor")
				sl=[]
				sr=[]
				for si in self.perspective_adjust_settings.get("screen_left_coords"):
					sl.append([si[0]*pss, si[1]*pss])
				for si in self.perspective_adjust_settings.get("screen_right_coords"):
					sr.append([si[0]*pss, si[1]*pss])
				#Perform perspective correction on both screen images
				fi = fi + f"[in1_screen]scale=w={vid_size[0]*pss}:h={vid_size[1]*pss}[sc];[sc]split=2[sca][scb];"
				fi = fi + f"[sca]perspective=x0={sl[0][0]}:y0={sl[0][1]}:x1={sl[1][0]}:y1={sl[1][1]}:x2={sl[2][0]}:y2={sl[2][1]}:x3={sl[3][0]}:y3={sl[3][1]}[pea];"
				fi = fi + f"[pea]scale=w={round(vid_size[0]/2)}:h={round(vid_size[1]/2)}[psa];[psa]split={Nnoo}"
				for k in range(0,Nnoo):
					fi = fi + f"[psa{k}]"
				fi = fi + f";"
				fi = fi + f"[scb]perspective=x0={sr[0][0]}:y0={sr[0][1]}:x1={sr[1][0]}:y1={sr[1][1]}:x2={sr[2][0]}:y2={sr[2][1]}:x3={sr[3][0]}:y3={sr[3][1]}[peb];"
				fi = fi + f"[peb]scale=w={round(vid_size[0]/2)}:h={round(vid_size[1]/2)}[psb];[psb]split={Nnoo}"
				for l in range(0,Nnoo):
					fi = fi + f"[psb{l}]"
				fi = fi + f";"

				#Assemble command to do perspective correction of the projector screens
				for j in range(0,Nnoo):
					if j==0:
						fi = fi + f"[in1_stage]"
					else:
						fi = fi + f"[nov{j-1}]"
					fi = fi + f"[psa{j}]overlay=0:0:enable=\'between(t,{nooverlay_intervals[j][0]},{nooverlay_intervals[j][1]})\'[nout{j}];"
					fi = fi + f"[nout{j}][psb{j}]overlay={round(vid_size[0]/2)}:0:enable=\'between(t,{nooverlay_intervals[j][0]},{nooverlay_intervals[j][1]})\'[nov{j}];"
			else:
				fi = fi +f"[in1_stage]null[nov{Nnoo-1}];"

			#Assemble command to add interrupted overlay
			No = len(overlay_interval)
			
			#Assemble command to rescale whiteboard overlay
			fi = fi + f"[0:v]scale={ol_size[0]}:{ol_size[1]} [ovr];"
			fi = fi + f"[ovr]pad=width={vid_size[0]}:height={ol_size[1]}:x={round((vid_size[0]-ol_size[0])/2)}:y=0:color=black [ovb];"

			#Assemble command to add whiteboard overlay during movie
			fi = fi + f"[ovb]split={No}"
			for m in range(0,No):
				fi = fi + f"[pip{m}]"
			fi = fi + f";"
			for i in range(0,No):
				if i==0:
					fi = fi +f"[nov{Nnoo-1}]" #here, the stream with the perspective-corrected screens enters
				else:
					fi = fi +f"[out{i-1}]"
				fi = fi +f"[pip{i}] overlay=0:0:enable=\'between(t,{overlay_interval[i][0]},{overlay_interval[i][1]})\'"
				if i<(No-1):
					fi = fi +f"[out{i}];"
				
		
		#Quality settings
		#fcmd = fcmd + f"\" -map 0:a -profile:v main -level 3.1 -b:v 440k -ar 44100 -ab 128k -s 1920x1088 -vcodec h264 -acodec aac -y {clip_name}"
		fcmd = fcmd + fi +"\""
		fcmd = fcmd + f" -map 0:a -profile:v main -c:v libx264 -preset slow -crf 22 -c:a copy -y \"{clip_name}\""

		print("----------- Join tracks function called:")
		print(f"Overlay intervals: {No}")
		print(repr(overlay_interval))
		print(f"No overlay intervals: {Nnoo}")
		print(repr(nooverlay_intervals))
		if self.debug:
			print("This is the FFMPEG command to be executed:")
			print(fcmd)
		print(f"----------- Starting encoding now. {datetime.now()}")

		#Execute FFMPEG command
		try:
			rtn = subprocess.check_call(fcmd)
			print(f"----------- Done. Successfully saved clip {clip_name} time: {datetime.now()}=====")
		except subprocess.CalledProcessError as grepexc:
			print(f"******************    ERROR writing clip:    *******************")
			print(f"*** {clip_name}")
			print(f"****************************************************************")
			print(grepexc.returncode)

	def processCut(self, folder, cuts_file="cuts.txt"):
		
		# Load cutting instructions from cuts.txt
		ci = self.loadCutsfile(folder + "/" + cuts_file)

		#Get cut timestamps for both tracks
		cut_t0 = ci.cut_t
		cut_t1 = self.addCutOffset(ci.cut_t,ci.offset_t)

		#Now do the cutting
		t0_clips = self.cutTrack(ci.track0_file,cut_t0,ci.titles)
		t1_clips = self.cutTrack(ci.track1_file,cut_t1,ci.titles)

		#Save the list of clip filenames  for further use
		clips_file = folder+"/" +"clips.txt"
		with open(clips_file,'w') as cliplist:
			for i in range(len(t0_clips)):
				line = f"{t0_clips[i]}\t{t1_clips[i]}\n"
				cliplist.write(line)
			cliplist.close()
		return clips_file


	def processJoin(self, folder, cuts_file="cuts.txt", clips_file="clips.txt"):
		
		# Load cutting instructions from cuts.txt
		ci = self.loadCutsfile(folder + "/" + cuts_file)

		# Load clips list from clips.txt
		cl = self.loadClips(folder + "/" + clips_file)

		print("================================================================")

		Nclips = len(cl)
		for i in range(0,Nclips):
			print(f"=========== Begin joining clip No.: {i+1} of {Nclips}   =================== ")
			print(f"Track0: {cl[i][0]}")
			print(f"Track1: {cl[i][1]}")
			self.joinTracks(cl[i][0], cl[i][1],ci.clip_exp_t[i])

			print(f"=========== Done joining clip No.: {i+1} of {Nclips}   ==================== ")
			print("")

		print("===========  I am done with EVERYTHING!  =======================")
		print("================================================================")



	def addCutOffset(self, track_cuts,cut_offset):
		# This function adjusts the cut marks for stream 2 by adding the timing offset 
		# Create cut array for stream 2
		t_o=[]
		for ts in track_cuts:
			t_o.append(ts + timedelta(seconds=cut_offset))
		return t_o

	def printCuts(self, track_cuts):
		for ts in track_cuts:
			print(ts.strftime("%H:%M:%S.%f"))
	
	def setScreenLeft(self, top_left, top_right, bottom_left, bottom_right):
		# The expected input is four coordinates of the form [x, y]:
		# numbers must be given in pixel
		# The topmost leftmost pixel of the entire video image has the coordinate [0, 0]
		self.perspective_adjust_settings["screen_left_coords"] = [top_left, top_right, bottom_left, bottom_right]

	def setScreenRight(self, top_left, top_right, bottom_left, bottom_right):
		# The expected input is four coordinates of the form [x, y]:
		# numbers must be given in pixel
		# The topmost leftmost pixel of the entire video image has the coordinate [0, 0]
		self.perspective_adjust_settings["screen_right_coords"] = [top_left, top_right, bottom_left, bottom_right]

	def setPerspectiveAdjust(self, adjust_toggle):
		# The expected input is a string
		# "on"  : Perspective correction of the lecture hall screens on
		# "off" : Perspective correction off
		self.perpective_adjust = adjust_toggle

	def str2Cut(self, string_cuts):
		t_o=[]
		for ts in string_cuts:
			t_o.append(datetime.strptime(ts,"%H:%M:%S"))
		return t_o

	def str2Exp(self, string_experiments):
		e_o=[]
		Nexp = len(string_experiments)
		for i in range(Nexp):
			cm = string_experiments[i]
			ct = [datetime.strptime(cm[0],"%H:%M:%S"), datetime.strptime(cm[1],"%H:%M:%S")]
			e_o.append(ct)
		#now e_o is a list of [experiment start, experiment end] in the time format of absolute time in FULL track
		return e_o

	
	def cut2clip(self, cutlist):
		#convert cut times into clip intervals
		Nclips = len(cutlist)-1
		clip_t = []
		if Nclips >=1:
			for i in range(Nclips):
				clip_t.append([cutlist[i],cutlist[i+1]])
			#now clip_t is a list of [clip_start, clip_end] in the time format of absolute time in full track
		else:
			clip_t=-1
		return clip_t
		

	def loadCutsfile(self, cuts_file):
		#Import the timestamps and names from cuts.txt file
		#Current function only imports 
		t_offset = 0.0
		cut_tstr = []
		exp_tstr = []
		cut_titles = []
		print(f"Loading cuts information from file: {cuts_file}")
		with open(cuts_file,"r") as cf:
			for cl in cf:
				if cl.find("offset") > -1:
					o = cl.split("\t")
					t_offset = float(o[1])
					print("Offset found: %f s"%(t_offset))
				elif cl.find("track0") > -1:
					t0 = cl.split("\t")
					track0 = t0[1].strip("\n")
					print("Input track 0: %s"%(track0))
				elif cl.find("track1") > -1:
					t1 = cl.split("\t")
					track1 = t1[1].strip("\n")
					print("Input track 1: %s"%(track1))
				elif cl.find("E\t") > -1:
					em = cl.strip("\n").split("\t")
					exp_tstr.append([em[1], em[2]])
					print(f"Found Experiment marker. Start: {em[1]} End: {em[2]}")
				elif cl.find("C\t") > -1:
					c = cl.split("\t")
					cut_tstr.append(c[1])
					cut_titles.append(c[2].strip("\n"))
					print(f"Found Cut marker. {c[1]}")
				else:
					print("ignored unknown command")
			cf.close()
		#convert Cut marker string array to timestamp
		cut_t=self.str2Cut(cut_tstr)

		#convert experiment time string into timestamp
		exp_t = self.str2Exp(exp_tstr)

		#convert cut marks into clip tuples with start and end
		clip_t=self.cut2clip(cut_t)
		print(clip_t)
		#Identify experiment time intervals for each clip and convert to start and stop time in sec
		clip_exp_t = []
		Nexp = len(exp_tstr)
		Nclips = len(cut_t)-1
		for i in range(Nclips):
			cclip = clip_t[i]
			clip_exp_t.append([])
			for j in range(Nexp):
				#compare start and end to current experiment
				cexp = exp_t[j]
				if cclip[0] <= cexp[0] and cclip[1] >= cexp[1]:
					#now convert timestamp to total seconds from start of clip
					exp_start = round((cexp[0]-cclip[0]).total_seconds())
					exp_end = round((cexp[1]-cclip[0]).total_seconds())
					clip_exp_t[i].append([exp_start, exp_end])
		#Now clip_exp_t is a list of lists that shows the experiment start and end as seconds from start of each clip.
		# If a clip contains no experiment, the entry is []
		# If a clip contains one experiment, the entry is [[exp_start(sec), seconds_end(seconds)]]
		# If a clip contains two or more experiments, the entry is [[exp1_start(seconds), exp1_end(seconds)], [exp2_start(seconds)...

		ci = cut_instructions()
		ci.cuts_file = cuts_file
		ci.track0_file = track0 
		ci.track1_file = track1
		ci.cut_str = cut_tstr
		ci.Nclips = Nclips
		ci.cut_t = cut_t
		ci.clip_t = clip_t
		ci.exp_tstr = exp_tstr
		ci.exp_t = exp_t
		ci.clip_exp_t = clip_exp_t
		ci.offset_t=t_offset
		ci.titles = cut_titles
		return ci
	
	def mono2stereo(self,input_filename,audio_channel=0):
		#convert from single-channel (mono) sound to quasi-stereo
		#Quickly copy a mkv file into a mp4 container WITHOUT re-encoding
		in_folder, in_file = os.path.split(input_filename)
		in_name, in_extension = os.path.splitext(in_file)
		print("================================================================")
		print(f"=======   Now converting mono to stereo for clip: {input_filename}")
		output_filename = os.path.join(in_folder,in_name + "_2ch.mp4")

		#Begin ffmpeg command (with different path depending on operating system)
		if system() == "Windows":
			ffmpeg_cmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg")
		else:
			ffmpeg_cmd = "ffmpeg"
		ffmpeg_cmd = ffmpeg_cmd + f" -hide_banner -loglevel warning -i \"{input_filename}\""
		ffmpeg_cmd = ffmpeg_cmd + f" -filter_complex \"[0:a]channelmap={audio_channel}|{audio_channel}:stereo[a]\""""
		ffmpeg_cmd = ffmpeg_cmd + f" -map \"[a]\" -map 0:v -c:v copy" 
		ffmpeg_cmd = ffmpeg_cmd + f" -y \"{output_filename}\""
		print("This is the ffmpeg commadn to be executed:")
		print(ffmpeg_cmd) #This is the command that will be executed in the shell
		try:
			rtn = subprocess.check_call(ffmpeg_cmd)
			rtn_msg = output_filename
			print("       Successfully written file.")
		except subprocess.CalledProcessError as grepexc:
			print("       ERROR writing file.")
			print(grepexc.returncode)
			rtn_msg = -1

		print("===========    DONE converting to stereo.    =========================")
		print("================================================================")
		return rtn_msg	

	
	def mkv2mp4(self, input_filename):
		#Quickly copy a mkv file into a mp4 container WITHOUT re-encoding
		in_folder, in_file = os.path.split(input_filename)		
		in_name, in_extension = os.path.splitext(in_file)
		print(in_folder)
		print(in_file)
		print(in_name)
		print(in_extension)
		if  in_extension == ".mkv":
			print("================================================================")
			print(f"=======   Now changing container for clip: {input_filename}")
			output_filename = os.path.join(in_folder,in_name + ".mp4")

			#Begin ffmpeg command (with different path depending on operating system)
			if system() == "Windows":
				ffmpeg_cmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg")
			else:
				ffmpeg_cmd = "ffmpeg"
			ffmpeg_cmd = ffmpeg_cmd + f" -hide_banner -loglevel warning -i \"{input_filename}\""
			ffmpeg_cmd = ffmpeg_cmd +f" -c copy -y \"{output_filename}\""
			#print(ffmpeg_cmd) #This is the command that will be executed in the shell
			try:
				rtn = subprocess.check_call(ffmpeg_cmd)
				rtn_msg = output_filename
				print("       Successfully written file.")
			except subprocess.CalledProcessError as grepexc:
				print("       ERROR writing file.")
				print(grepexc.returncode)
				rtn_msg = -1

			print("===========    DONE changing container.    =========================")
			print("================================================================")
		else:
			print("DUDE: Input file is not .mkv. I will ignore it.")
			rtn_msg = -1
		return rtn_msg	

	def encodeMp4(self, input_filename):
		#Re-encode any input file into a mp4 file
		in_folder, in_file = os.path.split(input_filename)		
		in_name, in_extension = os.path.splitext(in_file)
		print(in_folder)
		print(in_file)
		print(in_name)
		print(in_extension)
		print("================================================================")
		print(f"=======   Now re-encoding clip: {input_filename}")
		output_filename = os.path.join(in_folder,in_name + "_small.mp4")
		#Begin ffmpeg command (with different path depending on operating system)
		if system() == "Windows":
			ffmpeg_cmd = os.path.join(os.getcwd(),"libs/ffmpeg/bin/ffmpeg")
		else:
			ffmpeg_cmd = "ffmpeg"
		ffmpeg_cmd = ffmpeg_cmd + f" -hide_banner -loglevel warning -i \"{input_filename}\""
		ffmpeg_cmd = ffmpeg_cmd +f" -profile:v main -c:v libx264 -preset slow -crf 30 -c:a copy -y \"{output_filename}\""
		#note 06 Nov 2020 crf 23 is very good quality and approx 1/2 size of original recording
		#print(ffmpeg_cmd) #This is the command that will be executed in the shell
		try:
			rtn = subprocess.check_call(ffmpeg_cmd)
			rtn_msg = output_filename
			print("       Successfully written file.")
		except subprocess.CalledProcessError as grepexc:
			print("       ERROR writing file.")
			print(grepexc.returncode)
			rtn_msg = -1
		print("===========    DONE re-encoding video.    =========================")
		print("================================================================")
		return rtn_msg	


	def loadClips(self, clips_file):
		clips=[]
		with open(clips_file,"r") as cf:
			for cl in cf:
				clips.append(cl.strip("\n").split("\t"))
		cf.close()
		#clips is now an array of arrays in the form of
		#[ [clip0_track0, clip0_track1], [clip1_track0, clip1_track1],...]
		return clips


class cut_instructions:
	def __init__(self):
		self.cuts_file = []
		self.clips_file = []
		self.track0_file = [] #needed in processCut
		self.track1_file = [] #needed in processCut
		self.cut_str = []
		self.Nclips = []
		self.cut_t = [] #needed in processCut
		self.exp_tstr = []
		self.exp_t = []
		self.clip_exp_t = []  #needed in processJoin
		self.offset_t = 0.0 #needed in processCut
		self.titles = [] #needed in processCut

	def __str__(self):
		s=f"cuttools.cut_instructions object.\nContent:\n"
		s=s+f".track0_file: {self.track0_file}\n.track1_file: {self.track1_file}\n"
		s=s+f".offset_t: {self.offset_t}\n"
		s=s+f".cut_t (List of cuts):\n"
		for ci in self.cut_t:
			cuttime = ci.strftime("%H:%M:%S.%f")
			s=s+f"    {cuttime}\n"
		s=s+f".titles (List of clip titles):\n"
		for ti in self.titles:
			s=s+f"    {ti}\n"
		s=s+f".exp_t (List of experiment intervals, no overlay):\n"
		for ei in self.exp_t:
			estart = ei[0].strftime("%H:%M:%S.%f")
			eend = ei[1].strftime("%H:%M:%S.%f")
			s=s+f"    {estart}   {eend}\n"

		return s
