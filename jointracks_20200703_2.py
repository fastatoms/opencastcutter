#!/usr/bin/env python

"""jointracks.py: Join a dual-track open cast recording (or clip cut from it) into one video with overlays"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


from cuttools import cuttools
from datetime import datetime

#Create cuttools object
ct = cuttools()

#load a list of clips to join


#Lectures 06-28
# cuts = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/vl041500000-2019-6-28-5-54/2019-6-28-5-54/cuts.txt"
# clips_file ="G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/vl041500000-2019-6-28-5-54/2019-6-28-5-54/clips.txt"

#Test cut of additional lecture
# cuts = "C:/temp/vl041500000-2020-7-3-8-42/2020-7-3-8-42/cuts_test.txt"
# clips_file = "C:/temp/vl041500000-2020-7-3-8-42/2020-7-3-8-42/clips.txt"
# ct.setScreenLeft([58, 14], [925, 39], [100, 500], [921, 485])
# ct.setScreenRight([940, 38],[1776, 47], [931, 485], [1731, 517])


#2020 Additional lecture part 1
cuts = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/joined/Zusatzaufzeichnung (fehlerhaft)/2020-07-03-10/cuts_drive.txt"
clips_file = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/joined/Zusatzaufzeichnung (fehlerhaft)/2020-07-03-10/clips_drive.txt"
ct.setScreenLeft([58, 14], [925, 39], [100, 500], [921, 485])
ct.setScreenRight([940, 38],[1776, 47], [931, 485], [1731, 517])
# Note:
# The above functions define the postion of the two projector screens in the video image.
# Numbers are given in pixels counting from the top left corner of the video image. 
# Thefirst pixel i[0, 0]
# The expected input looks like this:
# ([x0, y0], [x1, y1], [x2, y2], [x3, y3])
# Corner 0 [x0,y0]: top left of projector screen
# Corner 1 [x1, y1]: top right
# Corner 2 [x2, y2]: bottom left
# Corner 3 [x3, y3]: bottom right


# ========================= Not user input required from this point on
clips = ct.loadClips(clips_file)
#clips is now an array of arrays in the form of
#[ [clip0_track0, clip0_track1], [clip1_track0, clip1_track1],...]

#load experiment markers and cut markers from cuts file
exp_tstr = []
cut_tstr = []
cut_titles = []
with open(cuts,"r") as cf:
	for cl in cf:
		if cl.find("E\t") > -1:
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
#convert cut time strings into timestamps
cut_t=ct.str2Cut(cut_tstr)
#print("Cut time markers:")
#print(repr(cut_t))
#now cut_t is a list of cut marks

#convert experiment time string into timestamp
exp_t = ct.str2Exp(exp_tstr)
#now exp_t is a list of [experiment start, experiment end] in the time format of absolute time in full track

#convert cut times into clip intervals
clip_t=ct.cut2clip(cut_t)
#now clip_t is a list of [clip_start, clip_end] in the time format of absolute time in full track

#Now identify experiments for each clip and convert their timestamps to seconds
clip_exp_t = []
Nexp = len(exp_tstr)
Nclips = len(cut_t)-1
for i in range(Nclips):
	cclip = clip_t[i]
	print(f"Checking clip {i}")
	clip_exp_t.append([])
	for j in range(Nexp):
		#compare start and end to current experiment
		cexp = exp_t[j]
		if cclip[0] <= cexp[0] and cclip[1] >= cexp[1]:
			print(f"experiment selected No. {j}")
			#now convert timestamp to total seconds from start of clip
			exp_start = round((cexp[0]-cclip[0]).total_seconds())
			exp_end = round((cexp[1]-cclip[0]).total_seconds())
			clip_exp_t[i].append([exp_start, exp_end])
#Now clip_exp_t is a list of lists that shows the experiment start and end as seconds from start of each clip.
# If a clip contains no experiment, the entry is []
# If a clip contains one experiment, the entry is [[exp_start(sec), seconds_end(seconds)]]
# If a clip contains two or more experiments, the entry is [[exp1_start(seconds), exp1_end(seconds)], [exp2_start(seconds)...
print("Done selecting clips and experiments. My conclusion is")
print(repr(clip_exp_t))
print("================================================================")

for i in range(0,Nclips):
	print(f"=========== Begin joining clip No.: {i+1} of {Nclips}   =========== ")
	print(f"Track0: {clips[i][0]}")
	print(f"Track1: {clips[i][1]}")
	ct.joinTracks(clips[i][0], clips[i][1],clip_exp_t[i])

	print(f"=========== DONE  joining clip No.: {i+1} of {Nclips}   =========== ")
	print("")
	
print("=========== I am done with EVERYTHING!")
print("================================================================")
