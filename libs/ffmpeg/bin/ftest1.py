import ffmpeg
(
    ffmpeg
    .input('test1.mp4')
    .hflip()
    .output('out1.mp4')
    .run()
)