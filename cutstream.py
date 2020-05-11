#!/usr/bin/env python

"""testcut.py: First test script to cut an open cast dual stream."""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


from cuttools import cuttools

cuts = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/cuts.txt";


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
t_offset = 0.0;
cut_tstr = [];
cut_titles = [];
with open(cuts,"r") as cf:
	for cl in cf:
		if cl.find("offset") > -1:
			o = cl.split("\t");
			t_offset = float(o[1]);
			print("Offset found: %f s"%(t_offset));
		elif cl.find("track0") > -1:
			t0 = cl.split("\t");
			track0 = t0[1].strip("\n");
			print("Input track 0: %s"%(track0));
		elif cl.find("track1") > -1:
			t1 = cl.split("\t");
			track1 = t1[1].strip("\n");
			print("Input track 1: %s"%(track1));
		else:
			c = cl.split("\t");
			cut_tstr.append(c[0]);
			cut_titles.append(c[1].strip("\n"));
#Note: this import can't handle empty lines or non-matching lines at the moment.
# this needs to be programmed still

for i in range(len(cut_tstr)):
	print("Cut position found: %s title: %s"%(cut_tstr[i], cut_titles[i]));



# Convert cuts into numbers
t0_cut=cuttools.str2Cut(cut_tstr);
#print("Cut marks selected track0:");
#cuttools.printCuts(t0_cut);

#Now do the cutting

cuttools.cutTrack(track0,t0_cut,cut_titles);

t1_cut = cuttools.addCutOffset(t0_cut,t_offset);
#print("Cut marks selected track1:");
#cuttools.printCuts(t1_cut);
cuttools.cutTrack(track1,t1_cut,cut_titles);
