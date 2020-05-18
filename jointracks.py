#!/usr/bin/env python

"""jointracks.py: Join the tracks track0 and track1 into one video with track1 overlaid onto track0"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"


from cuttools import cuttools
from datetime import datetime

#load a list of clips to join
clips_file = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/clips.txt";
cuts = "C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/cuts.txt";

clips=[];
with open(clips_file,"r") as cf:
	for cl in cf:
		clips.append(cl.strip("\n").split("\t"));
	cf.close();
#clips is now an array of arrays in the form of
#[ [clip0_track0, clip0_track1], [clip1_track0, clip1_track1],...]
#print(repr(clips));

#load experiment markers and cut markers from cuts file
exp_tstr = [];
cut_tstr = [];
cut_titles = [];
with open(cuts,"r") as cf:
	for cl in cf:
		if cl.find("E\t") > -1:
			em = cl.strip("\n").split("\t");
			exp_tstr.append([em[1], em[2]]);
			print(f"Found Experiment marker. Start: {em[1]} End: {em[2]}");
		elif cl.find("C\t") > -1:
			c = cl.split("\t");
			cut_tstr.append(c[1]);
			cut_titles.append(c[2].strip("\n"));
			print(f"Found Cut marker. {c[1]}");
		else:
			print("ignored unknown command");
	cf.close();
#convert cut time strings into timestamps
cut_t=cuttools.str2Cut(cut_tstr);
#print("Cut time markers:");
#print(repr(cut_t));
#now cut_t is a list of cut marks

#convert experiment time string into timestamp
Nexp = len(exp_tstr);
exp_t = [];
for i in range(Nexp):
	cm = exp_tstr[i];
	ct = [datetime.strptime(cm[0],"%H:%M:%S"), datetime.strptime(cm[1],"%H:%M:%S")];
	exp_t.append(ct);
#now exp_t is a list of [experiment start, experiment end] in the time format of absolute time in full track
#print("Experiment time markers");
#print(repr(exp_t));


#convert cut times into clip intervals
Nclips = len(cut_t)-1;
clip_t = [];
for i in range(Nclips):
	clip_t.append([cut_t[i],cut_t[i+1]]);
#now clip_t is a list of [clip_start, clip_end] in the time format of absolute time in full track
#print("Clip time marker:");
#print(clip_t);

#Now identify experiments for each clip and convert their timestamps to seconds
clip_exp_t = [];
for i in range(Nclips):
	cclip = clip_t[i];
	print(f"Checking clip {i}");
	clip_exp_t.append([]);
	for j in range(Nexp):
		#compare start and end to current experiment
		cexp = exp_t[j];
		if cclip[0] <= cexp[0] and cclip[1] >= cexp[1]:
			print(f"experiment selected No. {j}");
			#now convert timestamp to total seconds from start of clip
			exp_start = round((cexp[0]-cclip[0]).total_seconds());
			exp_end = round((cexp[1]-cclip[0]).total_seconds());
			clip_exp_t[i].append([exp_start, exp_end]);
#Now clip_exp_t is a list of lists that shows the experiment start and end as seconds from start of each clip.
# If a clip contains no experiment, the entry is []
# If a clip contains one experiment, the entry is [[exp_start(sec), seconds_end(seconds)]]
# If a clip contains two or more experiments, the entry is [[exp1_start(seconds), exp1_end(seconds)], [exp2_start(seconds)...
print("Done selecting clips and experiments. My conclusion is");
print(repr(clip_exp_t));

for i in range(Nclips):
	print(f"----------- Begin joining clip No.: {i} of {Nclips}");
	print(f"            Clip contains these experiments");
	
	print(clips[i][0]);
	print(clips[i][1]);
	print(repr(clip_exp_t[i]));

	cuttools.joinTracks(clips[i][0], clips[i][1],clip_exp_t[i]);

	print(f"----------- DONE  joining clip No.: {i} of {Nclips}");
	print("");
	
print("I am done with EVERYTHING!");
