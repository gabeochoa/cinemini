from collections import OrderedDict
import os
import re
import wapi
import util
import operator
import string
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

from pattern.search import match
from pattern.search import search
from pattern.en import parsetree
from pattern.search import Pattern

rmpat = ["CC","CD","DT","FW","IN","LS","PRP","PRP$","SYM","TO","UH","WRB","INTJ","PART","ADVP"]

def notneeded(word):
	print word, 
	for pos in rmpat:
		p = Pattern.fromstring(pos)
		if(p.scan(word)):
			print " " + pos
			return True
	return False
		
debug = True

usable_extensions = ['mp4', 'avi', 'mov', 'mkv', 'm4v']


def removePunc(word):
	exclude = set(string.punctuation)
	return ''.join(ch for ch in word if ch not in exclude)

#text vars
def getKey(item):
	return item[0]

def process_srt(filename):
	srtfile = get_subtitle_files(filename)

	if debug:
		print("Got Subtitle")

	for ext in usable_extensions:
		tempVideoFile = srtfile.replace('.srt', '.' + ext)
		if os.path.isfile(tempVideoFile):
			videofile = tempVideoFile
			foundVideoFile = True
			if debug:
				print "[+] Found '" + tempVideoFile + "'."

	output = OrderedDict()

	if not foundVideoFile:
		return (None, output)

	lines = clean_srt(srtfile)

	if lines:
		outlines = process_wiki_sum(srtfile.replace('.srt', ''), lines)

		print len(lines)
		print len(outlines)

		# Iterate over each line in the current subtitles file.
		for l, o in outlines:
			for timespan in lines.keys():
				line = lines[timespan].strip()

				if(timespan == o):
					output[timespan] = line
	# If no subtitles were found in the current file.
	else:
		if debug:
			print "[!] Subtitle file '" + srt + "' is empty."
		return (None, None)

	output = OrderedDict(sorted(output.items(), key=lambda t: t[0]))

	#print len(output)
	return (videofile, output)

def process_wiki_sum(filename, lines):



def process_wiki_sum_old(filename, lines):

	name = (filename.split('/'))
	title = name[len(name)-1]
	allParagraphs = wapi.get_plot(title).split("\n")

	paramap = dict()
	paramap2 = dict()
	output = []
	templines = [] 
	templines2 = [] 
	vals = []

	#for each paragraph
	for i in range(len(allParagraphs)):
		
		#for each word in paragraph
		for w in allParagraphs[i].split(' '):
			#check occurence of each word
			numTimes = 0
			w = removePunc(w)

			if(notneeded(w)):
				continue
	
			for w2 in allParagraphs[i].split(' '):
				w2 = removePunc(w2)
				if w2.find(w) != -1 or w.find(w2) != -1:
					numTimes+=1
			#put it in map
			try:
				paramap[w] += numTimes
			except KeyError:
				paramap.update({w : numTimes})

			vals.append(numTimes)

	#print "Word map generated ",

	paramap2 = (sorted(paramap.items(), key=lambda x: x[1], reverse = True))
	
	for line in paramap2:
		print line
	#print paramap
	#print paramap2
	return []



'''
	From VideoGrep Located here:
	https://github.com/antiboredom/videogrep/blob/master/videogrep.py
'''

def convert_timespan(timespan):
    """Converts an srt timespan into a start and end timestamp"""
    start, end = timespan.split('-->')
    start = convert_timestamp(start)
    end = convert_timestamp(end)
    return start, end


def convert_timestamp(timestamp):
    """Converts an srt timestamp into seconds"""
    timestamp = timestamp.strip()
    chunk, millis = timestamp.split(',')
    hours, minutes, seconds = chunk.split(':')
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    seconds = seconds + hours * 60 * 60 + minutes * 60 + float(millis) / 1000
    return seconds

def clean_srt(srt):
	"""Removes damaging line breaks and numbers from srt files and returns a dictionary"""
	with open(srt, 'r') as f:
		text = f.read()
	text = re.sub(r'^\d+[\n\r]', '', text, flags=re.MULTILINE)
	lines = text.splitlines()
	output = OrderedDict()
	key = ''

	for line in lines:
		line = line.strip()
		if line.find('-->') > -1:
			key = line
			output[key] = ''
		else:
			if key != '':
				output[key] += line + ' '

	return output


def get_subtitle_files(inputfile):
	"""Returns a list of subtitle files"""
	srts = []

	if os.path.isfile(inputfile):
		filename = inputfile.split('.')
		filename[-1] = 'srt'
		srts = ['.'.join(filename)]

	elif os.path.isdir(inputfile):
		if inputfile.endswith('/') == False:
			inputfile += '/'
		srts = [inputfile + f for f in os.listdir(inputfile) if f.lower().endswith('srt')]

	else:
		print "[!] No subtitle files were found."
		exit(1)

	return srts[0]







