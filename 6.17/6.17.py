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
def count_files(in_directory):
    joiner= (in_directory + os.path.sep).__add__
    return sum(
        os.path.isfile(filename)
        for filename
        in map(joiner, os.listdir(in_directory))
    )

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


def framesToImages(pathToInputVideo):
    command = [FFMPEG_BIN,
               '-i', pathToInputVideo,
               '-vf', "select='between(t,0,3)",
               '-vsync', '0', 'C:/Users/Dimitris/PycharmProjects/pikrakis/6.17/results/out%d.png'
               ]
    p = sp.Popen(command)


framesToImages(VIDEO_PATH)









