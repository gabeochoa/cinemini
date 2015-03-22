import os
import textprocessor as TP
import videoprocessor as VP
import wapi

import time


def cinemini(inputfile):
	starttime = time.time()
	vidfile, outputsrt = TP.process_srt(inputfile) #reads file name
	#print outputsrt

	if(vidfile != None):
		VP.editfilm(vidfile, outputsrt)
	#print outputsrt
	#print( str(time.time() - starttime) + " seconds")

	return










if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate a compressed version of a film by searching through subtitle tracks.')
    parser.add_argument('--input', '-i', dest='inputfile', required=True, help='video or subtitle file, or folder')
    
    args = parser.parse_args()

    cinemini(args.inputfile)