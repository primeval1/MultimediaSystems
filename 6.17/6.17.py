import  numpy as np
import subprocess as sp
import shlex
import json
from PIL import Image

#CONSTANTS
FFMPEG_BIN= 'C:/ffmpeg/bin/ffmpeg.exe'
FFPROBE_BIN = "C:/ffmpeg/bin/ffprobe.exe"
VIDEO_PATH = 'C:/Users/Dimitris/PycharmProjects/pikrakis/6.17/media/blocks.mp4'

def experimentalFunction():
    result = findVideoResolution(VIDEO_PATH)

    command = [FFMPEG_BIN,
               '-i', VIDEO_PATH,
               '-f', 'image2pipe',
               '-pix_fmt', 'rgb24',
               '-vcodec', 'rawvideo', '-'
               ]
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
    raw_image = pipe.stdout.readline(result[0] * result[1] * 3)
    # transform the byte read into a numpy array
    image = np.fromstring(raw_image, dtype='uint8')
    image = image.reshape((result[0], result[1], 3))
    img = Image.fromarray(image, 'RGB')
    img.show()
    pipe.stdout.flush()

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
    cmd = FFMPEG_BIN    +" -i "+pathToInputVideo+" -vf select='between(t,2,6)+between(t,15,24)' -vsync 0 out%d.png"
    command = [FFMPEG_BIN,
               '-i', pathToInputVideo,
               '-vf', "select='between(t,2,6)+between(t,15,24)",
               '-vsync', '0',
               '-vcodec', 'rawvideo', '-'
               ]








