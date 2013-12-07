##1dbdc6da34094db4e661ed43aac83d91
import httplib
import re
import time
import traceback
import urllib2
import random

from BeautifulSoup import BeautifulSoup

imagetypes=['png', 'jpg', 'gif', 'peg', 'bmp', 'tga']
datatypes=['zip', 'rar', 'dat']
badtags=['NWS', 'NSFW', 'NMS', 'NSFL', 'Gore', 'Naughty', 'Not safe for', 'Sexy', 'Fuck', 'cock', 'balls']
joke=["might show you his {LINK}, but not before you buy him dinner.", "grumbles, opening his pocket and fishing out a {LINK}.", "shoves {NAME} onto the ground. \"My {LINK}? Above your pay grade.\"", "blushes. \"{NAME}, w-what are you suggesting? In public, too...\" He squirms.", "does something undescribable to {NAME}. And nobody mentioned {LINK} ever again.", "pours {NAME} a nice, hot cup of tea. \"We can look at {LINK} later. For now, why don't you tell me about yourself?\"", "never has any {LINK} before noon, on principle."]

def links(self):
	if len(self.linklist)==0:
		self.say("Unable to comply: Link database is empty.", 0)
		return
	try:
		if self.args[0]=="-t":
			self.args=self.args[1:]
			if not int(self.args[0].split(':')[0]) in range(24):
				raise ValueError
			results=[]
			for x in self.linklist:
				if x[1]>self.args[0]:
					results.append(x)
				if len(results)==10:
					break
			self.say("Links since {} GMT (up to 10):".format(self.args[0]), 0)
			for x in results:
				self.say(u"[{}] {}: {} ({})".format(x[1], x[0], x[2], x[3]), 0)
	
		elif self.args[0]=="-u":
			results=[]
			exact = False
			try:
				if self.args[1]=="-e":
					exact = True
					self.args=self.args[2:]
			except IndexError: pass
			if not exact: pos = self._rootget(self.args[1])[2]
			a = self.args[1]
			for x in self.linklist:
				if exact:		
					if x[0]==self.args[0]:
						results.append(x)
				else:
					if x[0] in pos:
						results.append(x)
				
				if len(results)==10:
					break
			if exact: self.say("Last links from {} (up to 10):".format(a), 0)
			else: self.say("Last links from {} and associated nicks (up to 10):".format(a), 0)
			for x in results:
				self.say(u"[{}]: {} ({})".format(x[1], x[2], x[3]), 0)
		
		elif self.args[0]=='-p':
			del self.linklist
			self.linklist=[]
			self.say("Linklist successfully purged.", 0)
			
			
		
		else:
			try:
				n = int(self.args[0])
				self.say("Repeating last {} links:".format(n), 0)
				for x in self.linklist[-n:]:
					self.say(u"[{}] {}: {} ({})".format(x[1], x[0], x[2], x[3]) ,0)
				return
				
			except ValueError:
				raise ValueError
				
			
	except IndexError:
		self.say("Repeating last links, up to 5:", 0)
		for x in self.linklist[-5:]:
			self.say(u"[{}] {}: {} ({})".format(x[1], x[0], x[2], x[3]) ,0)
		return
		
		
	except ValueError:
		self.say("Syntax error: '{}' not recognized as a number.".format(self.args[0]), 0)
		
	else:
		self.say("Command successfully completed.", 0)
	
def bytes(b):
	b = float(b)
	if b >= 1048576:
		mb = b / 1048576
		size = '{:,.2f} megabytes'.format(mb)
	elif b >= 1024:
		kb = b / 1024
		size = '{:,.2f} kilobytes'.format(kb)
	else:
		size = '{:,.2f} bytes'.format(b)
	return size
				
def loop(self):
	flag = False
	try:
		if self.command=="332" or self.command=="TOPIC": #or self.NICK in self.prefix:
			return
		
		link = www_re.search(self.params)
		if link:
			if (link.group(3) or link.group(4)) and link.group(5):
				a, b, c = self._process_source(self.prefix)
				link = link.group(5)
				if black_re.search(link):
					self.writeLog("Attempted local IP parse by {} {} {}".format(a, b, c), 1)
					reply = random.choice(joke).replace('{LINK}', link)
					reply = reply.replace('{NAME}', a)
					self.say(reply, 3)
					return
				else:
					y = 0
					for x in badtags:
						if self.params.find(x)!=-1:
							y += 1
							if x in ['NMS', 'NSFL']: y += 4
					if y>0: tag = 'NSFW'
					if y>2: tag = 'Very NSFW'
					if y>5: tag = 'Oh God Why'
					else: tag = 'Not tagged'
					url = "http://{}".format(link)
					self.linklist=self.linklist[-29:]
					self.linklist.append((a, time.strftime("%H:%M"), url, tag))
					flag = True
		if flag:				
			yt=yt_re.match(url)
			if yt:
				return
			if url[-3:] in imagetypes:
				return
		
			else:
				if not url[-3:] in datatypes:
					soup = BeautifulSoup(opener.open(url))						
					self.say(u"\x0309{}\x03".format(soup.title.string), self.access_type)
							
	
	except Exception as error:
		traceback.print_exc()
	
def __init__(self):
	try:
		self.cf_list['.links']="links"
		self.cf_levels['.links']=2
		self.cf_access_types['.links']=[0,1,2]
		self.dict_help[".links"]="Repeats the last <x> links (.links <x>), 10 links since a time (in GMT) (.links -t <HH:MM>) or 10 links mentioned by a user (.links -u <user>)."
		self.linklist=self.loadData('links', tuple)
		
		www_re = re.compile('(((http|https)://)|(www\.))+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?') 
		black_re=re.compile('(localhost)+|^(192\.168\.)+|^(10\.)+|^(127\.)+|^(172\.(1[6-9]|2\d|31)\.)')
		yt_re=re.compile('((http|https)://)?(www\.)?(youtube\.com/|youtu\.be/)(watch\?v=)?([\S]{11})')
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	
	except Exception as error:
		self.writeLog("Error initializing plugin 'links': {}".format(error), 2)
		self.noteError()
		traceback.print_exc()
		
def exit(self):
	self.saveData(self.linklist[:30], 'links')