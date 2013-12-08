##1dbdc6da34094db4e661ed43aac83d91
import traceback
import random

def lottery(self): #callable main function
	self.say(random.choice(self.channel.users), 2)
		
def __init__(self):
	try:
		self.functions[".lottery"]=("lottery", 2, [0,1,2])
		self.helpDict[".lottery"]="Chooses a random user from the channel. S/h/it may win a fabulous prize!"
	except Exception as error:
		self.writeLog("---Error initializing plugin 'lottery': {}".format(error), 2)
		self.noteError()
		traceback.print_exc()