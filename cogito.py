#when leaving channel, replace datapipe.channels value with Null to prevent 1 becomine 2, 2 becoming 3.
#add a datapipe.ignorelist you can actually add/remove from


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

ignore_commands = ['FLN', 'STA', 'NLN', 'PIN', 'MSG', 'PRI', 'TPN', 'LIS', 'ORS', 'IDN', 'VAR', 'CDS', 'COL', 'ICH', 'JCH', 'LCH', 'CON', 'HLO', 'ERR']
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
		self.minage = 18
		self.checkAge = False
		self.index = None
		self.users=[]
		self.ops =[]
		self.lastjoined = []
		self.whitelist = []
		self.blacklist = []
		self.ignoreops = []
		
	def userJoined(chan, character):
		name = getUser(character).name
		chan.users.append(name)
		chan.lastjoined.append(name)
		print("Appended {} to {}'s last joined list. Current length: {}\n".format(name, chan.name, len(chan.lastjoined)))
				
	def userLeft(chan, character):
		name = getUser(character).name
		try:
			chan.users.remove(name)
			chan.lastjoined.remove(name)
		except ValueError: pass
		except:
			traceback.print_exc()
		
	def join(self):
		sendRaw("JCH {}".format(json.dumps({'channel':self.key})))
		for pos, item in enumerate(datapipe.channels):
			if item==None:
				print pos, item, datapipe.channels
				datapipe.channels[pos]=self
				print pos, item, datapipe.channels
				self.index = len(datapipe.channels)-1	
				return
		datapipe.channels.append(self)
		self.index = len(datapipe.channels)-1
		print("Joining channel '{}', index {}.".format(self.name, self.index))
		
	def part(self):
		sendRaw("LCH {}".format(json.dumps({'channel':self.key})))
		datapipe.channels[datapipe.channels.index(self)]=None
		
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
			# d.addCallback(object.__getattribute__(self, item))
			d.addCallback(object.__getattribute__, self, item)
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
	
def reply(message, item, path_override=None):
	if not hasattr(item, 'access_type'): item.access_type = 0
	if path_override is not None: path = path_override
	else: path = item.access_type
	sendText(message, path, item.source.character.name, item.source.channel.name)

class DataPipe():
	def __init__(self):
		self.character		= config.character
		self.blacklist		= utils.loadData('blacklist', list)
		self.helpDict 		= utils.loadData('help', dict)
		self.messageDict 	= utils.loadData('{} messages'.format(config.character), dict)
		#self.usersDict 	= utils.loadData('users', dict)
		self.whitelist		= utils.loadData('whitelist', list)
		self.admins 		= config.admins + admins
		self.functions		= config.functions
		self.channels		= [Channel('Dummy')]
		self.pluginexit		= []
		self.pluginloops	= []
		self.plugins 		= {}
		self.channelDict	= utils.loadData('channels', dict)
		self.dict_limits 	= {}
		self.usersDict 		= {}
		self.lastseenDict 	= utils.loadData('lastseen', dict)
		self.singer			= ""
		self.song 			= ""
		self.songlevel 		= 0
		self.song_flag 		= False
		self.success_flag 	= False
		self.personality	= None
		
	def loadData(self, file, expected=dict):
		return utils.loadData(file, expected=dict)
		
	def saveData(self, data, file):
		utils.saveData(data, file)

	def reply(self, message, item, path_override=None):
		reply(message, item, path_override)
		
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
		char = ""
		chan = ""
		self.access_type = 0
		try:
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
	print "\nParsing ORS data. Some Assembly Required."
	for part in data:
		channel = getChannel(part['title'])
		channel.key = part['name']
	return

def checkAge(age, char, chan):
	try:
		chan=getChannel(chan)
		char.age = age
		if char.age>=chan.minage:
			print("User {} has passed inspection for {} (Age>{}), claiming to be {} years old.".format(char.name, chan.name, chan.minage, char.age))
			#sendText("Demonstration: User {} has passed inspection (Age>{}), being {} years old. Apparently.".format(char.name, config.minage, char.age), 0, 'Valorin Petrov')
			chan.userJoined(char.name)
			telling(char, chan)
			return
			
		if (char.name in chan.whitelist) or (char.name in datapipe.whitelist): 
			print ("Whitelisted user.")
			chan.userJoined(char.name)
			telling(char, chan)
			return
			
		xadmins = sorted(chan.ops, key=lambda *args: random.random())
		for x in xadmins:
			if x in chan.users:
				if x in chan.ignoreops: continue
				y = getUser(x)
				try:
					if y.status in ['busy', 'dnd']: 
						continue
					else:
						print("Mod {} selected for this check.".format(y.name))
						break
				except: traceback.print_exc()
						
						
		if char.age<chan.minage and char.age!=0:
			sendText("User [color=red]below {}'s minimum age of {}:[/color] [user]{}[/user].".format(chan.name, chan.minage, char.name), 0, char=y)
			utils.log("User {} under minimum age of {} for {}. Alerting {}.".format(char.name, chan.minage, chan.name, y.name))
			banter = eval(random.choice(banBanter))
			sendText(banter, 2, char, chan)
		#	print("\tExpulsion.")
		#	char.kick(chan)
		
		elif char.age ==0:
			print("\tCannot parse. Informing Mod {}\n".format(y.name))
			sendText("Cannot automatically determine age of user '[user]{}[/user]'. Please verify manually: [user]{}[/user] [sub]To add user to the channel's whitelist, reply '.white {} {}' in a PM. If you tell me in the channel, leave the number out.[/sub]".format(char.name, char.name, char.name, chan.index), 0, char=y)
			chan.userJoined(char.name)
			return
			
	except:
		traceback.print_exc()

class FListCommands(threading.Thread):

	def __init__(self):
		threading.Thread.__init__()
		
	def reply(self, message, item, path_override=None):
		reply(message, item, path_override)
		
	def writeLog(self, text):
		utils.log(text, 1)

	def ACB(self, item):pass
	
	def ADL(self, item):pass
		#ops = item.args['ops']
		#for op in ops:
		#	datapipe.admins.append(op)
		
	def CDS(self, item):pass
	
	def CKU(self, item):
		# banned = getUser(item.args[''])
		if config.banter and random.random<=config.banterchance:
			a = eval(random.choice(banBanter))
			reply(a, item, 2)
	
	def COL(self, item):
		ops = item.args['oplist']
		chan = getChannel(item.args['channel'])
		for op in ops:
			if not op in chan.ops: 
				chan.ops.append(op)
				allAdmins.append(op)
		print ("Channel operators for "+chan.name +": "+ str(chan.ops))
		
	def CON(self, item):
		with open('./data/user stats.txt', 'a') as io:
			io.write("{} {}\n".format(time.strftime("%c"), item.args['count']))
		utils.log("{} users online.".format(int(item.args['count'])))
			
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
		utils.log("FList Error: Code {}. '{}'".format(item.args['number'], item.args['message']))
		if item.args['message']=="This command requires that you have logged in.":
			sendRaw("IDN {}".format(json.dumps({"method":"ticket","account":config.account,"character":"Cogito","ticket":datapipe.key,"cname":"cogito","cversion":config.version})))
				
	def FLN(self, item):
		char = getUser(item.args['character'])
		for chan in datapipe.channelDict.values():
			if char.name in chan.users:
				chan.leave(char)
		
	def FRL(self, item): pass
	
	def HLO(self, item): utils.log("Connection established...")
			
	def ICH(self, item):
		chan = getChannel(item.args['channel'])
		chan.users=[]
		chars = item.args['users']
		for x in chars:
			x=getUser(x)
			if not x.name in chan.users: chan.users.append(x.name)

	def IDN(self, item): pass
	def IGN(self, item): pass
		
	def JCH(self, item):
		char = getUser(item.args['character']['identity'])
		chan = getChannel(item.args['channel'])
		print("User {} has joined '{}'.".format(char.name, chan.name))
		if char.name == config.character: return
		if char.name in chan.blacklist: char.kick(char)
		if chan.checkAge == False: return
		d = threads.deferToThread(FListAPI.getAge, char.name)
		d.addCallback(checkAge, char=char, chan=chan)
						
	def LCH(self, item):
		chan = getChannel(item.args['channel'])
		if chan.name == "Frontpage":
			return
		char = getUser(item.args['character'])
		utils.log("User {} has left '{}'.".format(char.name, chan.name))
		chan.userLeft(char)
		datapipe.lastseenDict[char.name]=datetime.datetime.now()
					
	def LIS(self, item):pass
	def LRP(self, item):pass
	def NLN(self, item):pass
	def RLL(self, item):pass
	
	def ORS(self, item):
		try:
			data = item.args['channels']
			ORSParse(data)
			for x in config.channels:
				getChannel(x).join()
				#print ("Added callback to join {}".format(x))
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
			print("\tDetected server-side flood control. Self-adjusting: sending output every {} milliseconds.".format(new*1000))
			server_vars['permissions']=1
			EternalSender.stop()
			EternalSender.start(new)
		
	def listIndices(self, item):
		reply("List of active channels and their indices for channel-specific commands:", item, 0)
		for num, chan in enumerate(datapipe.channels):
			if num==0: continue
			if chan == None: continue
			reply("#{}: {}".format(num, chan.name), item, 0)
			
	def whitelist(self, item):
		candidate = item.params
		# datapipe.whitelist.append(candidate)
		item.source.channel.whitelist.append(candidate)
		reply("{} has been whitelisted for {}.".format(candidate, item.source.channel.name), item)	
		utils.log("{} has been whitelisted for {} by {}.".format(candidate, item.source.channel.name, item.source.character.name))	
		#utils.saveData(datapipe.whitelist, 'whitelist')

	def blacklist(self, item):
		candidate = item.params
		# datapipe.blacklist.append(candidate)
		item.source.channel.blacklist.append(candidate)
		reply("{} has been blacklisted for {}.".format(candidate, item.source.channel.name), item)
		utils.log("{} has been blacklisted for {} by {}.".format(candidate, item.source.channel.name, item.source.character.name))
		
	def op(self, item):
		candidate = item.params
		chan = item.source.channel
		chan.ops.append(candidate)
		datapipe.admins.append(candidate)
		reply("{} has been made a bot operator for {}.".format(candidate, item.source.channel.name), item)
		utils.log("{} has been a bot operator for {} by {}.".format(candidate, chan.name, item.source.character.name))
		
	def deop(self, item):
		candidate = item.params
		chan = item.source.channel
		chan.ops.remove(candidate)
		datapipe.admins.remove(candidate)
		reply("{} is no longer a bot operator for {}.".format(candidate, item.source.channel.name), item)
		utils.log("{} has is no longer a bot operator for {} by order of {}.".format(candidate, item.source.channel.name, item.source.character.name))
		
	def join(self, item):
		chan = getChannel(item.params)
		reply("Command received. Attempting to join '{}'".format(chan.name), item, 0)
		chan.join()
	
	def leave(self, item):
		chan = getChannel(item.params)
		reply("Command received. Leaving '{}'".format(chan.name), item, 0)
		chan.part()
	
	def kick(self, item):
		char = item.params
		sendRaw("CKU {}".format(json.dumps({'channel': item.source.channel.key, 'character': char})))
		reply("Command received. Removing '{}' from {}.".format(character, source.channel), item, 0)
		utils.log("{} has kicked {} from {}.".format(item.source.character.name, char, item.source.channel.name))
	
	def ban(self, item):
		char = item.params	
		sendRaw("CKU {}".format(json.dumps({'channel': item.source.channel.key, 'character': char})))
		reply("Command received. Banning '{}' from {}.".format(character, source.channel), item, 0)
		item.source.channel.blacklist.append(char)
		utils.log("{} has banned {} from {}.".format(item.source.character.name, char, item.source.channel.name))
	
#	def kickban(self, character, channel=source.channel):
#		kchannel = channelKey(channel)
#		sendText("CKU {}".format(json.dumps({'channel': kchannel, 'character': character})), 5)
#		sendText("Command received. Removing '{}' from {}.".format(character, channel), 0)
		
	def timeout(self, item):
		try: length = int(item.args[-1:])
		except ValueError: 
			reply("Could not parse parameter 'length'. I'll just use 10 minutes.", item, 0)
			length = 10
		except IndexError:
			length = 10
		#fix that
		character = " ".join(item.args[:-1])
		reply("Timeout for {} and channel {}. Duration: {} minutes.".format(character, item.source.channel.name, length), item, 0)
		sendRaw("CKU {}".format(json.dumps({"channel":item.source.channel.key, "character":character, "length":length})))
		
	def lastJoined(self, item):
		channel = item.source.channel
		last = channel.lastjoined
		users = []
		if len(last) == 0:
			reply("No new data available.", item, 0)
			return
		try: 
			numUsers = int(item.args[0])
			last = last[:numUsers]
		except IndexError:
			numUsers = len(last)
		for x in last:
			users.append("[user]{}[/user]".format(x))
		
		reply("The following {} users (out of a maximum {}) recently joined '{}': {}".format(numUsers, len(channel.lastjoined), channel.name, " ".join(users)), item, 0)
		channel.lastjoined=channel.lastjoined[numUsers:]
			
	def unban(self, item):pass
	
	def ignore(self, item):
		if not item.source.character.name in item.source.chan.ignoreops:
			item.source.chan.ignoreops.append(item.source.character.name)
			reply("You have been appended to the ignore list for {} and will no longer be pinged when AgeCheck is active.".format(item.source.channel.name), item)
		else:
			item.source.chan.ignoreops.remove(item.source.character.name)
			reply("You have been removed from the ignore list for {}.".format(item.source.channel.name), item)
			
	
	def minage(self, item):
		try:
			age = int(item.args[0])
			if age == 0:
				item.source.channel.checkAge = False
				sendText("Cogito Age Check deactivated by {}.".format(item.source.character.name), item.access_type, chan=item.source.channel)
				return
			item.source.channel.minage = age
			sendText("Cogito Age Check activated by {}. Alerting administrators to characters below age {}".format(item.source.character.name, age), item.access_type, chan=item.source.channel)
		except ValueError:
			reply("Error: Cannot parse {} as a number.".format(item.args[0]), item, 0)
	
	def rainbowText(self, item):
		slist=[]
		a = len(item.params)
		if a<7:
			reply("Gonna need at least seven letters for a rainbow!", item)
			return
		d,e = divmod(a, 6)
		for x in xrange(0, a, d):
			slist.append(item.params[x:x+d])
		if e>0:
			slist.append(item.params[-e:])
		print len(slist), slist
		sendText("[color=red]{}[/color][color=orange]{}[/color][color=yellow]{}[/color][color=green]{}[/color][color=cyan]{}[/color][color=blue]{}[/color][color=purple]{}[/color]".format(*slist), 2, chan=item.source.channel)
		
	def hibernation(self, item):
		try:
			reply("Command accepted. Shutting down.", item)
			print('Shutting down. Stopping reactor and writing data.')
			reactor.stop()
			chans = {}
			for name, chaninst in datapipe.channelDict.items():
				if (hasattr(chaninst, 'minage') and chaninst.minage!=18) or (len(chaninst.whitelist) > 0): 
					chaninst.users = []
					chaninst.lastjoined = []
					chaninst.index = []
					chaninst.key = ""
					chans[name]=chaninst
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
				reply(datapipe.helpDict[msg.args[0]], msg, 0)

		except KeyError:
			reply("No entry for command '{}'. Please check your syntax and try again.".format(msg.args[1]) , 0)
			
		except IndexError:	
			reply("{} F-List Bot, v{}.".format(config.character, config.version), 0)
			reply("Please note: All commands are executed in the channel they are received from. In case of a PM, you may specify a channel via its ID number. E.g. .kick 1 A Bad Roleplayer will kick A Bad RolePlayer from channel #1. To get a list of IDs and channels, use the command '.lc'. A command without an ID will be parsed as the 'default' channel, here: {}".format(config.channels[0]))
			reply("The following functions are available:")
			func=[]
			for x in datapipe.helpDict.keys():
				func.append(x)
			func.sort()
			for x in func:
				reply("--{}: {!s}".format(x, datapipe.helpDict[x]), 0)

	def tell(self, msg):
		sender = msg.source.character.name
		a = msg.params.find(':')
		if a ==-1:
			reply("You need to put a ':' after the recipient's name, darling.", msg, 1)
			return
		sender = msg.params[:a]
		recipient = msg.params[a:]
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
			reply("[color=green]{} already has {} messages waiting. Message not added.[/color]".format(recipient, personality.spokenNumber(config.messagelimit)), msg, 2)
			return
		else:	
			messages.append(data)
			datapipe.messageDict[recipient.lower()]=messages
			utils.saveData(datapipe.messageDict, '{} messages'.format(config.character))
			reply("[color=green]Message to {} saved.[/color]".format(recipient), msg, 2)
			
			
	def say(self, msg):
		sendText(msg.params, 2, chan=msg.source.channel)
		
	def act(self, msg):
		sendText(msg.params, 3, chan=msg.source.channel)
		
class FListProtocol(WebSocketClientProtocol, FListCommands):
	def __init__(self):
		datapipe.FListProtocol = self
		
	def onOpen(self):
		datapipe.key = FListAPI.getKey()
		sendRaw("IDN {}".format(json.dumps({"method":"ticket","account":config.account,"character":"Cogito","ticket":datapipe.key,"cname":"cogito","cversion":config.version})))
		#sendRaw("LCH {}".format(json.dumps({'channel':'Frontpage'})))
		sendRaw("ORS")

	def onMessage(self, msg, binary):
		msg = msg.decode('ascii', 'ignore')
		message = Message(msg)
		recvQueue.put((message, self))
		
"""sendRaw and sendText both expect Message() instances, which have self.params (a dict for sendRaw, a string for sendText, similar to received messages), self.source (carried over from the incoming message object?) and that's about it?"""	
def parseText(self, msg):
	if not msg.params[:3]=="/me":print ( "{} -- ({}) {}: \"{}\"".format(time.strftime("%c"), msg.source.channel.name, msg.source.character.name, msg.params))
	else: print ( "{} -- ({}) {}{}".format(time.strftime("%c"), msg.source.channel.name, msg.source.character.name, msg.params[3:]))
	try:
		if msg.args[0] in datapipe.functions.keys():
			#print ("\tCommand '{}' recognized.".format(msg.args[0]))
			func = msg.args[0]
			msg.args = msg.args[1:]
			msg.params = " ".join(msg.args)
			#!!! CHANGE TO PARSING SYSTEM FOR CHANNELINDEPENDENT WHATEVERTHEFUCK
			if msg.source.channel.name == "private": 
				msg.access_type = 0
				print ("Parsing for channel index...")
				index = None
				try:
					index = int(msg.args[-1])
					msg.args = msg.args [:-1]
					msg.params = " ".join(msg.args)
				except IndexError: pass
				except ValueError: pass

				if index is not None:
					try:	
						chan = datapipe.channels[index]
						print("Index found. Rerouting PM command '{}' from channel 'private' into '{}'.".format(func, chan.name))
						msg.source.channel = chan
					except IndexError:
						reply("Command not executed: There is no channel with index {}. There are {} channels registered. To see the list, message me with '.lc'.".format(index, len(datapipe.channels)))	
						return
						
					except:	
						traceback.print_exc()
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
					reply("You do not have the necessary permissions to execute function '{}' in channel '{}'.".format(func_params[0], msg.source.channel.name), msg)
					
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
			reply(eval(random.choice(funcBanter)), msgobj)
	
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
		# datapipe.source = item.source
		if item.cmd not in ignore_commands: print("{} -- {} {}".format(time.strftime("%c"), item.cmd, item.args))
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
		EternalSender.start(0.500)
		MainLoop.start(0.25)
		reactor.run()
	except:
		reactor.stop()
		traceback.print_exc()
