from collections import OrderedDict
import os
import re
debug = True

usable_extensions = ['mp4', 'avi', 'mov', 'mkv', 'm4v']


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
		# Iterate over each line in the current subtitles file.
		for timespan in lines.keys():
			line = lines[timespan].strip()

			if(process_line(line)):
				output[timespan] = line
	# If no subtitles were found in the current file.
	else:
		if debug:
			print "[!] Subtitle file '" + srt + "' is empty."

	return (videofile, output)

def process_line(Line):
	# check if we need line or not
	return True


'''
	for i in range(len(allParagraphs)):

	for w in words:
		int numTimes = 0
		for w2 in words:
			if w2 == w:
				numTimes++

		map[w] = numTimes #Not python syntax

	words.sortByNumTimes()

	for w in words:
		if w.numTimes < (len(words) - 1)) /2:
			words.remove(w) #make copy of words, can't iterate and remove from list

	words.sortByTime()

	for i in range(len(words) - 1):
		if !(words(i+1).timestamp - words(i).timestamp > 5):
			words.remove(words(i))

	words.removeBetweenTimeStamps(len(subtitles)/i, 2 * len(subtitles))

'''




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







