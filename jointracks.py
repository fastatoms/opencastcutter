#!/usr/bin/env python

"""jointracks.py: Join a dual-track open cast recording (or clip cut from it) into one video with overlays"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"

#Import class for video processing and create cuttools object
from cuttools import cuttools
ct = cuttools()

# -------------------------------------------------------------------------
# -- Instructions go below here

#Lectures 06-28
# cuts = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/vl041500000-2019-6-28-5-54/2019-6-28-5-54/cuts.txt"
# clips_file ="G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/vl041500000-2019-6-28-5-54/2019-6-28-5-54/clips.txt"

#Test cut of additional lecture
folder = "C:/temp/vl041500000-2020-7-3-8-42/2020-7-3-8-42"
cuts_file = "cuts_test.txt"
clips_file = "clips.txt"
ct.setPerspectiveAdjust("on")
ct.setScreenLeft([58, 14], [925, 39], [100, 500], [921, 485])
ct.setScreenRight([940, 38],[1776, 47], [931, 485], [1731, 517])


#2020 Additional lecture part 1
# cuts = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/joined/Zusatzaufzeichnung (fehlerhaft)/2020-07-03-8/cuts_drive.txt"
# clips_file = "G:/Geteilte Ablagen/ExpPhys 2 Skript/SS2019 Aufzeichnung/joined/Zusatzaufzeichnung (fehlerhaft)/2020-07-03-8/clips_drive.txt"
# ct.setScreenLeft([58, 14], [925, 39], [100, 500], [921, 485])
# ct.setScreenRight([940, 38],[1776, 47], [931, 485], [1731, 517])
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


# -------------------------------------------------------------------------
# -- Program execution (no user input required below here)
ct.processJoin(folder,cuts_file,clips_file)



