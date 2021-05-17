#!/usr/bin/env python

"""folder_convert_mkv2mp4.py: Convert all files in a folder from mkv to mp4"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"

from cuttools import cuttools
import os

target_folder = "G:/Geteilte Ablagen/Vorlesungen Aufzeichnung/ExpPhys 1/Aufzeichnungen live-Vorlesung WS2020/2020_11_19"

#Obtain list of all files in folder
all_files = [f for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))]
print(all_files)


#Now copy videos in mp4 container
ct = cuttools()
mp4_list = []
for cf in all_files:
    mp4_list.append(ct.mkv2mp4(os.path.join(target_folder, cf)))

print("*** DONE: Here is a list of generated files")
print(mp4_list)
