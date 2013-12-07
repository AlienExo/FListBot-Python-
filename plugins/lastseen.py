##1dbdc6da34094db4e661ed43aac83d91
import datetime
import random
import traceback

actions=["slaps NAME with a large trout.", "strokes NAME's hair fondly.", "facepalms.", "chuckles at NAME.", "looks up at NAME.", "just kind of stares at you.", "gives a toothy smile.", "bows.", "flips the fuck out.", "breaks down sobbing.", "looks anguished.", "fixes NAME with a cool stare."]
things=["is right behind you.", "is online right now.", "died three years ago.", "is, like, right there.", "is in this very room!", "has been inside you all along.", "is here. Why are you using this command?", "questioned the ouija dicks.", "will be with us again shortly.", "haben wir nicht. Kriegen wir auch nicht mehr rein.", "never was.", "was tasty."]

def lastseen(self, mode=0, mrec=0):
	"""Database of when a user was last seem. Refreshed on receiving their QUIT or PART.
	Looks up in dict, attempts to save [add: and rebuild if it fails.]
	"""
	try:
		user = self.source.character
		precise=False
		if self.args[0]==("-e"):
			self.args=self.args[1:]
			precise=True

		if self.args[0] in self.channel.users:
			action = random.choice(actions)
			thing = random.choice(things)
			reply="{} \"{} {}\"".format(action, self.args[0], random.choice(things))
			if self.args[0]==user:
				self.say("You are right in front of me.", self.access_type)
				return
			if self.args[0]==self.NICK:
				reply = reply.replace(self.NICK, "I")
				reply = reply.replace(" is", "'m")
				reply = reply.replace("has", "have")
			reply=reply.replace("NAME", user)
			self.say(reply, 3)
			return
		
		if precise:		
			try:
				data = self.dict_lastseen[self.args[0]]
				delta = datetime.datetime.now()-data
				self.say("{!s} was last seen on {}; {} ago.".format(self.args[0], data.strptime("%A, %d.%m.%Y %H:%M"), self._timecalc(delta)[0]), self.access_type)
				
			except:
				traceback.print_exc()
				raise KeyError
				
				
			else:
				return
				
		timelist = []
		print self.args[0]
		y = self._rootget(self.args[0])[2]
		print y
		
		if y:
			for x in y:
				for z in self.dict_lastseen.items():
					if x == z[0]:
						timelist.append(z[1])
			timelist.sort()
			
			if len(timelist)==0:
				raise KeyError
				
			else:
				timelist = timelist.pop()
				for x in self.dict_lastseen.items():
					if x[1]==timelist and x[0] in y:
						lastname = x[0]
				delta = datetime.datetime.now()-timelist
				self.say("{!s} was last seen as {!s} on {}; {} ago.".format(self.args[0], lastname, timelist.strftime("%A, %d.%m.%Y %H:%M"), self._timecalc(delta)[0]), 1)
				
		else:
			raise KeyError
			
	except KeyError:
		self.say("Unable to comply: No entry for subject '{!s}' found. Please make sure the name is properly spelled and capitalized.".format(self.args[0]), 0)
		traceback.print_exc()

def __init__(self):
	try:
		self.cf_list[".ls"]="lastseen"
		self.cf_levels['.ls']=2
		self.cf_access_types['.ls']=[0,1,2]
		self.dict_help[".ls"]="Shows when a user was last seen (by the bot). Usage: .ls (-e) <Username>. -e for that exact nick, otherwise, it scans for any associated nick."
	except:
		self.writeLog("Error initializing plugin 'lastseen'", 2)
		self.noteError()
		
def exit(self):
	try:
		for x in self.namelist:
			self.dict_lastseen[x]=datetime.datetime.now()
	except IndexError:
		pass
	self._savedata(self.dict_lastseen, 'lastseen')