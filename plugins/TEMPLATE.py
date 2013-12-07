#that key in line 2 needs to be line 1 so a plugin is loaded by the bot.
#1dbdc6da34094db4e661ed43aac83d91


#define imports; modules, even if loaded in the main program, have to be re-loaded. 
import traceback

#IMPORTANT Since all these plugins are run from within a class-based bot, every function should handle a self argument even if it's not in a class itself

"""
Accessible from the main program are (utilizing a <self>!):

	[FUNCTIONS]
	_send(self, message, mtype=0)	
		Send <message> to <mtype>: 
			0	The user who last messaged the bot, in a query
			1	the channel, with the username.
			2	the channel
			3	the channel, as an ACTION
	_loaddata(self, filename)
		loads an object from a <filename>.yml file in /data/. Returns the object read from the file.
	_savedata(self, data, file) 
		Saves the object or data in <data> to <file>.yml in /data/.
	_logwrite(self, text, ltype=1)
		Writes <test> to the logfile <ltype>
			0	<BOTNAME>.log
			1	<BOTNAME> EX.log
			2	both
	_rootget(self, name)
		Identifies a user based on his nicks and aliases, in order to centralize data around a 'main' nickname.
		Basically, anti alt-itis function.
		returns False, False, False, False if it has no idea who this is; else
		returns ident, root, nicks, full
	_process_source(self, data):
		Formats string to return <username><ident><host>
		expected data: reiv!~reiv@843FE74B.46884354.5903B821.IP (e.g the source part of a message tuple)
		used with self.source
	adderror()
		increments the error counter by 1.
	
	
	[DATA]
	self.source
		origin of a command
		
	self.namelist
		list of all users in current channel
		
	self.NICK
		bot name, from currently used settings file
	
	
"""

def FUNCTION(self):
	#this function can be called via getattr() after being registered in dict.functions during __init__()
	pass
	
def loop(self):
	#this function is executed in EVERY iteration of the main loop (so don't make it fucking huge)
	#loader3 automatically appends loop(self) and exit(self) functions.
	pass

def __init__(self):
	try:
		self.cf_list["COMMAND"]="FUNCTION"
		self.cf_levels['COMMAND']=2
		# 	0	creator only 
		#	1	admin from settings only
		#	2	everyone
		self.cf_access_types['COMMAND']=[0,1,2]
		#	0	Execute command only when it comes from a /query
		#	1	Execute command when the bot's name is mentioned before
		#	2	Execute command whenever called
		self.dict_help["COMMAND"]="Help Entry For Command"
	except:
		self.writeLog("Error initializing plugin 'PLUGINNAME'", 2)
		self.noteError()
		
def exit():
	#is run on Bot shutdown. Place cleanup, data saving, etc., here.