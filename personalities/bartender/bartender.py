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

lines = utils.loadData('bartender', dict, './personalities/bartender/')

class Functions():
	def JCH(FListProtocol, msg):
		line = eval(random.choice(lines['join']))
		if random.random<0.6:
			FList.say("Bartender Personality JCH! Welcome, new user.")
	
	def telling(FListProtocol, msg):
		pass
		# messages = FListProtocol._telling(msg.source.character.name)
		
def __init__(datapipe):
	print("\tBartender personality successfully loaded. HERE WE GO!")
	#datapipe.personality.lines = utils.loadData('bartender', '\personalities\bartender\\')

def test():
	print("\tBartender.py successfully called test()\n")
	
def handle(FListProtocol, msg):
	try:
		func = getattr(Functions, msg.cmd)
		if callable(func): func(FListProtocol, msg)
	except AttributeError: pass
	
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
