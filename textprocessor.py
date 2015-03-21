from collections import OrderedDict
import os
import re
import wapi
import util
import operator

debug = True

usable_extensions = ['mp4', 'avi', 'mov', 'mkv', 'm4v']


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

	print len(output)
	return (videofile, output)

def process_wiki_sum(filename, lines):

	#print "Setup Text Process."
		
	name = (filename.split('/'))
	title = name[len(name)-1]
	allParagraphs = wapi.get_plot(title).split("\n")

	paramap = dict()
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
			for w2 in allParagraphs[i].split(' '):
				if w2 == w:
					numTimes+=1

			#put it in map
			paramap.update({w : numTimes})
			vals.append(numTimes)

		#print "Word map generated ",
	

		#words.sortByNumTimes()
		paramap = dict(sorted(paramap.items(), key=operator.itemgetter(1), reverse = True))
		avg = sum(vals)/ len(vals)

		for key in paramap:
			if paramap[key] > avg:
				for timespan in lines.keys():
					line = lines[timespan].strip()
					if line.find(key) != -1:
						templines.append((line, timespan))
			else:
				continue
		
		#print "Word map filtered ",
	

		difflist = []
		for (line, timespan) in templines:
			first = timespan[0:12]
			second = timespan[16:]

			fint = util.cvsecs(first)
			sint = util.cvsecs(second)
			diff = sint - fint
			difflist.append(diff)

		avg2 = sum(difflist)/ len(difflist)
		
		clusters = []
		cluster = 0
		for (line, timespan) in templines:
			first = timespan[0:12]
			second = timespan[16:]

			fint = util.cvsecs(first)
			sint = util.cvsecs(second)
			diff = sint - fint

			if(diff > avg2):
				clusters.append(templines2)
				cluster += 1
				continue;
			else:
				templines2.append( (line, timespan))

		#print "Clusters Generated ",
	
		
		#output lines in cluster closes to paragraph
		pindratio = (i/len(allParagraphs)) #percentage of way through plot
		clusind = len(clusters) * pindratio

		for lin in clusters[clusind]:
			output.append(lin)

		#print "Output complete "

		'''
		for i in range(len(words) - 1):
			if not (words(i+1).timestamp - words(i).timestamp > 5):
				words.remove(words(i))

		words.removeBetweenTimeStamps(len(subtitles)/i, 2 * len(subtitles))

		'''

	return output



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







