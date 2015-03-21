FFMPEG_BINARY = '/usr/local/bin/ffmpeg'

from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate

import os
import re 

def touch(path):
	with open(path, 'a'):
		os.utime(path, None)


data = []

def cvsecs(time):
	if (',' not in time) and ('.' not in time):
		time = time + '.0'
	expr = r"(\d+):(\d+):(\d+)[,|.](\d+)"
	finds = re.findall(expr, time)[0]
	nums = list( map(float, finds) )
	return ( 3600*int(finds[0])
			+ 60*int(finds[1])
			+ int(finds[2])
			+ nums[3]/(10**len(finds[3])))

# Load inputfile.mp4 and select the subclip 00:00:50 - 00:00:60
def clipVideo(inputfile, outputfile, time1, time2):
	if not os.path.isdir("output/temp"):
		os.mkdir("output/temp")

	t1 = cvsecs(time1)
	t2 = cvsecs(time2)

	clip = VideoFileClip(inputfile).subclip(t1,t2)
	if os.path.isfile("output/temp/"+outputfile+".mp4"):
		touch("output/temp/"+outputfile+".mp4")

	clip.to_videofile("output/temp/"+outputfile+".mp4", codec="libx264") 

	return

def combineVideos(outputfile):
	filelist = os.listdir("output/temp/")
	cliplist = []

	for fil in filelist:
		cliplist.append(VideoFileClip("output/temp/"+fil))

	outputclip = concatenate(cliplist)


	if os.path.isfile(outputfile+".mp4"):
		touch(outputfile+".mp4")
	outputclip.to_videofile(outputfile+".mp4", codec="libx264")

	return

def editfilm(videofile, procsrt):
	i = 0
	for timespan in procsrt.keys():
		line = (procsrt[timespan])
		
		first = timespan[0:12]
		second = timespan[16:]
		print(first + " " + second)
		i += 1
		print(videofile)
		clipVideo(videofile, str(i), first, second)
		if(i > 5):
			break

	combineVideos("output/output")

	return
















