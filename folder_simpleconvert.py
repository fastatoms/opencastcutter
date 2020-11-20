#!/usr/bin/env python

"""test_simpleconvert.py: Encode all input files in a folder into small size mp4"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"

from cuttools import cuttools
import os

target_folder = "G:/Geteilte Ablagen/Vorlesungen Aufzeichnung/ExpPhys 1/Aufzeichnungen live-Vorlesung WS2020/2020_11_19/HD"

#Obtain list of all files in folder
all_files = [f for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))]
print(all_files)


#Now encode videos into mp4
ct = cuttools()

mp4_list = []
for cf in all_files:
    mp4_list.append(ct.encodeMp4(os.path.join(target_folder, cf)))

print("*** DONE: Here is a list of generated files")
print(mp4_list)
