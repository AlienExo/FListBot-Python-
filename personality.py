#use getattr() to get "".format() the required arguments?

# lines (dict)
#	telling
#		("line {} with inserts for your {} args", [args])
#	<function>

#[19:13 PM]Exo: And for the Ephebophile we have a nice, chilled cup of "get the fuck out of my channel"
#	program this

import bisect
import datetime
import math
import os.path
import random
import re
import sys
import time
import traceback
import utils

	
#units in relation
def spokenRelativeSize(n, nn):
	"""n - number, nn - max of it. Returns the string for the unit's relation to another, e.g. tiny, huge, enormous, microscopic."""
	try:
		n = float(n)
		sizes={0.01:['microscopic','minuscule'], 0.1:['miniature'],0.2:['mini'],0.25:['tiny'],0.3:[''],0.4:[''],0.5:['little'],0.75:['small'], 1.00:['equal', 'same'],2.00:['generous','jumbo', 'large'],5.00:['sizable','substantial', 'huge'],10.00:['gigantic','vast'],50.00:['colossal','excessive'],100.00:['monumental','immense'],250.00:['titanic','stupendous'],500.00:['supermassive','ginormous'],1000.00:['mind-boggling', 'leviathan']}
		f=n/nn
		k = sizes.keys()
		k.sort()
		bs = bisect.bisect_left(k, f)
		return random.choice(sizes[k[bs]])
	except:
		traceback.print_exc()

def spokenNumber(d):
	try:
		if math.log10(d)>10: return False
	except ValueError:
		pass
	except TypeError: print "Not a number."
	if type(d)==float: 
		a = str(d).split('.')
		for x in a[1]: a.append(x)
		a.pop(1)
	else: a =[str(d)]
	b = []
	for s in a:
		slist=[]
		for x in range(len(s[::3])):
			that = s[::-1][(x*3):(x*3)+3]
			if len(that)<3: 
				that=that+"00"
			slist.append(that[2::-1])
		slist.reverse()
		ones = 	["", "one ", "two ", "three ", "four ", "five ", "six ", "seven ", "eight ", "nine ", "ten ",\
				"eleven ", "twelve ", "thirteen ", "fourteen ", "fifteen ", "sixteen ", "seventeen ", "eighteen ", "nineteen "]
		tens = ["", "ten", "twenty ", "thirty ", "fourty ", "fifty ", "sixty ", "seventy ", "eighty ", "ninety "]
		units = ["", "hundred ", "thousand ", "million ", "billion "]
		swords = []
		for num, part in enumerate(slist):
			pos = len(slist)-num
			swords.append(ones[int(part[0])])
			swords.append("hundred "*(part[0]!='0'))
			q = int(part[1:])
			if q == 0: continue
			if q<20:
				swords.append(ones[q])				
			else:
				swords.append(tens[int(part[1])])
				swords.append(ones[int(part[2])])
			swords.append(units[pos]*(pos>1))
		b.append("".join(swords).strip())
	if len(a)>1: return "{} {} {}".format(b[0], 'point', ' '.join(b[1:]))
	return ''.join(b)
	
def fuzzyNumber(d):
	sd=str(d)
	if len(sd)>2:
		print "Greater"
		sdd=int(sd[-2:])
		sd="{}{}{}".format(sd[:-2], "0"*(sd[-2]=="0"), int(random.gauss(sdd, 0.25)))
		sd=int(sd)
	else:
		sd = int(random.gauss(d, 0.50))
	print sd
	return spokenNumber(sd)
	
#super unfinished
def spokenFraction(d):
	lines = {0:['', ''], 0.25:['', ''], 0.5:['', ''], 0.75:['', '']}
	power = log10(d)
	cat = d//0.25
	return random.choice(lines[cat])

"""	
def spokenColor(hex="ffffff"):
	pass

def fuzzyColor(color=None, hex="ffffff"):
	pass

def detectColor(color="white")
	compare to existing list
	otherwise regex existing list, list all matches, concoct... largest match? Mostly white? Adjectives?

def describeCharacter(char):
	get missing data from FListAPI
		which should scrape profiles that don't let API access. ;)
	complete class instance. if the char's in the channel, add to self.users (otherwise we'll have all of FList downloaded soon. :V)

def termOfAddress(char):
	pass
"""
def timeOfDay():
	return ["night", "morning", "afternoon", "evening"][datetime.datetime.now().hour//6]
	
#---------------------------------------------------------------
	
class Personality():
	def __init__(self, code, lines, path, tglobals, config):
		try:
			self.configref = config
			sys.path.append(path)
			self.code = __import__(code, tglobals)
			print "\tTesting code execution for personality."
			if callable(self.code.test): 
				self.code.test()
			else: raise ImportError
			self.lines = utils.loadData(lines, dict, path)
			
		except Exception as error:
			traceback.print_exc()
			
		except ImportError:
			print ("Cannot call self.code.test. Either the .py does not have it or the import went wrong.")
	
def __init__(config):
	print("Importing personalities. Please stand by.")
	tglobals = globals()
	personality = None
	personalities = {}
	for dirpath, subdirs, files in os.walk("./personalities/"):
		if dirpath=="../personalities/": continue
		if subdirs==[]:
			for x in files:
				if x[-3:]==".py":
					codefile = x
					print ("\tCodefile '"+codefile+"' found. Importing...")
				if x[-4:]==".yml":
					lines = x
					print ("\tLines '"+lines+"' found. Loading...\n")
				path = dirpath+'/'
			personalities[codefile[:-3]]=(Personality(codefile[:-3], lines[:-4], path, tglobals, config))
	print("Import complete.")
	if len(personalities)>0:
		print ("\n Available personalities:")
		choices = {}
		for number, item in enumerate(personalities):
			choices[number+1]=item
			print ("\t{}\t{}".format(number+1, item))
		choice = raw_input("Choose a personality by number (Press Enter for none): ")
		try:
			if choice == '':
				personality = None
				return
			choice = choices[int(choice)]
			print("Personality "+choice+" loaded.\n")
			return personalities[choice]
		except:
			traceback.print_exc()
	else:
		print ("No personality found.\n")
