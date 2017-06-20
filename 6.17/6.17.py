import  numpy as np
import subprocess as sp
import shlex
import json
import os
from PIL import Image

#CONSTANTS
FFMPEG_BIN= 'C:/ffmpeg/bin/ffmpeg.exe'
FFPROBE_BIN = "C:/ffmpeg/bin/ffprobe.exe"
VIDEO_PATH = 'C:/Users/Dimitris/PycharmProjects/pikrakis/6.17/media/blocks.mp4'
VIDEO_OUTPUT = 'C:/Users/Dimitris/PycharmProjects/pikrakis/6.17/results/video/out.mp4'
ARR_OF_FRAMES = []
IMG_SIZE = []

def quantizeImg(int, imgArr,imgHeight):
    for i in range(imgHeight):
        imgArr[i][:] = [x / int for x in imgArr[i]]
        imgArr[i][:] = [x * int for x in imgArr[i]]
    return imgArr

def count_images(in_directory):
    joiner= (in_directory + os.path.sep).__add__
    return sum(
        os.path.isfile(filename)
        for filename
        in map(joiner, os.listdir(in_directory))
    )

def findDifferences(i,imgHeight,imgWidth):
    for k in range(imgHeight):
        for j in range(imgWidth):
            ARR_OF_FRAMES[i][k][j] -= ARR_OF_FRAMES[i-1][k][j]

def restructFromDifferences(i,imgHeight,imgWidth):
    for k in range(imgHeight):
        for j in range(imgWidth):
            ARR_OF_FRAMES[i][k][j] += ARR_OF_FRAMES[i - 1][k][j]

def findVideoResolution(pathToInputVideo):
    cmd = FFPROBE_BIN+" -v quiet -print_format json -show_streams"
    args = shlex.split(cmd)
    args.append(pathToInputVideo)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    ffprobeOutput = sp.check_output(args).decode('utf-8')
    ffprobeOutput = json.loads(ffprobeOutput)

    # find height and width
    height = ffprobeOutput['streams'][0]['height']
    width = ffprobeOutput['streams'][0]['width']
    result = [height,width]

    return result

def createVideoFromFrames(path,imgHeight,imgWidth):
    command = [FFMPEG_BIN,
               '-y',  # (optional) overwrite output file if it exists
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-s', str(imgWidth)+'x'+str(imgHeight),  # size of one frame
               '-pix_fmt', 'rgb24',
               '-r', '24',  # frames per second
               '-i', '-',  # The imput comes from a pipe
               '-an',  # Tells FFMPEG not to expect any audio
               '-vcodec', 'mpeg', path]

    pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)
    for frame in ARR_OF_FRAMES:
        pipe.stdin.write(frame.tostring())


def framesToImages(pathToInputVideo):
    command = [FFMPEG_BIN,
               '-i', pathToInputVideo,
               '-vf', "select='between(t,0,3)",
               '-vsync', '0', 'C:/Users/Dimitris/PycharmProjects/pikrakis/6.17/results/out%d.png'
               ]
    p = sp.Popen(command)

nuOfFrames = count_images('results')
RESOLUTION =  findVideoResolution(VIDEO_PATH)

for i in range(nuOfFrames):
    print(i)
    im = Image.open("results/out"+str(i+1)+".png")
    imgArr = np.array(im)
    imgHeight = im.height
    imgWidth = im.width
    imgArr =  quantizeImg(10,imgArr,imgHeight)
    ARR_OF_FRAMES.append(imgArr)

print("finish appending of frames")
for i in range(nuOfFrames):
    if i != 0 : findDifferences(i,RESOLUTION[0],RESOLUTION[1])

print("finish finding differences")

for i in range(nuOfFrames):
    print(i)
    if i != 0: restructFromDifferences(i, RESOLUTION[0], RESOLUTION[1]);

createVideoFromFrames(VIDEO_OUTPUT,RESOLUTION[0],RESOLUTION[1])









