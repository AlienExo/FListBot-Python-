# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import config
import json
from urllib import urlencode, quote
import urllib2
import utils
import re
import traceback

opener = urllib2.build_opener()
opener.addheaders.append(('Cookie', 'warning=1'))
loginAPI =	"http://www.f-list.net/json/getApiTicket.php"
#Returns JSON with: 
	#datetime_changed, pageviews, name, created, BIG FAT DESCRIPTION.
		#description COOOOULD be parsed for colors/height/size/whatevs but FUCK THAT	
		
"""
def parseFromJSON(data):
	res = {u'Age':0}
	data = data['info']
	for key in data:
		frag = data[key]['items']
"""		
def parseFromHTML(data):
	res = {u'Age':'0'}
	# res = {}
	for x in data:
		item = re.findall('<span class=.*>(.*):</span>(.*)', x)
		if len(item)>0:
			item = item[0]
			res[item[0]]=item[1].strip()
	return res
		
def getCharProfile(character, key):
	#resp = json.load(urllib2.urlopen("http://www.f-list.net/json/api/character-get.php", urlencode({'name':character, 'account': config.account, 'ticket': key, 'warning':1})))
	#if u'description' in resp['character']: del resp['character'][u'description']
	#if resp[u'error']==u'You may not access this characters data.':
	resp = BeautifulSoup(opener.open("http://www.f-list.net/c/{}".format(quote(character))))
	return resp
	
#stuff like age, species, etc is in here:
def getCharInfo(character, key):
	#resp=json.load(urllib2.urlopen("http://www.f-list.net/json/api/character-info.php", urlencode({'name':character, 'account': config.account, 'ticket': key, 'warning':1})))
	#if resp[u'error']==u'You may not access this characters data.':
	resp = opener.open("http://www.f-list.net/c/{}".format(quote(character)))
	soup=BeautifulSoup(resp)
	data = str(soup.find('div', {'class':'infodatabox'})).split("<br/>")
	res = parseFromHTML(data)
	#else:
		# res = parseFromJSON(resp)
		#res = resp
	return res

#not yet made for HTML scraping
def getCharKinks(character, key):
	# resp = json.load(urllib2.urlopen("http://www.f-list.net/json/api/character-kinks.php", urlencode({'warning':1,'ticket':key, 'account':config.account, 'name':character})))	
	# if u'error' in resp.keys():
	data = BeautifulSoup(opener.open("http://www.f-list.net/c/{}".format(quote(character))))
	#quite likely makes a mess of it
	resp = parseFromHTML(data)
	return resp	

#could intergrate into main?
def getAge(name, key):
	age = getCharInfo(name, key)['Age']
	try: 
		age = int(re.search('(\d{1,5})', age).group(0))
	except:
		age = 0
	return age

def getKey():
	key = json.load(urllib2.urlopen(loginAPI, urlencode({'account': config.account, 'password': config.password})))['ticket']
	return key
