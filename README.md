# opencastcutter
Python class and scripts to cut the dual stream videos of open cast lecture recordings.

# Basic working principle
The goal is to provide an easy method to cut and re-encode lecture recordings into smaller video clips.


# Procedures
## Cutting of stream into clips
As the lecture recordings feature two parallel video streams (typically named track-0.mp4 and trach-1.mp4), the procedure to cut the entire lecture into smaller streams is done as follows:
1. Select which track contains the stage view (labeled track0 throughout program) and which track contains the whiteboard view (labeled track1 throughout program).
2. Determine time offset between track0 and track1. Positive time offset means that things happen later in track1 compared to track0.
3. Make a list of cut marks and save them together with some additional information in a text file cuts.txt
4. Run script cutstream.py.
The script import cut marks and clip titles from cuts.txt. Then use FFMPEG fast copy functionality to save portions of track0 and track1 into clips. The clips are named *track(trackno)-(clipno)-(title).mp4*, .e.g. track0-01-Introduction.mp4. In the cutting process the script takes care that time offset between track0 and track1 is removed. So, this should be the first thing to do to a lecture recording.

### Format of `cuts.txt`
This is an example of the format that the cuts.txt file should have.
```
track0	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-0.mp4
track1	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-1.mp4
offset	-3.2
C	00:00:14	Wiederholung
E	00:00:14	00:01:40
C	00:01:49	Dipolmoment
C	00:13:55	Polarisation
C	00:20:37	weg
C	00:20:55	Dielektrika in Kondensatoren
E	00:20:58	00:23:26
C	00:37:19	weg
C	00:37:52	Ohmesche Leiter (und reale Kondensatoren)
E	00:38:33	00:45:22
C	00:49:01	Leitfaehigkeit
E	01:06:17	01:13:03
C	01:14:29	Leitfaehigkeit von Glas
E	01:14:37	1:21:16
C	01:25:11	Ohmsches Gesetz
E	01:28:04	1:31:43
C	01:31:43	Ende
```
