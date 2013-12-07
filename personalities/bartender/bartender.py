import personality
#from cogito import config?
#how to access config.character?
#eval all lines in cogito itself?
#return s, sArgs instance
#sArgs is a dummy class containing the needed things to complete
#s has its insertions converted to sArgs.<item>, sArgs instance delivered along - .format via eval in cogito core?
import FListAPI
import random
import utils

def JCH(datapipe, msgobj):
	if msgobj.source.character.name!=config.character:
		if random.random<0.6:
			FList.say("Bartender Personality JCH! Welcome, new user.")
	

def __init__(lines):
	print("\tBartender personality successfully loaded. HERE WE GO!")

def test():
	print("\tBartender.py successfully called test()")
	
#can i even refer to this i dunno
#as test shows, you can
def telling(datapipe, msgobj):
	nmes = len(messages)
	if recipient in FList.users.keys():
		userdata=FList.users[recipient]
	else:
		userdata = FListAPI.getCharData(recipient)
	line = random.choice(lines['telling']).format()
	FList.say(line)
	
	for num, item in enumerate(messages):
		d = timeFrac(datetime.datetime.now()-x[2])[0]
	
#drink maker
#customer statistics, seen before, yaml file of... customer? class customer()
def createDrink(datapipe, msgobj):
	pass
	
def recallDrink(datapipe, msgobj):
	pass
	
def serveDrink(datapipe, msgobj):
	pass
	
def calculatePrice(datapipe, msgobj):
	pass
	
def barTab(datapipe, msgobj):
	pass
