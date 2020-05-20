# opencastcutter
Python class and scripts to cut the dual stream videos of open cast lecture recordings.

# Basic working principle
The goal is to provide an easy method to cut and re-encode lecture recordings into smaller video clips.

# Cutting of stream into clips
As the lecture recordings feature two parallel video streams (typically named track-0.mp4 and trach-1.mp4), the procedure to cut the entire lecture into smaller streams is done as follows:
1. Select which track contains the stage view (labeled track0 throughout program) and which track contains the whiteboard view (labeled track1 throughout program).
2. Determine time offset between track0 and track1. Positive time offset means that things happen later in track1 compared to track0.
3. Make a list of cut marks and save them together with some additional information in a text file cuts.txt
4. Run script cutstream.py.
The script import cut marks and clip titles from cuts.txt. Then use FFMPEG fast copy functionality to save portions of track0 and track1 into clips. The clips are named track<trackno>-<clipno>-<title>.mp4, .e.g. track0-01-Introduction.mp4. In the cutting process the script takes care that time offset between track0 and track1 is removed. So, this should be the first thing to do to a lecture recording.

