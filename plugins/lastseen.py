#1dbdc6da34094db4e661ed43aac83d91
import datetime
import random
import traceback
import utils

actions=["slaps NAME with a large trout.", "strokes NAME's hair fondly.", "facepalms.", "chuckles at NAME.", "looks up at NAME.", "just kind of stares at you.", "gives a toothy smile.", "bows.", "flips the fuck out.", "breaks down sobbing.", "looks anguished.", "fixes NAME with a cool stare."]
things=["is right behind you.", "is online right now.", "died three years ago.", "is, like, right there.", "is in this very room!", "has been inside you all along.", "is here. Why are you using this command?", "questioned the ouija dicks. thats the spooky thing about penis ouija you can never be sure who did the dicks. was it you or me or maybe a ghoooost???", "will be with us again shortly.", "haben wir nicht. Kriegen wir auch nicht mehr rein.", "never was.", "was tasty.", "Error code 404."]

def lastseen(self, msgobj, mode=0, mrec=0):
	"""Database of when a user was last seem. Refreshed on receiving their QUIT or PART.
	Looks up in dict, attempts to save [add: and rebuild if it fails.]
	"""
	try:
		user = msgobj.source.character.name
		if msgobj.params in msgobj.source.channel.users:
			action = random.choice(actions)
			thing = random.choice(things)
			reply="{} \"{} {}\"".format(action, msgobj.params, random.choice(things))
			if msgobj.params==user:
				self.reply("You are right in front of me.", msgobj)
				return
			if msgobj.params==self.character:
				reply = reply.replace(self.character, "I")
				reply = reply.replace(" is", "'m")
				reply = reply.replace("has", "have")
			reply=reply.replace("NAME", user)
			self.reply(reply, msgobj, 3)
			return
		
		else:
			try:
				data = self.lastseenDict[msgobj.params]
				delta = datetime.datetime.now()-data
				self.reply("{!s} was last seen on {}; {} ago.".format(msgobj.params, data.strptime("%A, %d.%m.%Y %H:%M"), utils.timeCalc(delta)[0]), msgobj)
				
			except:
				traceback.print_exc()
				raise KeyError
					
			else:
				return
			
	except KeyError:
		self.reply("Unable to comply: No entry for subject '{!s}' found. Please make sure the name is properly spelled and capitalized.".format(msgobj.params), msgobj, 0)
		
	except:
		traceback.print_exc()

def __init__(self):
	try:
		self.lastseenDict=utils.loadData('lastseen', dict)
		self.functions[".ls"]=("lastseen", 2, [0,1,2])
		self.helpDict[".ls"]="Shows when a user was last seen (by the bot). Usage: .ls <Username>"
	except:
		self.writeLog("Error initializing plugin 'lastseen':", 2)
		self.noteError()
		
def exit(self):
	try:
		for x in datapipe.channelDict:
			for user in x.users:
				user = datapipe.getUser(user).name
				datapipe.lastseenDict[user]=datetime.datetime.now()
	except IndexError:
		pass
	utils.saveData(self.lastseenDict, 'lastseen')