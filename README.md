# opencastcutter
Python class and scripts to cut the dual stream videos of opencast lecture recordings.

# Basic working principle
The goal is to provide an easy method to cut and re-encode lecture recordings into smaller video clips.
As such, the program will work from a short text file that contains the cutting instructions.
It creates several small clips from of one big video, so its working principle is oposite to normal video editing software.
The artistic choices are kept minimal to keep the cutting instructions needed minimal as well.
At present, the program works in two steps:
1. division of input videos (track0 and track1) into smaller clips.
   This process is very fast and retains the original video quality as it does not require rendering.
2. joining of both tracks for each small clip into single videos using overlays.
   This process is time-consuming because the video is rendered again.

All of the cutting and rendering is performed by **ffmpeg**, which is a command line based video rendering program that is very fast.
The python script creates the ffmpeg command for each clip and executes it.


# Procedures
## a) Cutting of streams into clips (`cutstream.py`)
As the lecture recordings feature two parallel video tracks (typically named track-0.mp4 and track-1.mp4), the procedure to cut the entire lecture into smaller streams is done as follows:
1. Select which track contains the stage view (labeled track0 throughout program) and which track contains the whiteboard view (labeled track1 throughout program).
2. Determine time offset between track0 and track1. Positive time offset means that things happen later in track1 compared to track0.
3. Make a list of cut marks and save them together with some additional information in a text file 'cuts.txt'
   (See below for details on the file format)
4. Run script cutstream.py.
   - The script imports cut marks and clip titles from cuts.txt.
   - Then it uses FFMPEG fast copy functionality to save portions of track0 and track1 into clips.
   - The clips are named *track(trackno)-(clipno)-(title).mp4*, .e.g. track0-01-Introduction.mp4.
   - In the cutting process the script takes care that time offset between track0 and track1 is removed.
   - **This should be the first thing to do to a lecture recording.**

## b) Joining tracks into one video (`jointracks.py`)
After cutting the long opencast lecture into smaller clips, it may be desired to join the two tracks (stage and whiteboad view) into one mp4 video that can be uploaded to ILIAS, Youtube etc..
By default the whiteboard view will be overlaid on top of the stage view leaving the bottom portion of the stage view visible. (Because this is where the lecturer is seen in the physics lecture halls of U Stuttgart).
The procedure is as follows:
0. Do the cutting described above.
1. Make a list of experiment intervals. Add this information to the cuts.txt file (see below for details). During the experiment intervals the whiteboard overlay will be paused so that the stage view is fully visible. 
2. Decide whether a perspective correction should be performed on the captures screens visible in the stage view.
   If yes: use this line 'ct.setPerspectiveAdjust("on")' in the jointracks.py
   If no: use this line 'ct.setPerspectiveAdjust("off")' in the jointracks.py
   (See below for details on how to define where exactly the screens are)
3. Run the script 'jointracks.py'
   - The script imports the cut marks and experiment intervals
   - Then it calculates for each movie clip when oberlay should be on and when not
   - Then it renders the video with overlay, color correction and perspective correction.
   - The output will be named *track(trackno)-(clipno)-(title)_joined.mp4*



# Details
## Format of `cuts.txt`
This is an example of the format that the cuts.txt file should have.
```
track0	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-0.mp4
track1	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-1.mp4
offset	-3.2
C	00:00:14	Wiederholung
E	00:00:14	00:01:40
C	00:01:49	Dipolmoment
C	00:13:55	Polarisation
C	00:20:37	_weg
C	00:20:55	Dielektrika in Kondensatoren
E	00:20:58	00:23:26
C	00:37:19	_weg
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
### General rules ###
- This is a Tab delimited list. The separators in each line *must* be Tab stops.
  For example, the *offset* line is typed `offset(Tab)-3.2(Enter)`
### Input track specification ###
- Begin `cuts.txt` file by naming the two raw video streams of the lecture recording.
  ```
  track0	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-0.mp4
  track1	C:/temp/vl041500000-2019-5-29-5-54/2019-5-29-5-54/track-1.mp4
  ```
  `track0` will be used as the stage view showing the lecture hall stage.
  `track1` will be used as the whiteboard view showing what the presenter is writing on the screen.
### Offset between input tracks ###
- Specify offset between track0 and track1
  ```
  offset	-3.2
  ```
  A positive number means that things are happening *later* in track1 compared to track0 and
  a negative number means things in track1 happen earlier than in track0.
### Specify cut marks ###
- Specify cut marks.
  Lines indicating cut marks **must** begin with capital `C`.
  ```
  C	00:00:14	Wiederholung
  C	00:01:49	Dipolmoment
  C 00:13:55	Polarisation
  C	00:20:37	weg
  ```
  The format of a cut mark is
  **C** *(Tab)* **(hours:minutes:seconds)** *(Tab)* **(Title)** *(Enter)*
  The cut marks **must** be in proper order. Clip 1 will be created to have the video content between cut mark 1 and cut mark 2. Clip 2 will run between cut mark 2 and cut mark 3. And so on.
  **Note:**
  To remove part of the video stream from the beginning, simply let the first cut mark begin at a finite time. In the 
  above example, the first 13 seconds of the raw streams will be removed.
  To remove part of the video stram from the end, simply let the last cut mark end before the end of the raw video streams.
  This also means that beginning and end must always be specified.
  To remove pieces in the middle of the video stream, define a cut mark for a video clip to be thrown away.
  If this cut is titles "_weg", the program will (mostly) recognize that this segment is not needed.
### Specify experiment markers ###
- Specify experiment time markes.
  Lines specifying experiments **must** begin with capital `E`
  ```
  E	00:38:33	00:45:22
  ```
  The format of an experiment markers is
  **E** *(Tab)* **(Start hours:minutes:seconds)** *(Tab)* **(End hours:minutes:seconds)** *(Enter)*
  This time interval lets the program know that during this time an experiment was conducted and that the whiteboard overlay should not be shown when the two tracks are joined in the reencoded video.
  **Note:**
  It does not matter where in the cuts.txt file the experiment intervals are specified.
  However, the experiment intervals **must not** overlap cut marks. Meaning, an experiment can begin at the exaxt time of a clip and can end at the exact end of a clip, e.g. like this
  ```
  C	00:00:14	Wiederholung
  E	00:00:14	00:01:49
  C	00:01:49	Dipolmoment
  ```
  but they are not allowed to go bexond. The following example would not work.
  ```
  C	00:00:14	Wiederholung
  E	00:00:14	00:02:55
  C	00:01:49	Dipolmoment
  ```

## Color correction
description will follow.
Color correction is *On* by default. Current correction profile is optimized for physics lecture hall PWR57.3 U Stuttgart 

## Perspective correction
description will follow.
Perspective correction is *On* by default. Current correction profile is optimized for physics lecture hall PWR57.3 U Stuttgart 


## Joining of streams (jointracks.py)
This script can join the two lecture streams (track-0 and track-1) into one .mp4 video. The script assumes that:
- *track0 is the stage view* that shows the lectuerer and the experiment and in the upper part the two screens on which close-ups of the experiment are shown.
- *track1 is the whiteboard view* which shows only the recording of the notebook screen on which the lecturer writes the lecture notes.

### The script provides two views:
- Whiteboard view
  The whiteboard screen is overlayed on the stage and blocks the upper half of the video image.
  The lectuerer is visible in the lower part but the screens in the lecture hall are not visible.
- Experiment view
  The stage view is shown fully. Optionally,  the projector screens which are captured in the video are replaced with perspective and color corrected overlays of these screens.
  
