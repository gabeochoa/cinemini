import wikipedia
import HTMLParser
import cgi
import json
import requests

art = ["Step Brothers"]#, "In Time", "Thor", "Iron Man", "Drive"]

def get_summary(Article):
	return wikipedia.summary(Article)

def get_plot(Page):
	return Page.section("Plot")

def toHtml(string):
	return cgi.escape(string, True)

def fromHtml(string):
	html_parser = HTMLParser.HTMLParser()
	unescaped = html_parser.unescape(my_string)
	return unescaped

def getPageFromJson(apireq, searchstr):
	json_data = requests.get(apireq)
	data = json.loads(json_data.text)
	
	newurl = data['query']['search']

	for i in newurl:
		if str(i['title']).find(searchstr) != -1:
			return (wikipedia.search(i['title'], 1))[0]

def main():
	print("Running summary test")
	for film in art:
		print(film + " "), 
		
		try:
			page = wikipedia.page(film)
		except(wikipedia.exceptions.DisambiguationError):
			apireq = "http://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch="+toHtml(film)+"+incategory:English-language_films"
			page = wikipedia.page(getPageFromJson(apireq, film))

		print("Found page: "),
		print(page.title)

		print(get_summary(page.title))


	print("Running Plot test")
	for film in art:
		print(film + " "),

		try:
			page = wikipedia.page(film)
		except(wikipedia.exceptions.DisambiguationError):
			apireq = "http://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch="+toHtml(film)+"+incategory:English-language_films"
			page = wikipedia.page(getPageFromJson(apireq, film))

		print("Found page: "),
		print(page.title)
		print(get_plot(page))


main()