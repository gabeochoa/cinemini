import os
import textprocessor as TP
import videoprocessor as VP
import wapi


def cinemini(inputfile):
	vidfile, outputsrt = TP.process_srt(inputfile)
	if(vidfile != None):
		VP.editfilm(vidfile, outputsrt)

	return







if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate a compressed version of a film by searching through subtitle tracks.')
    parser.add_argument('--input', '-i', dest='inputfile', required=True, help='video or subtitle file, or folder')
    
    args = parser.parse_args()

    cinemini(args.inputfile)