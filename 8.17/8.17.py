import  numpy as np
import subprocess as sp
import shlex
import json
import os
from PIL import Image
FFMPEG_BIN= 'C:/ffmpeg/bin/ffmpeg.exe'
FFPROBE_BIN = "C:/ffmpeg/bin/ffprobe.exe"
VIDEO_PATH = 'C:/Users/Dimitris/PycharmProjects/pikrakis/8.17/media/blocks.mp4'
VIDEO_OUTPUT = 'C:/Users/Dimitris/PycharmProjects/pikrakis/8.17/results/video/out.mp4'
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

def readFrames(VIDEO_PATH,RESOLUTION):
    command = [FFMPEG_BIN,
               '-i', VIDEO_PATH,
               '-f', 'image2pipe',
               '-pix_fmt', 'rgb24',
               '-vcodec', 'rawvideo', '-']
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
    raw_image = pipe.stdout.read(RESOLUTION[0] * RESOLUTION[1] * 3)
    # transform the byte read into a numpy array
    image = np.fromstring(raw_image, dtype='uint8')
    frames = image.reshape((RESOLUTION[0], RESOLUTION[1], 3))
    # throw away the data in the pipe's buffer.
    pipe.stdout.flush()
    return frames

def divToMacroblock(frame):
    macroblocks = []
    i = 0
    j = 0
    while (i < frame.length) &  (j <frame[0].length):
        macroblock = []
        for i in range(i + 16):
            for j in range(j+16):
                macroblock[i][j] = frame[i][j]

        macroblocks.append(macroblock)
        i += 16
        j += 16
        if((i < frame.length) &  (j <frame[0].length)): #an ksepernaei to mhkos platos, vale macroblcok me 0
            macroblocks.append(np.zeros(16,16))

def plaisioSfalmatwn(frame1,frame2):
    height = frame1.length
    errorArr=[]
    for k in range(height):
        width = frame1[k].length
        for j in range(width):
            errorArr[k][j] = frame2[k][j] - frame1[k][j]
    return errorArr

def compMacroblocks(macroblocksFRM1, macroblocksFRM2):
    height = macroblocksFRM1.length()
    width = macroblocksFRM1[0].length()
    return plaisioSfalmatwn(macroblocksFRM1,macroblocksFRM2) #since k = 16 we need the nextmacroblock

def SAD(macroblocks1,macroblocks2):
    allplaisiasfalmatwn = []
    i = 0
    while i < macroblocks1.length():
        err=[]
        macros=[] #store macrors compared
        if i + 1 <= macroblocks1.length():
            err[1] =  compMacroblocks(macroblocks1[i],macroblocks2[i+1])
            macros[1]= macroblocks2[i+1] #macroblock next
        if i+16 <= macroblocks1.length():
            err[2] = compMacroblocks(macroblocks1[i],macroblocks2[i+16])#macroblock bellow
            macros[2]= macroblocks2[i+16]
        if i-16 >0:
            err[3] = compMacroblocks(macroblocks1[i],macroblocks2[i-16]) #macroblock above
            macros[3] = macroblocks2[i-16]
        if i-1 > 0:
            err[4] = compMacroblocks(macroblocks1[i],macroblocks2[i-1]) #macroblock before
            macros[4] = macroblocks2[i-1]
        plaisiosfalmatwn = min(sum(macros)) #epistrefei to mikrotero plaisio sfalmatwn
        allplaisiasfalmatwn.append(plaisiosfalmatwn)
        i+=1
    return allplaisiasfalmatwn #rerurn the foresighted frame


RESOLUTION = findVideoResolution(VIDEO_PATH)
FRAMES = readFrames(VIDEO_PATH,RESOLUTION)
ERR_FRAMES = []
ERR_FRAMES2 = []

#find error frame between frames
for i in range(FRAMES.length):
   if i!=0: ERR_FRAMES.append(plaisioSfalmatwn(FRAMES[i-1],FRAMES[i]))

#find error frame after SAD selection.
for i in range(FRAMES.length):
    if i != 0:
        framemacro1 = divToMacroblock(FRAMES[i])
        framemacro2 = divToMacroblock(FRAMES[i-1])
        ERR_FRAMES2.append(SAD(framemacro1,framemacro2))

