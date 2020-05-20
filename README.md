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
   - The script imports cut marks and clip titles from cuts.txt.
   - Then it uses FFMPEG fast copy functionality to save portions of track0 and track1 into clips.
   - The clips are named *track(trackno)-(clipno)-(title).mp4*, .e.g. track0-01-Introduction.mp4.
   - In the cutting process the script takes care that time offset between track0 and track1 is removed.
   - **This should be the first thing to do to a lecture recording.**

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
**Formatting rules:**
- This is a Tab delimited list. The separators in each line *must* be Tab stops.
  For example, the *offset* line is typed `offset(Tab)-3.2(Enter)`
- Begin `cuts.txt` file by naming the two raw video streams of the lecture recording.
  ```
  track0	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-0.mp4
  track1	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-1.mp4
  ```
  `track0` will be used as the stage view showing the lecture hall stage.
  `track1` will be used as the whiteboard view showing what the presenter is writing on the screen.
- Specify offset between track0 and track
  ```
  offset	-3.2
  ```
- Specify cut marks.
  Lines indicating cut marks **must** begin with capital `C`.
  ```
  C	00:00:14	Wiederholung
  C	00:01:49	Dipolmoment
  C   00:13:55	Polarisation
  C	00:20:37	weg
  ```
  The format of a cut mark is **C** *(Tab)* **(hours:minutes:seconds)** *(Tab)* **(Title)** *(Enter)*
  The cut marks **must** be in proper order. Clip 1 will be created to have the video content between cut mark 1 and cut mark 2. Clip 2 will run between cut mark 2 and cut mark 3. And so on.
- Specify experiment time markes.
  Lines specifying experiments **must** begin with capital `E`
  ```
  E	00:38:33	00:45:22
  ```
  The format of an experiment markers is **E** *(Tab)* **(Start hours:minutes:seconds)** *(Tab)* **(End hours:minutes:seconds)**
  This time interval lets the program know that during this time an experiment was conducted and that the whiteboard overlay should not be shown when the two tracks are joined in the reencoded video.
