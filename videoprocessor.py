FFMPEG_BINARY = '/usr/local/bin/ffmpeg'

from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate
import util
import os
import re 

#create file at path
def touch(path):
	with open(path, 'a'):
		os.utime(path, None)


data = []



# Load inputfile.mp4 and select the subclip 00:00:50 - 00:00:60
def clipVideo(inputfile, outputfile, time1, time2):
	if not os.path.isdir("output/temp"):
		os.makedirs("output/temp")

	t1 = util.cvsecs(time1)
	t2 = util.cvsecs(time2)

	clip = VideoFileClip(inputfile).subclip(t1,t2)
	if os.path.isfile("output/temp/"+outputfile+".mp4"):
		touch("output/temp/"+outputfile+".mp4")

	clip.to_videofile("output/temp/"+outputfile+".mp4", codec="libx264") 

	return

#combines all videos in output/temp/ to the outfile
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

#Will clip the film into the pieces we want and then 
#recombine it all at the end into one film. 
def editfilm(videofile, procsrt):
	i = 0
	for timespan in procsrt.keys():
		line = procsrt[timespan].strip()

		first = timespan[0:12]
		second = timespan[16:]
		print(first + " " + second)
		i += 1
		print(videofile)
		clipVideo(videofile, str(i), first, second)

	combineVideos("output/output")

	return
















