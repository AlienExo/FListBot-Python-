#1dbdc6da34094db4e661ed43aac83d91
import httplib
import re
import time
import traceback
import urllib2
import random

from BeautifulSoup import BeautifulSoup

www_re = re.compile('(((http|https)://)|(www\.))+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?') 
black_re=re.compile('(localhost)+|^(192\.168\.)+|^(10\.)+|^(127\.)+|^(172\.(1[6-9]|2\d|31)\.)')
yt_re=re.compile('((http|https)://)?(www\.)?(youtube\.com/|youtu\.be/)(watch\?v=)?([\S]{11})')
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
imagetypes=['png', 'jpg', 'gif', 'peg', 'bmp', 'tga']
datatypes=['zip', 'rar', 'dat']
joke=["might show you his {LINK}, but not before you buy him dinner.", "grumbles, opening his pocket and fishing out a {LINK}.", "shoves {NAME} onto the ground. \"My {LINK}? Above your pay grade.\"", "blushes. \"{NAME}, w-what are you suggesting? In public, too...\" He squirms.", "does something undescribable to {NAME}. And nobody mentioned {LINK} ever again.", "pours {NAME} a nice, hot cup of tea. \"We can look at {LINK} later. For now, why don't you tell me about yourself?\"", "never has any {LINK} before noon, on principle."]
					
def loop(self, msgobj):
	flag = False
	try:	
		link = www_re.search(msgobj.params)
		if link:
			if (link.group(3) or link.group(4)) and link.group(5):
				link = link.group(5)
				if black_re.search(link):
					areply = random.choice(joke).replace('{LINK}', link)
					areply = areply.replace('{NAME}', msgobj.source.character.name)
					self.reply(areply, msgobj, 3)
					return		
			url = "http://{}".format(link)
			yt=yt_re.match(url)
			if yt:
				return
			if url[-3:] in imagetypes:
				return
			else:
				if not url[-3:] in datatypes:
					soup = BeautifulSoup(opener.open(url), convertEntities=BeautifulSoup.HTML_ENTITIES)						
					self.reply("{}".format(soup.title.string.strip()), msgobj, 2)
	except Exception as error:
		traceback.print_exc()
	
def __init__(self):
	try:
		pass	
	except Exception as error:
		self.writeLog("Error initializing plugin 'links': {}".format(error), 2)
		self.noteError()
		traceback.print_exc()