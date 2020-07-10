#!/usr/bin/env python

"""cutstream.py: Python script that cuts a dual-track open cast recording into clips."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


import os
from cuttools import cuttools


#Create cuttools object
ct = cuttools()

#Lecture 05-29 (from local PC Sebastian)
# cuts = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/cuts.txt"

#Lecture 05-31 (from Google Drive connected PC)
# cuts = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/vl041500000-2019-5-31-5-54/2019-5-31-5-54/cuts.txt"

#Lectures 06-19 (from FMQ PC)
cuts = "\\fmq-cifs.tik.uni-stuttgart.de/Loth_group/Teaching/2020 SS ExpPhys 2/SS2019 Aufzeichnung/vl041500000-2019-6-19-5-54/2019-6-19-5-54/cuts.txt"

#Lectures 06-26
# cuts = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/vl041500000-2019-6-26-5-54/2019-6-26-5-54/cuts.txt"

#Lectures 06-28
# cuts = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/vl041500000-2019-6-28-5-54/2019-6-28-5-54/cuts.txt"

#Test cut of additional lecture
cuts = "C:/temp/vl041500000-2020-7-3-8-42/2020-7-3-8-42/cuts_test.txt"

#Import cut marks
"""
Note:
	Cut marks need to be defined in the following format
	01:23:45 (tab)  bla bla
	To introduce a cut at position 1h 23min 45sec with the title "bla bla"
	Important is that the first cut mark indicates where the first clip will begin
	(If first clip should begin from track beginning enter first mark 00:00:00)
	Import is that the last cut mark is the end of the last clip.

	Offset needs to be specified as
	offset (tab)  8.5
	To introduce a 8.5 sec offset between track0 and track1.
	Positive numbers indicate that things in track1 are happening later
"""	
t_offset = 0.0
cut_tstr = []
cut_titles = []
with open(cuts,"r") as cf:
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
			print("Ignored experiment marker")
		elif cl.find("C\t") > -1:
			c = cl.split("\t")
			cut_tstr.append(c[1])
			cut_titles.append(c[2].strip("\n"))
		else:
			print("ignored unknown command")
	cf.close()


for i in range(len(cut_tstr)):
	print("Cut position found: %s title: %s"%(cut_tstr[i], cut_titles[i]))
# Convert cuts into numbers
t0_cut=ct.str2Cut(cut_tstr)
#print("Cut marks selected track0:")
#ct.printCuts(t0_cut)

#Now do the cutting

t0_clips = ct.cutTrack(track0,t0_cut,cut_titles)

t1_cut = ct.addCutOffset(t0_cut,t_offset)
#print("Cut marks selected track1:")
#ct.printCuts(t1_cut)
t1_clips = ct.cutTrack(track1,t1_cut,cut_titles)


#Save the list of generated files for further use
folder, cutsfile = os.path.split(cuts)
clips = folder+"/" +"clips.txt"
print(clips)
with open(clips,'w') as cliplist:
	for i in range(len(t0_clips)):
		line = f"{t0_clips[i]}\t{t1_clips[i]}\n"
		cliplist.write(line)
	cliplist.close()

