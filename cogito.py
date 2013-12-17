#when leaving channel, replace datapipe.channels value with Null to prevent 1 becomine 2, 2 becoming 3.

#rewrite to use a per-channel .minage rather than config.minage. Perhaps a .setage function.
#export channels with .minage on shutdown, fuck all others.
	#import from file. for each object, join it and import data.
	
	
#Please note: All commands are executed in the channel they are received from. In case of a PM, you may specify a channel via its ID number. E.g. .kick 1 A Bad Roleplayer will kick A Bad RolePlayer from channel #1. To get a list of IDs and channels, use the command '.lc'. A command without an ID will be parsed as the 'default' channel, config.channels[0]

import config
import datetime
import FListAPI
import importlib
import json
import os
import personality
import Queue
import random
import re
import songs
import string
import sys
import threading
import time
import traceback
from urllib import urlencode, quote_plus
import urllib2
import utils
import yaml
from twisted.internet import defer, reactor, task, threads
from autobahn.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS

opener 			= urllib2.build_opener()
opener.addheaders.append(('Cookie', 'warning=1'))
startuptime 	= datetime.datetime.now()
sendQueue		= Queue.Queue()
recvQueue 		= Queue.Queue()
EventQueue 		= Queue.Queue()

admins 			= utils.loadData('admins', list)
allAdmins		= []
banBanter		= utils.loadData('banbanter', list)
funcBanter		= utils.loadData('funcbanter', list)
joinmsgDict 	= utils.loadData('joinmsg', dict)
server_vars 	= {}

class Channel():
	def __init__(self, name, ckey=None):
		self.name=name
		self.key = ckey if ckey is not None else self.name
		self.minage = config.minage
		self.users=[]
		self.ops =[]
		self.lastjoined = []
		self.whitelist = []
		self.blacklist = []
		
	def userJoined(chan, character):
		name = getUser(character).name
		chan.users.append(name)
		chan.lastjoined.append(name)
		print("\tAppended {} to lastjoined. Current length: {}\n".format(name, len(chan.lastjoined)))
				
	def userLeft(chan, character):
		name = getUser(character).name
		try:
			chan.users.remove(name)
			chan.lastjoined.remove(name)
		except ValueError: pass
		except:
			traceback.print_exc()
		
def userFromFListData(name, data):
	print("\tUser data acquired.")
	user = getUser(name)
	try:
		for x in data:
			print("Setting ", user.name, " ", str(x), " to ", data[x])
			setattr(user, str(x).lower(), data[x])
	except Exception, exc:
		print exc
	try:
		user.age = int(re.search('(\d{1,5})', data['Age']).group(0))
		user.weight = int(re.search('(\d{1,5})', data['Weight']).group(0))
	except KeyError as error: 
		setattr(user, "".format(error).lower(), 0)
		
class User():
	def __init__(self, name):
		self.name = name
		self.lastseen = datetime.datetime.now()
		self.status = "online"
		self.channels=[]
		self.kinks=()

	def __getattribute__(self, item):
		try:
			return object.__getattribute__(self, item)
		except AttributeError:
			print("\t Could not find {} in User instance for {}.".format(item, self.name))
			#the blocking one never completes, the non-blocking returns a deferred that fucks up __getitem__ (and stop all the other stuff from working aparently)... :/
			#data = threads.blockingCallFromThread(reactor, FListAPI.getCharInfo, name)
			d = threads.deferToThread(FListAPI.getCharInfo(self.name))
			d.addCallback(userFromFListData)
			d.addCallback(object.__getattribute__(self, item))
			return d
			#data = reactor.callFromThread(FListAPI.getCharInfo, name)
			#reactor.callInThread(getUserData(self, self.name))
			
	#def __str__(self):

	def kick(self, channel):
		channel = getChannel(channel)
		req = json.dumps({"operator":"{}".format(config.character),"channel":channel.key,"character":self.name})
		sendRaw("CKU {}".format(req))
		
	def ascend(self):pass
	
def sendRaw(msg):
	sendQueue.put(msg)
	
def sendText(message, route=1, char='Cogito', chan='private'):
	"""	Route	0			1			2				3				4
		Target	Private		Channel		Channel+Prefix	Action in MSG	Action in PRI"""
	char=getUser(char).name
	if chan=='private': route=0
	else: chan=getChannel(chan).key
	if route == 0:
		msg = "PRI {}".format(json.dumps({'recipient':char, 'message':message})).encode('utf-8', 'replace')
	elif route<3:
		prefix = '{}: '.format(char)
		msg = "{}{}".format(prefix*(route>1), message)
		msg = "MSG {}".format(json.dumps({'channel':chan, 'message':message}))
	elif route<5:
		message = "/me "+message
		if route==4 or chan=='private': 
			path="PRI" 
			msg = "{} {}".format(path, json.dumps({'recipient':char, 'message':message}))
		else: 
			path="MSG"
			msg = "{} {}".format(path, json.dumps({'channel':chan, 'message':message}))
	sendQueue.put(msg)
	
def reply(message, route=2):
	sendText(message, route, datapipe.source.character.name, datapipe.source.channel.name)
	
def joinChannel(channel):
	channel = getChannel(channel)
	sendRaw("JCH {}".format(json.dumps({'channel':channel.key})))
	datapipe.channels.append(channel)

class DataPipe():
	def __init__(self):
		self.character		= config.character
		self.blacklist		= utils.loadData('blacklist', list)
		self.helpDict 		= utils.loadData('help', dict)
		self.ignorelist		= ['Dregan Stouthilt']
		self.messageDict 	= utils.loadData('{} messages'.format(config.character), dict)
		#self.usersDict 	= utils.loadData('users', dict)
		self.whitelist		= utils.loadData('whitelist', list)
		self.admins 		= config.admins + admins
		self.functions		= config.functions
		self.channels		= []
		self.pluginexit		= []
		self.pluginloops	= []
		self.plugins 		= {}
		self.channelDict	= {}
		self.dict_limits 	= {}
		self.usersDict 		= {}
		self.lastseenDict 	= utils.loadData('lastseen', dict)
		self.singer			= ""
		self.song 			= ""
		self.access_type    = 0
		self.songlevel 		= 0
		self.song_flag 		= False
		self.success_flag 	= False
		self.personality	= None
		
	def loadData(self, file, expected=dict):
		return utils.loadData(file, expected=dict)
		
	def saveData(self, data, file):
		utils.saveData(data, file)

	def reply(self, message, route=2):
		reply(message, route)
		
	def writeLog(self, text):
		utils.log(text, 1)
		
datapipe = DataPipe()

def getUser(user):
	if isinstance(user, User): return user
	if isinstance(user, Channel):
		print("{} is a Channel instance on which getUser has been called. Check the program.".format(user))
		return None
	try: user=user['identity']
	except: pass
	if user in datapipe.usersDict.keys():
		return datapipe.usersDict[user]
	else:
		xuser = User(user)
		datapipe.usersDict[user]=xuser
		return xuser
	
def getChannel(channel):
	if isinstance(channel, Channel): return channel
	if isinstance(channel, User):
		print "{} is actually a User instance; this is what's been messing up your channelDict.".format(channel)
		return None
	for x in datapipe.channelDict.values():
		if (x.name == channel) or (x.key == channel): 
			return x
	chan = Channel(channel)
	datapipe.channelDict[channel]=chan
	return chan
		
datapipe.getUser = getUser
datapipe.getChannel = getChannel
	
#"It's easier to ask forgiveness than permission"
class Source():
	def __init__(self, channel, character):
		if channel == "": 
			self.channel = ""
			self.character = ""
			return
		self.channel = getChannel(channel)
		self.character = getUser(character)

class Message():
	def __init__(self, msg):
		"""Rememeber: params is the list of keys, args is the dict"""
		try:
			char = ""
			chan = ""
			self.access_type = 0
			self.cmd = msg[:3]
			if len(msg)<4:
				self.args 	= {}
				self.params = []
				self.source = Source(Channel('None'), User('None'))
				return
			else: self.msg_data = json.loads(msg[4:])
			try:
				char=getUser(self.msg_data['character'])
			except KeyError:
				char = User('None')
			if self.cmd in ['PRI', 'MSG']:
				text = self.msg_data['message']
				text = text.strip()
				self.args 	= text.split()
				self.params = text
				if self.cmd == 'PRI': chan=Channel("private", None)
				else: chan = getChannel(self.msg_data['channel'])
				self.source = Source(chan, char)
				
			else:
				try:
					self.args 	= self.msg_data
					self.params = self.msg_data.keys()
					chan = getChannel(self.msg_data['channel'])
					self.source = Source(chan, char)
				except:
					raise KeyError

		except ValueError:
			print("ValueError w/ "+self.cmd)
			self.msg_data = ""
			self.args = {}
			self.params = []
			self.source = Source(Channel('None'), User('None'))
			
		except KeyError:
			self.source = Source(Channel('None'), User('None'))
			
		except:
			print "WEIRD ERROR"
			traceback.print_exc()
			
		else:
			del self.msg_data
			
def load(self):
	names=[]
	for root, sub, files in os.walk("./plugins/"):
		for filename in files:
			if filename.startswith('_'): continue
			name, ext = os.path.splitext(filename)
			if ext[1:] in ('py', 'pyw'):
				pathname=os.path.join(root, filename)
				with open(pathname, 'r') as afile:
					c = afile.readline().strip()
					if c ==r'#1dbdc6da34094db4e661ed43aac83d91':
						names.append(name)
	for name in names:
		try:
			# reivnote:
			# __import__('plugins.foo') returns the plugins parent module,
			# so we use getattr to reach inside for the desired plugin
			self.plugins[name] = getattr(__import__('plugins.{}'.format(name)), name)
			current = self.plugins[name]
			current.__init__(self)
			try: 
				if getattr(current, "loop"):
					self.pluginloops.append(getattr(current, "loop"))
			except AttributeError: pass
			try:
				if getattr(current, "exit"):
					self.pluginexit.append(getattr(current, "exit"))
			except AttributeError: pass
			except NameError: pass
		except:
			traceback.print_exc()
		else:
			print("---plugin '{}' successfully initialized.".format(name))
		
def ORSParse(data):
	print "\tParsing ORS data. Some Assembly Required."
	d = defer.Deferred()
	for part in data:
		channel = getChannel(part['title'])
		channel.key = part['name']
	return d

def checkAge(age, char, chan):
	try:
		chan=getChannel(chan)
		char.age = age
		if (char.name in chan.whitelist) or (char.name in datapipe.whitelist): 
			print ("Whitelisted user.")
			chan.userJoined(char.name)
			return
		if char.age<chan.minage and char.age!=0:
			sendText("Cogito has detected an user [color=red]below the room's minimum age:[/color] {}.".format(char.name), 2, chan=chan)
			banter = eval(random.choice(banBanter))
			sendText(banter, 2, char.name, chan.key)
		#	print("\tExpulsion.")
		#	char.kick(chan)
		elif char.age ==0:
			chanusers = getChannel(chan).users
			chan.userJoined(char.name)
			print("\tCannot parse.")
			xadmins = sorted(chan.ops, key=lambda *args: random.random())
			for x in xadmins:
				if x in chanusers:
					if x in datapipe.ignorelist: continue
					y = getUser(x)
					try:
						if y.status in ['busy', 'dnd']: 
							continue
						else:
							print("\tAdministrator {} found, reporting user to be checked.".format(y.name))
							sendText("Cannot automatically determine age of user '[user]{}[/user]'. Please verify manually: [user]{}[/user] [sub]To add user to whitelist, tell me '.white {}', in the channel to whitelist the user for.[/sub]".format(char.name, quote_plus(char.name), char.name), 0, y.name)
							return
					except: traceback.print_exc()
		else:
			print("\tUser {} has passed inspection (Age>{}), claiming to be {} years old.".format(char.name, chan.minage, char.age))
			#sendText("Demonstration: User {} has passed inspection (Age>{}), being {} years old. Apparently.".format(char.name, config.minage, char.age), 0, 'Valorin Petrov')
			chan.userJoined(char.name)
			telling(char, chan)
			
	except:
		traceback.print_exc()

class FListCommands(threading.Thread):

	def __init__(self):
		threading.Thread.__init__()
		
	def reply(self, message, route=2):
		print ("FListProtocol reply")
		reply(message, route)
		
	def writeLog(self, text):
		utils.log(text, 1)

	def ACB(self, item):pass
	
	def ADL(self, item):pass
		#ops = item.args['ops']
		#for op in ops:
		#	datapipe.admins.append(op)
		
	def CDS(self, item): pass
	
	def CKU(self, item):
		if config.banter and random.random<=config.banterchance:
			a = eval(random.choice(banBanter))
			reply(a, 1)
	
	def COL(self, item):
		ops = item.args['oplist']
		chan = getChannel(item.args['channel'])
		for op in ops:
			if not op in chan.ops: 
				chan.ops.append(str(op))
				allAdmins.append(str(op))
		print ("Channel operators for "+chan.name +": "+ str(chan.ops))
		
	def CON(self, item):
		with open('./data/user stats.txt', 'a') as io:
			io.write("{} {}\n".format(time.strftime("%c"), item.args['count']))
			
	def COA(self, item):
		chan = getChannel(item.args['channel'])
		char = getUser(item.args['channel'])
		if not char.name in chan.ops:
			chan.ops.append(char.name)
			allAdmins.append(char.name)

	def COR(self, item):
		chan = getChannel(item.args['channel'])
		chan.ops.remove(item.args['character'])
		allAdmins.remove(item.args['character'])
		
	def ERR(self, item):
		utils.log("ERROR: {}".format(item.args))
		if item.args['message']=='This command requires that you have logged in.':
			sys.exit(1)
				
	def FLN(self, item): pass		
	def FRL(self, item): pass
	def HLO(self, item): pass
			
	def ICH(self, item):
		chan = item.args['channel']
		chan = getChannel(chan)
		chan.users=[]
		chars = item.args['users']
		for x in chars:
			x=getUser(x)
			if not x.name in chan.users: chan.users.append(x.name)
		#print "\tUserlist for ", chan.name, "completed: ", chan.users

	def IDN(self, item): pass
	def IGN(self, item): pass
		
	def JCH(self, item):
		char = getUser(item.args['character']['identity'])
		chan = getChannel(item.args['channel'])
		print("User {} has joined '{}'.".format(char.name, chan.name))
		if char.name == config.character: return
		if char.name in datapipe.blacklist: char.kick(char)
		d = threads.deferToThread(FListAPI.getAge, char.name)
		d.addCallback(checkAge, char=char, chan=chan)
						
	def LCH(self, item):
		chan = getChannel(item.args['channel'])
		if chan.name == "Frontpage":
			return
		char = getUser(item.args['character'])
		print("User {} has left '{}'.".format(char.name, chan.name))
		chan.userLeft(char)
		datapipe.lastseenDict[char.name]=datetime.datetime.now()
					
	def LIS(self, item):pass
	def NLN(self, item):pass
	
	def ORS(self, item):
		try:
			data = item.args['channels']
			d = ORSParse(data)
			for x in config.channels:
				d.addCallback(joinChannel(x))
			#result = threads.blockingCallFromThread(reactor, ORSParse, data)
			#except Error, exc:
		except Exception:
			traceback.print_exc()
		
		#this is important and needs to lock 'till it's done
			#need a unique function to handle it?
			#browse through recvQueue until you get one with ORS in it, put others back FIFO style, process ORS, release lock?
			#spawn no new worker threads during lock, instead finish current thread, then parallel process merrily along?
					
	def PIN(self, item): sendRaw("PIN")
	
	def STA(self, item):
		if item.args['character'] in allAdmins:
			getUser(item.args['character']).status = item.args['status']			
	
	def SYS(self, item):
		utils.log(item.args['message'])
	
	def TPN(self, item): pass
		
	def VAR(self, item):
		server_vars[item.args["variable"]]=item.args["value"]
		if item.args["variable"]=="msg_flood":
			new = item.args["value"]*1.25
			print("\tDetected server-side flood control. Self-adjusting: sending output every {} milliseconds.".format(new))
			server_vars['permissions']=1
			EternalSender.stop()
			EternalSender.start(new)
		
	def listIndices(self, item):
		self.reply("List of active channels and their indices for channel-specific commands:")
		for num, chan in enumerate(datapipe.channels):
			self.reply("#{}: {}".format(num, chan.name))
			
	def whitelist(self, item):
		chan, item = channelFromIndex(self, item)
		candidate = item.params
		#	item.source.channel.whitelist.append(candidate)
		datapipe.whitelist.append(candidate)
		reply("{} has been whitelisted.".format(candidate), 0)	
		utils.log("{} has been whitelisted by {}.".format(candidate, item.source.character.name))	
		utils.saveData(datapipe.whitelist, 'whitelist')

	def blacklist(self, item):
		candidate = item.params
		datapipe.blacklist.append(candidate)
		reply("{} has been blacklisted.".format(candidate), 0)
		utils.log("{} has been blacklisted by {}.".format(candidate, item.source.character.name))
		
	def op(self, item):
		candidate = item.params
		chan = item.source.channel
		chan.ops.append(candidate)
		datapipe.admins.append(candidate)
		reply("{} has been made a bot operator.".format(candidate), 0)
		utils.log("{} has been a bot operator for {} by {}.".format(candidate, chan.name, item.source.character.name))
		
	def deop(self, item):
		candidate = item.params
		chan = item.source.channel
		chan.ops.remove(candidate)
		datapipe.admins.remove(candidate)
		reply("{} is no longer a bot operator.".format(candidate), 0)
		utils.log("{} has is no longer a bot operator by order of {}.".format(candidate, item.source.character.name))
		
	def join(self, item):
		chan = item.params
		reply("Command received. Joining '{}'".format(chan), 0)
		joinChannel(chan)
	
	def part(self, item):
		chan = item.params
		reply("Command received. Leaving '{}'".format(chan), 0)
		sendRaw("LCH {}".format(channelKey(chan)))
	
	def kick(self, item):
		char = item.params
		sendRaw("CKU {}".format(json.dumps({'channel': item.source.channel.key, 'character': char})))
		reply("Command received. Removing '{}' from {}.".format(character, source.channel), 0)
		utils.log("{} has kicked {} from {}.".format(item.source.character.name, char, item.source.channel.name))
	
	def ban(self, item):
		char = params	
		sendRaw("CKU {}".format(json.dumps({'channel': item.source.channel.key, 'character': char})))
		reply("Command received. Banning '{}' from {}.".format(character, source.channel), 0)
		item.source.channel.blacklist.append(char)
		utils.log("{} has banned {} from {}.".format(item.source.character.name, char, item.source.channel.name))
	
#	def kickban(self, character, channel=source.channel):
#		kchannel = channelKey(channel)
#		sendText("CKU {}".format(json.dumps({'channel': kchannel, 'character': character})), 5)
#		sendText("Command received. Removing '{}' from {}.".format(character, channel), 0)
		
	def timeout(self, item):
		try: length = int(item.args[-1:])
		except ValueError: 
			reply("Could not parse parameter 'length'. I'll just use 10 minutes.", 0)
			length = 10
		except IndexError:
			length = 10
		#fix that
		character = " ".join(item.args[:-1])
		self.reply("Handing in a timeout for {} from {}. Duration: {} minutes.".format(character, item.source.channel.name, length))
		sendRaw("CKU {}".format(json.dumps({"channel":item.source.channel.key, "character":character, "length":length})))
		
	def lastJoined(self, item):
		print item.source.channel.name
		channel = item.source.channel
		print channel.name
		last = channel.lastjoined
		users = []
		if len(last) == 0:
			reply("No new data available.", 0)
			return
		try: 
			numUsers = int(item.args[0])
			last = last[:numUsers]
		except IndexError:
			numUsers = len(last)
		for x in last:
			users.append("[user]{}[/user]".format(x))
		
		reply("The following {} users (out of a maximum {}) recently joined '{}': {}".format(numUsers, len(channel.lastjoined), channel.name, " ".join(users)), 0)
		channel.lastjoined=channel.lastjoined[numUsers:]
			
	def unban(self, item):pass
	
	def minage(self, item):
		try:
			age = int(item.args[0])
			self.source.channel.minage = age
			self.reply("Successfully set minimum age for {} to {}.".format(item.source.channel.name, age))
		except ValueError:
			self.reply("Error: Cannot parse {} as a number.".format(self.args[0]))
	
	def rainbowText(self, item):
		slist=[]
		a = len(item.params)
		d,e = divmod(a, 6)
		if a<7:
			reply("Gonna need at least seven letters for a rainbow!",1)
		for x in xrange(0, a, d):
			slist.append(item.params[x:x+d])
		if e>3:
			slist[-2]=slist[-2]+item.params[-(e-3):]
		sendText("[color=red]{}[/color][color=orange]{}[/color][color=yellow]{}[/color][color=green]{}[/color][color=cyan]{}[/color][color=blue]{}[/color][color=purple]{}[/color]".format(*slist), 2, chan=config.channels[0])
		
	def hibernation(self, item):
		try:
			reply("Command accepted. Shutting down.", 1)
			print('Shutting down. Stopping reactor and writing data.')
			reactor.stop()
			chans = {}
			for name, chaninst in datapipe.channelDict:
				if hasattr(chaninst, minage): chans[name]=chaninst
			utils.saveData(chans, 'channels')
			utils.saveData(utils.statsDict, '{} stats'.format(config.character))
			utils.saveData(admins, 'admins')
			utils.saveData(datapipe.whitelist, 'whitelist')
			utils.saveData(datapipe.blacklist, 'blacklist')
			for x in datapipe.pluginexit:
				try:
					func = getattr(x, "exit", None)
					if callable(func): func()
				except:
					traceback.print_exc()
		except Exception, error:
			utils.log("Error during shutdown: {}".format(error))
			traceback.print_exc()
		else:
			print('Shutdown successful. Goodbye, administrator.')
		finally:
			sys.exit(0)
		
	def help(self, msg):
		
		try:
			print msg.args[0]
			if msg.args[0]:
				reply(datapipe.helpDict[msg.args[0]], 0)

		except KeyError:
			reply("No entry for command '{}'. Please check your syntax and try again.".format(msg.args[1]) , 0)
			
		except IndexError:	
			self.reply("{} F-List Bot, v{}.".format(config.character, config.version), 0)
			self.reply("Please note: All commands are executed in the channel they are received from. In case of a PM, you may specify a channel via its ID number. E.g. .kick 1 A Bad Roleplayer will kick A Bad RolePlayer from channel #1. To get a list of IDs and channels, use the command '.lc'. A command without an ID will be parsed as the 'default' channel, here: {}".format(config.channels[0]))
			self.reply("The following functions are available:")
			func=[]
			for x in datapipe.helpDict.keys():
				func.append(x)
			func.sort()
			for x in func:
				self.reply("--{}: {!s}".format(x, datapipe.helpDict[x]), 0)

	def tell(self, msg):
		sender = msg.source.character.name
		if msg.params.find(':')==-1:
			reply("You need to put a ':' after the recipient's name, darling.", 1)
			return
		recipient, message = msg.params.split(':')
		sendtime = datetime.datetime.now()
		data = (sender, message, sendtime)
		try:
			messages = datapipe.messageDict[recipient.lower()]
		except TypeError:
			datapipe.messageDict = {}
			messages = []
		except KeyError:
			messages = []
		if len(messages)>4:
			reply("[color=green]{} already has {} messages waiting. Message not added.[/color]".format(recipient, personality.spokenNumber(config.messagelimit)), 2)
			return
		else:	
			messages.append(data)
			datapipe.messageDict[recipient.lower()]=messages
			utils.saveData(datapipe.messageDict, '{} messages'.format(config.character))
			reply("[color=green]Message to {} saved.[/color]".format(recipient), 2)
			
			
	def say(self, msg):
		index, msg = channelFromIndex(self, msg)
		sendText(msg.params, 2, chan)
		
	def act(self, msg):
		index, msg = channelFromIndex(self, msg)
		sendText(msg.params, 3, chan)
		

	

class FListProtocol(WebSocketClientProtocol, FListCommands):
	def __init__(self):
		datapipe.FListProtocol = self
		
	def onOpen(self):
		datapipe.key = FListAPI.getKey()
		sendRaw("IDN {}".format(json.dumps({"method":"ticket","account":config.account,"character":"Cogito","ticket":datapipe.key,"cname":"cogito","cversion":"0"})))
		sendRaw("LCH {}".format(json.dumps({'channel':'Frontpage'})))
		sendRaw("ORS")

	def onMessage(self, msg, binary):
		msg = msg.decode('ascii', 'ignore')
		message = Message(msg)
		recvQueue.put((message, self))
		
"""sendRaw and sendText both expect Message() instances, which have self.params (a dict for sendRaw, a string for sendText, similar to received messages), self.source (carried over from the incoming message object?) and that's about it?"""	
def parseText(self, msg):
	if not msg.params[:3]=="/me":print ( "{} -- {} ({}): \"{}\"".format(time.strftime("%c"), msg.source.character.name, msg.source.channel.name, msg.params))
	else: print ( "{} -- ({}){}{}".format(time.strftime("%c"), msg.source.channel.name, msg.source.character.name, msg.params[3:]))
	try:
		if msg.args[0] in datapipe.functions.keys():
			#print ("\tCommand '{}' recognized.".format(msg.args[0]))
			func = msg.args[0]
			msg.args = msg.args[1:]
			msg.params = " ".join(msg.args)
			#!!! CHANGE TO PARSING SYSTEM FOR CHANNELINDEPENDENT WHATEVERTHEFUCK
			if msg.source.channel.name == "private": 
				msg.access_type = 0
				try:
					index = int(msg.args[0])
					msg.args = msg.args [1:]
					msg.params = " ".join(msg.args)
				except ValueError, IndexError:
					index = 0
					
				try:	
					chan = datapipe.channels[index]
					print("Rerouting PM command '{}' from channel 'private' into '{}'.".format(func, chan.name))
					msg.source.channel = chan
					
				except IndexError:
					self.reply("Command not executed: There is no channel with index {}. There are {} channels registered. To see the list, message me with .cl.".format(index, len(datapipe.channels)))
					
			else: 
				msg.access_type = 1
			#print msg.access_type,  msg.access_type in datapipe.cf_access_types[func], msg.source.channel.name, msg.source.character.name
			# 0 - priv, 1 - chan, 2 - chan, nick 
			func_params = datapipe.functions[func]
			if msg.access_type in func_params[2]:
				print("\t\tCorrect access type")
				msg.cf_level = 2
				if msg.source.character.name in datapipe.admins: msg.cf_level=0
				elif (msg.source.character.name in msg.source.channel.ops): msg.cf_level = 1
				#if (msg.source.channel.name == 'private') and (msg.source.character.name in allAdmins): msg.cf_level = 1
				#print msg.source.character.name, msg.source.channel.ops, datapipe.admins, msg.cf_level, msg.source.character.name in msg.source.channel.ops, msg.source.character.name in datapipe.admins
				if msg.cf_level <= func_params[1]:
					print ("\t\t\tHandling '{}'...".format(func_params[0]))
					handle_all_the_things(self, msg, func_params[0])
				else:
					self.reply("You do not have the necessary permissions to execute function '{}' in channel '{}'.".format(func_params[0], msg.source.channel.name))
					
	except IndexError:
		traceback.print_exc()
		
	if datapipe.song != "":
		if datapipe.singer == msg.source.character.name:
			try:
				_listen(self, msg, datapipe.song, datapipe.songiter, datapipe.dict_limits[datapipe.singer])

			except AttributeError, error:
				try:
					datapipe.song = songs.dict_firstlines[msg.params]
					datapipe.songiter = iter(songs.dict_songs[datapipe.song])
					datapipe.singer = self.source.character.name
					_listen(self, msg, datapipe.song, datapipe.songiter, datapipe.dict_limits[datapipe.singer])
				except Exception:
					traceback.print_exc()
				finally:	
					_songreset()

	for x in songs.dict_firstlines: 
		if songs.matcher(lambda x: x==" ", msg.params, x).ratio() > config.min_ratio:
			try:
				datapipe.song = songs.dict_firstlines[x]
				datapipe.songiter = iter(songs.dict_songs[datapipe.song])
				datapipe.singer = msg.source.character.name
				datapipe.dict_limits[datapipe.singer]=0
				datapipe.song_flag = True

			except (IndexError, RuntimeError, TypeError, NameError) as function_error:
				print("Error whilst listening to text command: {}".format(function_error), 2)
				traceback.print_exc()
				datapipe.song_flag = False

			if datapipe.song_flag == True:
				_listen(self, msg, datapipe.song, datapipe.songiter, datapipe.dict_limits[datapipe.singer])

	for x in datapipe.pluginloops:
		if callable(x):
			x(datapipe, msg)
							
def handle_all_the_things(self, msgobj, cmd=None):
	if cmd is None: cmd=msgobj.cmd
	try:
		if cmd in datapipe.plugins:
			func = getattr(datapipe.plugins[cmd], cmd, None)
			if callable(func):
				func(datapipe, msgobj)
		elif datapipe.personality!=None:
			func = getattr(datapipe.personality.code, cmd, None)
			if callable(func):
				func(datapipe, msgobj)
		else:
			func = getattr(FListCommands, '{}'.format(cmd), None)
			if callable(func):
				func(self, msgobj)
			else:
				raise AttributeError
				
	except AttributeError, error:
		print("\tFunction '{}' failed to execute: ({})".format(msgobj.cmd, error))
		traceback.print_exc()
		
	except:
		traceback.print_exc()
	else:
		#needs to be selective to user commands, not FListCommands shit. :/
		if config.banter and (cmd in config.functions.keys()) and (random.random>config.banterchance):
			reply(eval(random.choice(funcBanter)), 2)
	
def _songreset():
	datapipe.song = ""
	datapipe.songiter = None
	datapipe.singer = ""
	datapipe.dict_limits[datapipe.singer]=0
	datapipe.song_flag = False			
	datapipe.success_flag = False			
			
def _listen(self, msg, song, iter, limit):
	print("Listening to {}; limit {}".format(datapipe.song, limit))
	datapipe.songdata = songs.dict_songs[datapipe.song]
	datapipe.max_limit = len(datapipe.songdata)
	try:
		datapipe.songline2 = iter.next()
	except StopIteration:
		reply("Song rejected.", 0)
		_songreset()
		pass
	
	if songs.matcher(lambda x: x == " ", msg.params, datapipe.songline2).ratio() > config.min_ratio:
		datapipe.dict_limits[datapipe.singer]+=1
		datapipe.success_flag = True
		if datapipe.song in songs.dict_answers and datapipe.dict_limits[datapipe.singer] in songs.dict_alimits[datapipe.song]:
			print("I want to reply.")
			sreply = songs.dict_answers[datapipe.song][datapipe.dict_limits[datapipe.singer]-1]
			reply(str(sreply), 2)
	
	elif ("exec waath" in msg.params.lower()):
		_songreset()
	
	else:
		print("No match, no endline.")
		reply("Access denied", 0)
		_songreset()
		
	if datapipe.dict_limits[datapipe.singer] >= datapipe.max_limit:
		try:
			#handle_all_the_things needs a Message instance!
			msg=Message('MSG {\'message\':\'A MESSAGE NEEDS TO BE HERE\'}')
			handle_all_the_things(self, msg, config.cf_list[datapipe.song])
		finally:
			_songreset()
		
	elif datapipe.success_flag == False:
		reply("Access denied", 0)
		_songreset()		
		
def telling(char, chan):
	messages=[]
	try:
		for x in datapipe.messageDict[char.name.lower()]:
			messages.append(x) 
		c = len(messages)
		if c==0: return
		sendText("[color=green]{}, you have {} new message{}:[/color]".format(char.name, personality.spokenNumber(c), 's'*(c>1)), 1, char, chan)
		for x in messages:
			d = utils.timeFrac(datetime.datetime.now()-x[2])
			sendText("[color=yellow]<{}> [color=green]{}[/color] ({} ago)[/color]".format(x[0], x[1], d[0]), 2, char, chan)
	except KeyError: pass
	
	except TypeError:
		traceback.print_exc()
	else:
		del(datapipe.messageDict[char.name.lower()])
		utils.saveData(datapipe.messageDict, '{} messages'.format(config.character))
		
def qsend():
	try:
		item = sendQueue.get_nowait()
		datapipe.FListProtocol.sendMessage(item.encode('utf-8'))
	except Queue.Empty:	pass
		
def mainloop():
	try:
		"""doesn't do anything if EventQueue empty. instead of eventQueue, threading and conditions?"""
		#while EventQueue.qsize()>0:
		#	try: 
		#		func, data = EventQueue.get_nowait()
		#		func(data)
		#	except Queue.Empty: pass
		#	except Exception: traceback.print_exc()
		#Like, (Person who talked to you, function to call when you hear them again, condition to remove this part of the stack)
		
		item, self = recvQueue.get_nowait()
		datapipe.source = item.source
		if item.cmd not in config.ignore_commands: print("{} -- {} {}".format(time.strftime("%c"), item.cmd, item.args))
		if datapipe.personality != None: 
			datapipe.personality.code.handle(self, item.cmd, item.params) 
		if item.cmd not in ['MSG', 'PRI']:
			handle_all_the_things(self, item, item.cmd)
		else:
			parseText(self, item)
	except Queue.Empty: pass
	
if __name__ == '__main__':
	load(datapipe)
	datapipe.personality = personality.__init__(config)
	factory = WebSocketClientFactory("ws://chat.f-list.net:{}".format(config.port), debug = True)
	factory.protocol = FListProtocol
	EternalSender = task.LoopingCall(qsend)
	MainLoop = task.LoopingCall(mainloop)
	print('Booting cogito, version {}. Connecting to account "{}". Condition all green. Get set.'.format(config.version, config.account))
	connectWS(factory)
	try:
		print('Starting reactor.')
		EternalSender.start(config.flood_pause)
		MainLoop.start(0.25)
		reactor.run()
	except:
		reactor.stop()
		traceback.print_exc()
