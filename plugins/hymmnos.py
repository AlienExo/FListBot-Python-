#1dbdc6da34094db4e661ed43aac83d91
#1dbdc6da34094db4e661ed43aac83d91
#!/usr/bin/python
import urllib
import urllib2
import string
import re
import traceback
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 5.1; rv:8.0) Gecko/20100101 Firefox/8.0'
headers = { 'User-Agent' : user_agent }

def translate(words):
	"""Searches the Hymmnoserver for a translation and provides it"""
	vowels = {'LYA':'', 'LYE':'', 'LYI':'', 'LYO':'', 'LYU':'', 'YA':'', 'YE':'', 'YI':'', 'YO':'', 'YU':'', 'A':'', 'E':'', 'I':'', 'O':'', 'U':''}
	emotion=[]
	a = re.compile(r'L?(Y?(A|E|I|O|U))')
	pwords = words
	for x in words:
		for y in vowels.keys():
			if a.search(y)!=-1:
				emotion.append(vowels[y])
				re.sub(y, ".", x)
				break
	words = urllib.urlencode({"word" : words})
	request = urllib2.Request("http://hymmnoserver.uguu.ca/search.php", words, headers)
	response = urllib2.urlopen(request)
	soup = BeautifulSoup(response)
	response.close()
	results = soup.findAll('td', attrs={'style' : 'width: 50%;'})
	source = ''
	translations = []
	for result in results:
		word = ''
		for tmp in result.findAll(text=True):
			word += unicode(tmp).encode("utf-8")
			translations.append((word))
	for word in translations:
		word.replace('.', emotion.pop(0))
	return translations
	
def hymmnos(self, msgobj):
	try:
		words = msgobj.params
		reply = translate(words)
		a=""
		for x in reply:
			x.strip()
			a += "({}) ".format(x)
		a = a.rstrip()
		#self.writeLog ("Translated: \"{} : {}\"".format(words, a))
		self.reply(a, msgobj)

		
	except Exception as error:
		#self.writeLog ("Failed to translate: {}".format(error))
		traceback.print_exc()

def __init__(self):
	try:
		self.functions[".h"]=("hymmnos", 2, [0,1,2])
		self.helpDict[".h"]="Translates from the conlang Hymmnos to English. Usage: .h <Word/sentence>."
	except:
		self.writeLog("Error initializing plugin 'hymmnos'")
		traceback.print_exc()