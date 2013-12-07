#1dbdc6da34094db4e661ed43aac83d91
import traceback
import urllib2
import re
import json

yt_re=re.compile('(?:youtube.com.*v=([\S]{11})|youtu.be/([\S]{11}))')

def lencalc(i):
	minutes = i//60
	hours = minutes//60
	minutes = minutes-(hours*60)
	seconds = i-(hours*60*60 + minutes*60)
	results = [hours, minutes, seconds]
	for x, result in enumerate(results):
		if result == 60:
			result = "00"
			results[x-1]+=1
		elif result<10:
			results[x] = "0{!s}".format(result)
		else: results[x] = str(result)
	if results[0]=="00":
		results = results[1:]
		
	s=":".join(results)
	return s

def loop(self, msg):
	a = yt_re.search(msg.params)
	if a:
		if a.group(1) != None: vid=a.group(1) 
		else: vid=a.group(2)
		url = "https://gdata.youtube.com/feeds/api/videos/{}?alt=json".format(vid)
		response = urllib2.urlopen(url)
		resp = json.load(response)
		response.close()
		data 	= resp['entry']
		title 	= data['title']['$t']
		title 	= title.encode('utf-8', 'replace')
		views 	= int(data['yt$statistics']['viewCount'])
		length 	= data['media$group']['media$content'][0]['duration']
		flength = lencalc(length)
		try:
			rating 	= int(round(data['gd$rating']['average'], 1))
			nrating = int(data['gd$rating']['numRaters'])
		except KeyError:
			rating = 0
			nrating = 0
		msg = "[YouTube] [color=green] {!s} :: {!s} :: {!s} :: {!s} Views :: {!s} Ratings[/color]".format(title, flength, "*"*rating, views, nrating).encode('ascii', 'replace')
		self.reply(msg, 2)
				
def test(url):
		vid = yt_re.search(url).group(1)
		url = "https://gdata.youtube.com/feeds/api/videos/{}?alt=json".format(vid)
		response = urllib2.urlopen(url)
		resp = json.load(response)
		response.close()
		data 	= resp['entry']
		title 	= data['title']['$t']
		views 	= int(data['yt$statistics']['viewCount'])
		rating 	= int(round(data['gd$rating']['average'], 1))
		nrating = int(data['gd$rating']['numRaters'])
		length 	= data['media$group']['media$content'][0]['duration']
		flength = lencalc(length)
		return title

def __init__(self):
	try:
		self.helpDict["YouTube Parser"]="Shows the title of any Youtube or Youtu.be video linked."

	except Exception as error:
		print("Error initializing plugin 'youtube': {}".format(error), 2)
		traceback.print_exc()