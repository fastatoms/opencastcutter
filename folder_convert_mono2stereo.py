#!/usr/bin/env python

"""test_mono2stereo.py: Convert all files in folder from mono to stereo"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"

from cuttools import cuttools
import os

ct = cuttools()

target_folder = "G:/Shared drives/ExpPhys Aufzeichnung/ExpPhys 1/Aufzeichnungen live-Vorlesung WS2020/2020_11_05 for ILIAS"
audio_source_channel = 0


#Obtain list of all files in folder
all_files = [f for f in os.listdir(target_folder) if os.path.isfile(os.path.join(target_folder, f))]
print(all_files)



mp4_list = []
for cf in all_files:
    mp4_list.append(ct.mono2stereo(os.path.join(target_folder, infile),audio_source_channel))

print("*** DONE: Here is a list of generated files")
print(mp4_list)

