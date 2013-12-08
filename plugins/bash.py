##1dbdc6da34094db4e661ed43aac83d91
#import urllib
#import urllib2
from BeautifulSoup import BeautifulSoup
#import re
#import time
#import traceback
modules = ['urllib', 'urllib2', 're', 'time', 'traceback']
user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0'
headers = { 'User-Agent' : user_agent }

def BashGet(no="random"):
	"""Random quotes off the Waargh! Bash"""
	request = urllib2.Request('http://bash.waargh.org/{}'.format(no), None, headers)
	response = urllib2.urlopen(request)
	#print "Response: {}".format(response)
	soup = BeautifulSoup(response, convertEntities=BeautifulSoup.HTML_ENTITIES)
	response.close()
	answer = soup.find('p', {"class":"quote"})
	no = answer.find('u', text=True)
	quotetext = []
	word = ''
	for tmp in answer.findAll(text=True):
		tmp = tmp.strip()
		quotetext.append(tmp.encode('utf-8', 'replace'))
	quotetext = quotetext[11:]
	quote = []
	for x in quotetext:
		x = x.replace("\r\n", "")
		quote.append(x)
	
	return quote, no

#bash quotes
def bash(self):
	"""Takes a quote from the url indicated in the config (must follow URL structure). Indicate a number or get a random one."""
	if (time.time()-self.lasttime)<self.bashlim:
		self.say("Bash quotes are limited to once per <{}> seconds.".format(self.bashlim),0)
		return
	try:
		b = int(self.args[0])
		answer, no = BashGet(b)
	except ValueError:
		self.say("Syntax error. Correct usage: .b <number> (none for a random quote)", 0)
		traceback.print_exc()
		return
		
	except IndexError:
		answer, no = BashGet()
		
	if not self.func_type==0:
		send = 2
	else:
		send = 0
		
	self.say("Bash {}:".format(no), send)
	for x in answer:
		self.say(x, 2)
	self.lasttime=time.time()
		
def __init__(self):
	try:
		self.functions['.b']=("bash", 2, [0,1,2])
		self.helpDict[".b"]="Loads a quote from the Waargh! Bash. Leave blank for a random quote. Usage: .b <Number> "
		self.bashlim=15
		self.lasttime=time.time()-15
	except Exception as error:
		self.writeLog("---Error initializing plugin 'bash': {}".format(error), 2)
		self.noteError()
		traceback.print_exc()