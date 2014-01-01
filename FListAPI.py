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
				
def getCharProfile(character):
	resp = json.load(urllib2.urlopen("http://www.f-list.net/json/api/character-get.php", urlencode({'name':character, 'warning':1})))
	if u'description' in resp['character']: del resp['character'][u'description']
	if resp[u'error']==u'You may not access this characters data.':
		resp = BeautifulSoup(opener.open("http://www.f-list.net/c/{}".format(quote(character))))
	return resp
	
#stuff like age, species, etc is in here:
def getCharInfo(character):
	resp = opener.open("http://www.f-list.net/c/{}".format(quote(character)))
	soup=BeautifulSoup(resp, convertEntities=BeautifulSoup.HTML_ENTITIES)
	data = str(soup.find('div', {'class':'infodatabox'})).split("<br />")
	res = {u'Age':0}
	for x in data:
		item = re.findall('<span class=.*>(.*):</span>(.*)', x)
		if len(item)>0:
			item = item[0]
			res[item[0]]=item[1].strip()
	return res	

#not yet made for HTML scraping
def getCharKinks(character):
	resp = json.load(urllib2.urlopen("http://www.f-list.net/json/api/character-kinks.php", urlencode({'warning':1,'ticket':config.key, 'account':config.account, 'name':character})))	
	#if u'error' in resp.keys():
		#data = BeautifulSoup(opener.open("http://www.f-list.net/c/{}".format(character)))
	return resp	

#could intergrate into main?
def getAge(name):
	age = getCharInfo(name)['Age']
	try: 
		age = int(re.search('(\d{1,5})', age).group(0))
	except:
		age = 0
	return age

def getKey():
	key = json.load(urllib2.urlopen(loginAPI, urlencode({'account': config.account, 'password': config.password})))['ticket']
	return key