##1dbdc6da34094db4e661ed43aac83d91
import traceback
import random

def lottery(self): #callable main function
	self.say(random.choice(self.channel.users), 2)
		
def __init__(self):
	try:
		self.cf_list[".lottery"]="lottery" #this maps to the function to be executed on command receiving.
		self.cf_levels['.lottery']=2 #0 - creator only, 1 - admin, 2 - public
		self.cf_access_types['.lottery']=[0,1,2] #execute if message from 0- direct, 1 - nick in chan, 2 - chan
		self.dict_help[".lottery"]="Chooses a random user from the channel. S/h/it may win a fabulous prize!"
	except Exception as error:
		self.writeLog("---Error initializing plugin 'lottery': {}".format(error), 2)
		self.noteError()
		traceback.print_exc()