#from __future__ import unicode_literals
import config
import datetime
import json
from urllib import urlencode
import urllib2
import time
import traceback
import yaml
import re

def log(text, ltype=0, channel="System"):
	"""Merely dresses up text with a timestamp and prints it (ltype 0), writes to '<BOT> events.log' (ltype 1), or '<BOT> errors.log' (ltype 2), or '<BOT> conversation.log'(type 3)"""
	try:
		text=text.encode('utf-8', 'ignore')
	except:
		print("Illegal character in string: "+text)
	files=['', ' events', ' errors', channel]
	print("{} -- ({}) {}".format(time.strftime("%c"), channel, text))
	text="{} -- {}".format(time.strftime("%c"), text)
	if ltype==0: return
	channel = re.sub("[^A-Za-z0-9-_]", "_", channel)
	text=text.encode('ascii', 'replace')
	try:
		with open('./logs/{} ({}).log'.format(config.character, channel, files[ltype]), 'a') as io:
			io.write(text+"\n")

	except IOError:
		a = open('./logs/{} ({}).log'.format(config.character, channel, files[ltype]), 'w')
		a.write(text+"\n")
		a.close()	

def loadData(file, expected=dict, path='./data/'):
	try:
		with open(path+file+".yml", 'r') as inp:
			obj = yaml.load(inp)
		return obj

	except IOError:
		print("File does not exist in {}: '{}.yml' Creating empty file and returning an empty {}...".format(path, file, expected))
		return expected()		
	except:
		traceback.print_exc()
		
	
def saveData(data, file, path='./data/'):
	"""Serializes data as YAML object and outputs to <file> in <path> (default path is './data/')"""
	with open("{}{}.yml".format(path, file), 'w') as out:
		yaml.dump(data, out)
		
def timeCalc(t):
	"""Re-calculates a timedelta object to output <weeks>, <days>, <hours>, <minutes>, <seconds> ago instead of just days/seconds.
	Variables: t (datetime delta object)
	NOW NO LONGER DEPENDANT ON 'PROPER ORDER'"""
	days = t.days
	minutes, seconds = divmod(int(abs(t.seconds + (t.microseconds/1e+6))), 60)
	hours, minutes = divmod(minutes, 60)
	if abs(days)!=days:
		print "Negative days!"
		sum = days*24 + hours
		sum = abs(sum)
		days, hours = divmod(sum, 24)
	weeks, days = divmod(days, 7)
	bluh =[(weeks, 9999), (days, 7), (hours, 24), (minutes, 60), (seconds, 60)]
	for num, item in enumerate(bluh):
		if item[0]>item[1]:
			bluh[num-1][0]+=1
			bluh[num][0]=0
	s = ""
	results = [weeks, days, hours, minutes, seconds]
	items = ["week", "day", "hour", "minute", "second"]
	nonzero=[]
	for x, result in enumerate(results):
		if results[x]>0: nonzero.append("{:.0f} {}{}".format(result, items[x], "s"*(result>1)))
	if len(nonzero)>1:
		s=", ".join(nonzero[:-1])
		s+=" and {}".format(nonzero[-1])
	else: s="".join(nonzero)
	s=s.strip()
	return (s, (weeks, days, hours, minutes, seconds))
	
	#check this code
def timeFrac(t):
	"""Short format timeCalc, approximating a fraction.
	Variables: t (datetime delta object)"""
	lt = timeCalc(t)[1]
	unit = ['w', 'd', 'h', 'm', 's']
	maxima = [0, 7.0, 24.0, 60.0, 60.0]
	fractions = ["", u"\xBC", u"\u00BD", u"\u00BE", ""]
	#fractions = ["0", "1/4", "1/2", "3/4", "0"]
	# 			0		1/4		1/2		3/4	
	for x, dp in enumerate(lt):
		if dp==0:
			continue
		else:
			a = dp
			b = 0
			for y in range(x+1, len(lt)):
				b+= lt[y]/maxima[y]
			c = int(round(b, 1)//0.25)
			if b>0.8: 
				a+=1
				b=0
				c=0
			#print "a:{} b:{} c:{}, x:{}".format(a, b, c, x)
			#d = u"{}{}{}".format(a, fractions[c]*(x>3), unit[x]) WHY THIS??
			d = u"{}{}{}".format(a, fractions[c], unit[x])
			return (d, (a, c, unit[x]))
			
statsDict = loadData('{} stats'.format(config.character), dict)
