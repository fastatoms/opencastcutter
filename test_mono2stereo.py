#!/usr/bin/env python

"""test_mono2stereo.py: Test conversion from mono to stereo"""

__author__      = "Sebastian Loth"
__copyright__   = "Copyright 2020, University of Stuttgart, Institute FMQ"

from cuttools import cuttools
import os

target_folder = "G:/Geteilte Ablagen/ExpPhys Aufzeichnung/ExpPhys 1/Aufzeichnungen live-Vorlesung WS2020/2020_11_05"
infile = "20-11-05-01_Organisatorisches.mp4"

ct = cuttools()
ct.mono2stereo(os.path.join(target_folder, infile),0)
