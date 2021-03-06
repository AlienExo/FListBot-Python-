from __future__ import unicode_literals

#instead of user.age, attach a .data dict to users and rewrite.
#getattr lookup -> dict lookup -> FList api -> Second lookup, dict "not set", return "not set"
#write def get() or something for User

from collections import deque
import config
from copy import deepcopy
import datetime
import FListAPI
from hashlib import md5
import importlib
import json
import math
import os
import personality
import random
import re
import songs
import string
import sys
# import threading
import time
import traceback
from urllib import urlencode, quote_plus
import urllib2
import utils
import yaml
from twisted.internet import defer, reactor, task, threads
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS

ignore_commands = ['FLN', 'STA', 'NLN', 'PIN', 'MSG', 'PRI', 'TPN', 'LIS', 'ORS', 'IDN', 'VAR', 'CDS', 'COL', 'ICH', 'JCH', 'LCH', 'CON', 'HLO', 'ERR', 'CKU']
opener 			= urllib2.build_opener()
opener.addheaders.append(('Cookie', 'warning=1'))
startuptime 	= datetime.datetime.now()
sendQueue		= deque()
recvQueue 		= deque()
EventQueue 		= deque()

admins 			= utils.loadData('admins', list)
chanAdmins		= []
banBanter		= utils.loadData('banbanter', list)
funcBanter		= utils.loadData('funcbanter', list)
joinmsgDict 	= utils.loadData('joinmsg', dict)
server_vars 	= {}

class Channel():
	def __init__(self, name, ckey=None):
		self.name=name
		self.key = ckey if ckey is not None else self.name
		self.minage = 0
		self.alertNoAge = False
		self.alertUnderage = False
		self.index = None
		self.users=[]
		self.ops =[]
		self.lastjoined = []
		self.whitelist = []
		self.blacklist = []
		self.ignoreops = []
		self.isPublic = True
		
	def userJoined(chan, character):
		char = getUser(character)
		chan.users.append(char.name)
		chan.lastjoined.append(char.name)
		# if datapipe.personality != None: 
		telling(char, chan)
		# else: datapipe.personality.code.telling(datapipe.FListProtocol, char, chan)
				
	def userLeft(chan, character):
		name = getUser(character).name
		try:
			chan.users.remove(name)
			chan.lastjoined.remove(name)
			datapipe.lastseenDict[name]=datetime.datetime.now()
		except ValueError: pass
		except:
			traceback.print_exc()
		
	def join(self):
		sendRaw("JCH {}".format(json.dumps({'channel':self.key})))
		for pos, item in enumerate(datapipe.channels):
			if item==None:
				datapipe.channels[pos]=self
				# self.index = len(datapipe.channels)-1	
				self.index = pos	
				print("Joining channel '{}', index {}.".format(self.name, self.index))
				return
		datapipe.channels.append(self)
		self.index = len(datapipe.channels)-1
		print("Joining channel '{}', index {}.".format(self.name, self.index))
		
	def part(self):
		sendRaw("LCH {}".format(json.dumps({'channel':self.key})))
		datapipe.channels[self.index]=None
		self.index=None
	
	def toggleLock(self):
		self.status = not self.status
		sendRaw("RST {}".format(json.dumps({'channel':self.key, 'status': ['private', 'public'][self.status]})))
		reply("Channel '{}' set to '{}'.".format(self.name, ['private', 'public'][self.status]))
		
class User():
	def __init__(self, name):
		self.name = name
		self.status = "online"
		self.channels=[]
		self.data={}
		self.kinks=()
		# datapipe.lastseenDict[self.name]=datetime.datetime.now()
		
	# def __nonzero__(self):
		# print("Calling User.__nonzero__")
		# return True
		
	def parseFListData(self, data, item):
		try:
			for x in data:
				#print("\t\tSetting '{}' to '{}'".format(str(x).lower(), data[x]))
				# setattr(self, str(x).lower(), data[x])
				self.data[str(x).lower()]=data[x]
		except Exception, exc:
			print exc
		
		try:
			self.age = int(re.search('(\d{1,5})', data['Age']).group(0))
			# self.weight = int(re.search('(\d{1,5})', data['Weight']).group(0))
		except:
			self.data['age']=0
			self.age=0
			
		if not item.lower() in self.data.keys(): return "Not Assigned"
		else: return self.data[item.lower()]

	"""		
	def _ga(self, item):
		try:
			_item = self.data[item.lower()]
			return _item
		except KeyError:
			# d = threads.deferToThread(FListAPI.getCharInfo(self.name, datapipe.key))
			# d.addCallback(self.parseFListData, item)
			# return d
			data = FListAPI.getCharInfo(self.name, datapipe.key)
			result = self.parseFListData(data, item)
			return result
			
		except:
			traceback.print_exc()
			
	def __ga(self, item):
		return item
	"""		
	def __getattr__(self, item):
		try:
			_item = self.data[item.lower()]
			return _item
		except KeyError:
			# d = threads.deferToThread(FListAPI.getCharInfo(self.name, datapipe.key))
			# d.addCallback(self.parseFListData, item)
			# return d
			data = FListAPI.getCharInfo(self.name, datapipe.key)
			result = self.parseFListData(data, item)
			return result
			
		except:
			traceback.print_exc()

		"""	
		d = defer.maybeDeferred(self._ga, item)
		d.addCallback(self.__ga)
		return d
		"""
		
	def kick(self, channel):
		channel = getChannel(channel)
		req = json.dumps({"operator":"{}".format(config.character),"channel":channel.key,"character":self.name})
		sendRaw("CKU {}".format(req))

class DataPipe():
	def __init__(self):
		self.character		= config.character
		self.helpDict 		= utils.loadData('help', dict)
		self.messageDict 	= utils.loadData('{} messages'.format(config.character), dict)
		self.functions		= config.functions
		self.channels		= [Channel('Dummy')]
		self.channelDict	= utils.loadData('channels', dict)
		self.songs 			= []
		self.pluginexit		= []
		self.pluginloops	= []
		self.dict_limits 	= {}
		self.plugins 		= {}
		self.usersDict 		= {}
		self.lastseenDict 	= utils.loadData('lastseen', dict)
		self.personality	= None
		self.Aurica			= ""
		self.Despedia		= False
		
	def loadData(self, file, expected=dict):
		return utils.loadData(file, expected=dict)
		
	def saveData(self, data, file):
		utils.saveData(data, file)

	def reply(self, message, item, path_override=None):
		reply(message, item, path_override)
		
	def writeLog(self, text):
		utils.log(text, 1)

datapipe = DataPipe()

def sendRaw(msg):
	sendQueue.append(msg)
	
def sendText(message, route=1, char=config.character, chan='PM'):
	"""	Route	0			1			2				3				4
		Target	PM		Channel		Channel+Prefix	Action in MSG	Action in PRI"""
	char=getUser(char).name
	if chan=='PM': route=0
	else: chan=getChannel(chan).key
	if route == 0:
		msg = "PRI {}".format(json.dumps({'recipient':char, 'message':message})).encode('utf-8', 'replace')
	elif route<3:
		prefix = '{}: '.format(char)
		msg = "{}{}".format(prefix*(route>1), message)
		msg = "MSG {}".format(json.dumps({'channel':chan, 'message':message}))
	elif route<5:
		message = "/me "+message
		if route==4 or chan=='PM': 
			path="PRI" 
			msg = "{} {}".format(path, json.dumps({'recipient':char, 'message':message}))
		else: 
			path="MSG"
			msg = "{} {}".format(path, json.dumps({'channel':chan, 'message':message}))
	sendQueue.append(msg)
	
def reply(message, item, path_override=None):
	if not hasattr(item, 'access_type'): item.access_type = 0
	if path_override is not None: path = path_override
	else: path = item.access_type
	sendText(message, path, item.source.character.name, item.source.channel.name)
	
def saveChannelSettings():
	chans = {}
	for name, chaninst in datapipe.channelDict.items():
		if (hasattr(chaninst, 'minage') and chaninst.minage!=0) or (len(chaninst.whitelist) > 0): 
			newinst = deepcopy(chaninst)
			newinst.users = []
			newinst.lastjoined = []
			newinst.index = []
			chans[name]=newinst
	utils.saveData(chans, 'channels')
	del chans

# def parseFListData(self, data):
	# try:
		# print "Processing FList data for {}".format(self.name)
		# for x in data:
			# print("Setting ", str(x), " to ", data[x])
			# setattr(user, str(x).lower(), data[x])
	# except Exception, exc:
		# print exc
	# try:
		# user.age = int(re.search('(\d{1,5})', data['Age']).group(0))
		# user.weight = int(re.search('(\d{1,5})', data['Weight']).group(0))
	# except KeyError as error: 
		# setattr(user, "".format(error).lower(), 0)

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
		if (x.key == channel) or (x.name == channel): 
			return x
	chan = Channel(channel)
	datapipe.channelDict[channel]=chan
	return chan
		
datapipe.getUser = getUser
datapipe.getChannel = getChannel
	
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
		self.cf_level = 3
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
				if self.cmd == 'PRI': chan=Channel("PM", None)
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
	print("Loading plugins. Please stand by.")
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
			print("\tPlugin '{}' successfully initialized.".format(name))
	print("Import complete.\n")
		
def checkAge(char, chan):
	if char.name in chan.whitelist: 
		print ("\t{} is a whitelisted user for {}".format(char.name, chan.name))
		chan.userJoined(char.name)
		return
		
	elif (char.age >= chan.minage):
		print char.age, chan.minage, char.age>=chan.minage, type(char.age)
		utils.log("User {} has passed inspection for {} (Age>={}), claiming to be {} years old.".format(char.name, chan.name, chan.minage, char.age))
		chan.userJoined(char.name)
		return
		
	else:
		xadmins = sorted(map(getUser, chan.ops), key=lambda *args: random.random())
		xadmins = filter(lambda x: x.status in ['online', 'looking'], xadmins)
		y = xadmins[0]
		try:
			if not isinstance(y, User): raise UnboundLocalError
			if char.age<chan.minage and char.age!=0:
				try:
					banter = eval(banter)
				except SyntaxError:
					pass
				banter = chan.name+": "+banter
				sendText(banter, 2, char, chan)
				if config.character in chan.ops:
					utils.log("Auto-kicking underage user {}.".format(char.name), 3, chan.name)
					sendText("Your character {} is under the minimum age of {} for the channel '{}' and has thus been removed. If you wish to return, please do so with an of-age alias. {} wishes you a nice day.".format(char.name, chan.minage, config.character), 0, char)
					char.kick(chan)
				elif chan.alertUnderAge:
					sendText("User [color=red]below channel \"{}\"'s minimum age of {}:[/color] [user]{}[/user].".format(chan.name, chan.minage, char.name), 0, char=y)
					utils.log("User {} under minimum age of {} for {}. Alerting {}.".format(char.name, chan.minage, chan.name, y.name),3, chan.name)
					banter = random.choice(banBanter)
			
			elif char.age == 0:
				if chan.alertNoAge:
					utils.log("User {}'s age cannot be parsed. Informing Mod {}".format(char.name, y.name), 3, chan.name)
					sendText("Can't verify user '[user]{}[/user]' for {} (minimum age set to {}). Please verify. [sub]To add user to the channel's whitelist, reply '.white {} {}' in a PM (or - without the number - in the channel to whitelist for).[/sub]".format(char.name, chan.name, chan.minage, char.name, char.name, chan.index), 0, char=y)
				return
			
		except UnboundLocalError:
			utils.log("Cannot fetch a mod, none logged in or set to online. Cannot verify user {} for {}.".format(char.name, chan.name), 3, chan.name)
			for op in chan.ops:
				op = getUser(op)
				print("Op: {} Status: {}".format(op.name, op.status))
			return

		except: traceback.print_exc()

class FListProtocol(WebSocketClientProtocol):
	def __init__(self):
		datapipe.FListProtocol = self
		
	def onOpen(self):
		datapipe.key = FListAPI.getKey()
		reactor.callLater(0.75, sendRaw, "IDN {}".format(json.dumps({"method":"ticket","account":config.account,"character":"Cogito","ticket":datapipe.key,"cname":"cogito","cversion":config.version})))

	def onMessage(self, msg, binary):
		# msg = msg.decode('ascii', 'ignore')
		#if msg[:3] not in ['LIS', 'NLN', 'ORS', 'STA', 'CDS']: print msg
		message = Message(msg)
		recvQueue.append((message, self))
		
	def reply(self, message, item, path_override=None):
		reply(message, item, path_override)
		
	def writeLog(self, text):
		utils.log(text, 1)

	def ACB(self, item):pass
	
	def ADL(self, item):pass
		#ops = item.args['ops']
		#for op in ops:
		#	chanAdmins.append(op)
		
	def BRO(self, item):
		utils.log("Broadcast from {}: {}".format(item.args['character'], item.args['message']), 1)
		
	def CBU(self, item):
		chan = getChannel(item.args['channel']).name
		utils.log("{} was banned from {} by {}".format(item.args['character'], chan, item.args['operator']), 3, chan)
		
	def CCR(self, item):
		print ("\t\tCCR RESPONSE")
		print item.args, item.params
		
	def CDS(self, item):pass
	
	def CIU(self, item):
		chan = getChannel(item.args['channel'])
		utils.log("Invited to {}. Joining channel.".format(chan.name), 1)
		chan.join()
	
	def CKU(self, item):
		chan = getChannel(item.args['channel']).name
		utils.log("{} was kicked from {} by {}".format(item.args['character'], chan, item.args['operator']), 3, chan)
		if config.banter and random.random<=config.banterchance:
			a = eval(random.choice(banBanter))
			reply(a, item, 2)
	
	def COA(self, item):
		chan = getChannel(item.args['channel'])
		char = getUser(item.args['character'])
		if not char.name in chan.ops:
			chan.ops.append(char.name)
			
	def COL(self, item):
		ops = item.args['oplist']
		chan = getChannel(item.args['channel'])
		for op in ops:
			if not op in chan.ops: 
				chan.ops.append(op)
				chanAdmins.append(op)
		print ("Channel operators for "+chan.name+": "+ ", ".join(chan.ops))
		
	def CON(self, item):
		with open('./data/user stats.txt', 'a') as io:
			io.write("{} {}\n".format(time.strftime("%c"), item.args['count']))
		utils.log("{} users online.".format(int(item.args['count'])), 0)
			
	def COR(self, item):
		chan = getChannel(item.args['channel'])
		try:
			chan.ops.remove(item.args['character'])
			chanAdmins.remove(item.args['character'])
		except:
			traceback.print_exc()
		
	def ERR(self, item):
		utils.log("FList Error: Code {}. '{}'".format(item.args['number'], item.args['message']), 2)
			
	def FLN(self, item):
		char = getUser(item.args['character'])
		for chan in datapipe.channelDict.values():
			if char.name in chan.users:
				utils.log("{} logged out.".format(char.name), 3, chan.name)
				chan.userLeft(char)
		
	def FRL(self, item): pass
	
	def HLO(self, item): 
		utils.log("Connection established.", 1)
		reactor.callLater(1.0, sendRaw, "ORS")
			
	def ICH(self, item):
		chan = getChannel(item.args['channel'])
		if chan.index==None: return
		chars = map(getUser, item.args['users'])
		for x in chars:
			if (not x.name in chan.users): chan.users.append(x.name)
			datapipe.lastseenDict[x.name]=datetime.datetime.now()

	def IDN(self, item): pass
	def IGN(self, item): pass
		
	def JCH(self, item):
		char = getUser(item.args['character']['identity'])
		chan = getChannel(item.args['channel'])
		chan.userJoined(char)
		if char.name == config.character: return
		if chan.name[:2]=="ADH": 
			chan.name=item.args['title']
			chan.key=item.args['channel']
		utils.log("User {} has joined '{}'.".format(char.name, chan.name), 3, chan.name)
		if char.name in chan.blacklist: 
			utils.log("User {} is blacklisted and was promptly removed from '{}'.".format(char.name, chan.name), 3, chan.name)
			chan.kick(char)
			return
			
		if chan.minage == 0: return
		else:
			checkAge(char, chan)
						
	def LCH(self, item):
		chan = getChannel(item.args['channel'])
		if chan.index==None: return
		char = getUser(item.args['character'])
		utils.log("User {} has left '{}'.".format(char.name, chan.name), 3, chan.name)
		chan.userLeft(char)
					
	def LIS(self, item):
		chars = item.args['characters']
		for data in chars:
			char = getUser(data[0])
			char.status = data[2]
			
	def LRP(self, item):pass
	def NLN(self, item):pass
	
	def ORS(self, item):
		try:
			print "\nParsing ORS data. Some Assembly Required."
			data = item.args['channels']
			for part in data:
				channel = getChannel(part['title'])
				channel.key = part['name']
			for x in config.channels: 
				getChannel(x).join()
		except Exception:
			utils.log(traceback.format_exc(), 2)
		
	def PIN(self, item):sendRaw("PIN")
	
	def PRF(self, item):
		"""PRD
		Profile data commands sent in response to a PRO client command.
		Syntax
		>> PRD { "type": enum, "message": string, "key": string, "value": string }
		The message field is sent when the type is "start" or "end", as it will be displayed to the user. First, a PRD command of type "start" is sent, then a series of PRD commands of type "info" and "select", holding "key" "value" properties of the character's profile properties. Then, finally a PRD command of type "end" is sent. 
		"""
		#receive data, from flag: know what to return. Defer() the process? Callback?
	
		pass
	
	def PRO(self, item):
		#send request
		pass		
		
	def RLL(self, item):pass
					
	
	def STA(self, item):
		if item.args['character'] in chanAdmins:
			getUser(item.args['character']).status = item.args['status']			
	
	def SYS(self, item):
		utils.log(item.args['message'], 1)
	
	def TPN(self, item): pass
		
	def VAR(self, item):
		server_vars[item.args["variable"]]=item.args["value"]
		if item.args["variable"]=="msg_flood":
			new = item.args["value"]*1.5
			if new<config.minSendDelay: new = config.minSendDelay
			print("\tDetected server-side flood control. Self-adjusting: sending output every {} milliseconds.".format(new*1000))
			server_vars['permissions']=1
			EternalSender.stop()
			EternalSender.start(new)
			
#===========================================

	def listIndices(self, item):
		reply("List of active channels and their indices for channel-specific commands:", item, 0)
		for num, chan in enumerate(datapipe.channels):
			if num==0: continue
			if chan == None: continue
			reply("Index #{}: [session={}]{}[/session]".format(num, chan.name, chan.key), item, 0)
			
	def whitelist(self, item):
		candidate = item.params
		# datapipe.whitelist.append(candidate)
		item.source.channel.whitelist.append(candidate)
		reply("{} has been whitelisted for {}.".format(candidate, item.source.channel.name), item)	
		utils.log("{} has been whitelisted for {} by {} (level {} access).".format(candidate, item.source.channel.name, item.source.character.name, item.cf_level), 1)
		saveChannelSettings()
		#utils.saveData(datapipe.whitelist, 'whitelist')

	# def blacklist(self, item):
		# candidate = item.params
		# datapipe.blacklist.append(candidate)
		# item.source.channel.blacklist.append(candidate)
		# reply("{} has been blacklisted for {}.".format(candidate, item.source.channel.name), item)
		# utils.log("{} has been blacklisted for {} by {} (level {} access).".format(candidate, item.source.channel.name, item.source.character.name, item.cf_level), 1)
		# saveChannelSettings()
		
	def auth(self, item):
		if md5(item.params).hexdigest() == config.masterkey:
			reply("Was ki ra hyma yor, futare ANSUL_{}".format(config.character.upper()), item, 0)
			datapipe.Aurica = item.source.character.name
		
	def _admin(self, item):
		if datapipe.Aurica:
			config.admins.append(datapipe.Aurica)
			reply("Was yea ra chmod b111111111/n => zuieg {}_ANSUL_{}".format(item.source.character.name.upper(), config.character.upper()), item)
			datapipe.Aurica = ""
		else:
			reply("", item)

	def op(self, item):
		candidate = item.params
		chan = item.source.channel
		if not candidate in chan.ops: chan.ops.append(candidate)
		if not candidate in chanAdmins: chanAdmins.append(candidate)
		reply("{} has been made a bot operator for {}.".format(candidate, item.source.channel.name), item)
		utils.log("{} has been a bot operator for {} by {} (level {} access).".format(candidate, chan.name, item.source.character.name, item.cf_level), 1)
		
	def deop(self, item):
		candidate = item.params
		chan = item.source.channel
		try:
			chanAdmins.remove(candidate)
			chan.ops.remove(candidate)
			reply("{} is no longer a bot operator for {}.".format(candidate, item.source.channel.name), item)
			utils.log("{} has is no longer a bot operator for {} by order of {} (level {} access).".format(candidate, item.source.channel.name, item.source.character.name, item.cf_level), 1)
		except IndexError:
			reply("[color=red][b]Error:[/b][/color] {} was not found in the bot operator registry for {}. Please check spelling and capitalization.".format(candidate, item.source.channel.name), item)
				
	def join(self, item):
		chan = getChannel(item.params)
		reply("Command received. Attempting to join '{}'".format(chan.name), item, 0)
		utils.log("Joining channel '{}' by order of {} (level {} access).".format(chan.name, item.source.character.name, item.cf_level), 1)
		chan.join()
	
	def leave(self, item):
		chan = item.source.channel
		reply("Command received. Leaving '{}'".format(chan.name), item, 0)
		utils.log("Leaving channel '{}' by order of {} (level {} access).".format(chan.name, item.source.character.name, item.cf_level), 1)
		chan.part()
	
	def kick(self, item):
		char = item.params
		sendRaw("CKU {}".format(json.dumps({'channel': item.source.channel.key, 'character': char})))
		reply("Command received. Removing '{}' from {}.".format(character, source.channel), item, 0)
		utils.log("{} (level {} access) has kicked user {} from {}.".format(item.source.character.name, item.cf_level, char, item.source.channel.name), 3, chan.name)
	
	def ban(self, item):
		char = item.params	
		sendRaw("CBU {}".format(json.dumps({'channel': item.source.channel.key, 'character': char})))
		reply("Command received. Banning '{}' from {}.".format(character, source.channel), item, 0)
		#item.source.channel.blacklist.append(char)
		utils.log("{} (level {} access) has banned {} from {}.".format(item.source.character.name, item.cf_level, char, item.source.channel.name), 3, chan.name)
		
	def unban(self, item):
		char = item.params
		sendRaw("CBU {}".format(json.dumps({'channel': item.source.channel.key, 'character': char})))
		utils.log("{} was unbanned from {} by {} (level {} access)".format(item.params, item.source.channel.name, item.source.character.name, item.cf_level), 1, item.source.channel.name)
		
		#try:
			#item.source.channel.blacklist.remove(item.params)
		#except IndexError:
			#reply("Character '{}' not in Blacklist for {}. Please check channel, check spelling, and retry.".format(item.params, item.source.channel.name), item)
		#else:
			#reply("Character '{}' removed from blacklist for {}.".format(item.params, item.source.channel.name), item)
			#utils.log("{} removed from blacklist for {} by {} (level {} access)".format(item.params, item.source.channel.name, item.source.character.name, item.cf_level), 1, item.source.channel.name)
			
	def exec_purger(self, item):
		reply("Rrha yea ra EXEC_PURGER >> {}_ANSUL_{}".format(item.source.character.name.upper(), config.character.upper()), item)
		EventQueue.append((item.source.character.name, 'Was ki ra exec syec parge ', 'kick'))
		
	def method_metafalica(self, item):
		newchannel=item.params
		sendRaw("CCR {}".format(json.dumps({'channel':newchannel})))
	
	def _method_metafalica(self, item):
		reply("Was ki ga exec hymme METAFALICA reta tie manac dor.", item)
		EventQueue.append((item.source.character.name, 'exec hymme METAFALICA ', 'method_metafalica'))
	
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
		reply("{} (level {} access) made {} timeout from '{}' for {} minutes.".format(character, item.cf_level, item.source.channel.name, length), item, 0)
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
			
	def ignore(self, item):
		if not item.source.character.name in item.source.chan.ignoreops:
			item.source.chan.ignoreops.append(item.source.character.name)
			reply("You have been appended to the ignore list for {} and will no longer be pinged when AgeCheck is active.".format(item.source.channel.name), item)
			utils.log("{} opted to be ignored in {}".format(item.source.character.name, item.source.channel.name), 1)
		else:
			item.source.chan.ignoreops.remove(item.source.character.name)
			reply("You have been removed from the ignore list for {}.".format(item.source.channel.name), item)
			utils.log("{} opted to no longer be ignored in {}".format(item.source.character.name, item.source.channel.name), 1)
			
	def minage(self, item):
		try:
			age = int(item.args[0])
			item.source.channel.minage = age
			if age == 0:
				reply("Age Check deactivated by {} (level {} access).".format(item.source.character.name), item)
				return
			reply("Age Check activated by {}. Alerting administrators to characters below age {}.".format(item.source.character.name, personality.spokenNumber(age)), item)
			utils.log("{} set the minimum age for {} to {}.".format(item.source.character.name, item.source.channel.name, age), 3, item.source.channel.name)
		except ValueError:
			reply("Error: Cannot parse {} as a number.".format(item.args[0]), item, 0)
		else:
			saveChannelSettings()
			
	def alertUnderAge(self, item):
		try:
			item.source.channel.alertUnderage = not item.source.channel.alertUnderage
			reply("Alerts for underage characters are {}. Moderators will{} be alerted to underage characters.".format(['off', 'on'][item.source.channel.alertUnderage], ' not'*(not item.source.channel.alertUnderage)), item)
			utils.log("{} set the underage alert for {} to '{}'.".format(item.source.character.name, item.source.channel.name, item.source.channel.alertUnderage), 3, item.source.channel.name)
		except:
			traceback.print_exc()
		else:
			saveChannelSettings()
			
	def alertNoAge(self, item):
		item.source.channel.alertNoAge = not item.source.channel.alertNoAge
		reply("Alerts for characters with no age listed are {}. Moderators will{} be alerted to such characters.".format(['off', 'on'][item.source.channel.alertNoAge], ' not'*(not item.source.channel.alertNoAge)), item)
		utils.log("{} set the mod alert for {} to '{}'.".format(item.source.character.name, item.source.channel.name, item.source.channel.alertNoAge), 3, item.source.channel.name)
		saveChannelSettings()
		
	def bingo(self, item):
		reply("[url=http://i.imgur.com/fUHxLPQ.png]Collect your FList Bingo Card here.[/url]", item)
		
	def rainbowText(self, item):
		slist=[]
		a = len(item.params)
		b,c = divmod(a, 6)
		print a, b, c
		for x in xrange(0, a, b):
			slist.append(item.params[x:x+b])
		if c == 0: slist.append('')
		else: slist.append(item.params[a-c:])
		#if len(slist)==8:
		#	slist[6]="".join(slist[6:])
		#	slist=slist[:7]
		sendText("[color=red]{}[/color][color=orange]{}[/color][color=yellow]{}[/color][color=green]{}[/color][color=cyan]{}[/color][color=blue]{}[/color][color=purple]{}[/color]".format(*slist), 2, chan=item.source.channel)
		
	def lockdown(self, item):
		datapipe.Despedia = not datapipe.Despedia
		utils.log("Lockdown {} by {} (level {} access). None but hardcoded administrators may issue commands until lifted.".format(['disengaged', 'engaged'][datapipe.Despedia], item.source.character.name, item.cf_level), 1)
		reply("Lockdown {} by {} (level {} access). None but hardcoded administrators may issue commands until lifted.".format(['disengaged', 'engaged'][datapipe.Despedia], item.source.character.name, item.cf_level), item, 2)
		
	def hibernation(self, item):
		try:
			reply("Command accepted. Shutting down.", item, 2)
			utils.log('Shutting down by order of {} (level {} access). Stopping reactor and writing data.'.format(item.source.character.name, item.cf_level), 1)
			reactor.stop()
			chans = {}
			saveChannelSettings()
			utils.saveData(datapipe.lastseenDict, 'lastseen')
			for x in datapipe.pluginexit:
				try:
					func = getattr(x, "exit", None)
					if callable(func): func()
				except:
					traceback.print_exc()
		except Exception, error:
			utils.log("Error during shutdown: {}".format(error), 2)
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
			reply("{} F-List Bot, v{}.".format(config.character, config.version), msg, 0)
			reply("Please note: All commands are executed in the channel they are received from. In case of a PM, you may specify a channel via its ID number. E.g. .kick A Bad Roleplayer 1 will kick A Bad RolePlayer from channel #1. To get a list of IDs and channels, use the command '.lc'. A command without an ID will be parsed as the 'default' channel, here: {}".format(config.channels[0]), msg, 0)
			reply("The following functions are available:", msg, 0)
			func=[]
			for x in datapipe.helpDict.keys():
				func.append(x)
			func.sort()
			for x in func:
				reply("--{}: {!s}".format(x, datapipe.helpDict[x]), msg, 0)

	def tell(self, msg):
		sender = msg.source.character.name
		a = msg.params.find(':')
		if a ==-1:
			reply("You need to put a ':' after the recipient's name, darling.", msg, 1)
			return
		sender = msg.source.character.name
		recipient = msg.params[:a]
		message = msg.params[a:]
		sendtime = datetime.datetime.now()
		data = (sender, message, sendtime)
		try:
			messages = datapipe.messageDict[recipient.lower()]
		except TypeError:
			datapipe.messageDict = {}
			messages = []
		except KeyError:
			messages = []
		if len(messages)>config.messagelimit:
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
		
	def infodump(self, msg):
		#debug command, print __attributes__ or other metadata. get object with __getattr__ and disassemble.
		pass
		
	def scan(self, msg):
		numeric = False
		stats = False
		anon = False
		if "-n" in msg.args:
			numeric=True
			msg.args.remove('-n')
			msg.params=" ".join(msg.args)
		if "-s" in msg.args:
			stats=True
			msg.args.remove('-s')
			msg.params=" ".join(msg.args)
		if "-a" in msg.args:
			anon=True
			msg.args.remove('-a')
			msg.params=" ".join(msg.args)		
		
		msg.params = msg.params.lower()
		print("\tEngaging data gathering subroutines. Please stand by.")
		users=map(getUser, msg.source.channel.users)
		assocData = map(lambda x: (User.__getattr__(x, msg.params), x.name), users)
		oldDataLen=len(assocData)
		print("Starting with processing of {} entries.".format(len(assocData)))
		data=map(lambda x: x[0], assocData)
		if numeric: 
			_data = []
			for index, item in enumerate(assocData):
				n=str(item[0]).replace(',', '.')
				try:
					n=float(re.search('\d{1,5}\.?\d{0,2}', n).group(0))
					if not n==0: 
						_data.append((n, item[1]))		
				except:pass
			assocData = dict(_data)
			data=map(lambda x: x[0], _data)
		print("\tData processing complete. {} entries now available.".format(len(data)))
		if len(data)==0: return
		print("Beginning analysis.")
		if not stats:	
			permutations = set(data)
			results = []
			total = 0.0
			for permutation in permutations:
				permutationCount = data.count(permutation)
				results.append((permutation, permutationCount))
				total += permutationCount
			analysis = reduce(lambda x,y: x+"'{}': {} occurences ({:.2%}) ".format(y[0], y[1], y[1]/total), results, "")
		else:
			dataTotal = reduce(lambda x,y: x+y, data, 0.0)
			dataAvg = dataTotal/len(data)
			dataStDev=map(lambda x: (x-dataAvg)**2, data)
			dataStDev=reduce(lambda x,y: x+y, dataStDev, 0.0)
			dataStDev=math.sqrt(dataStDev/len(data))
			dataMedian=sorted(data)[len(data)//2]
			analysis = "Mean: {:.2f}. Median: {:.2f}. Maximum: {:.2f}{}. Minimum: {:.2f}{}. Standard Deviation: {:.3f}. (Only nonzero entries were counted).".format(dataAvg, dataMedian, max(data), ['', ' ({})'.format(assocData[max(data)])][anon], min(data), ['', ' ({})'.format(assocData[min(data)])][anon], dataStDev)
		analysis = "Search of users for '{}' complete. {} of {} entries could be processed. {}".format(msg.params, len(data), oldDataLen, analysis)
		print analysis
		reply(analysis, msg)
			
		
def parseText(self, msg):
	if msg.params[:5]==".auth": utils.log("root-level login attempt by {}".format(msg.source.character.name), 0)
	elif not msg.params[:3]=="/me":utils.log("{}: \"{}\"".format(msg.source.character.name, msg.params), 3, msg.source.channel.name)
	else: utils.log("{}{}".format(msg.source.character.name, msg.params[3:]), 3, msg.source.channel.name)
	# SUPER EXPERIMENTAL DANGER WILL ROBINSON
	if len(EventQueue)>0:
		try: 
			person, trigger, func = EventQueue.popleft()
			if item.source.character.name == person and trigger in item.params:
				item.params = item.params.split(trigger)[1]
				print item.params
				try:
					handle_all_the_things(self, msg, func)
				except:
					EventQueue.appendleft((person, trigger, func))
					traceback.print_exc()

		except IndexError: pass
		# END SUPER EXPERIMENTAL
	try:
		if datapipe.Despedia and msg.source.character.name not in config.admins: return
		if msg.args[0] in datapipe.functions.keys():
			func = msg.args[0]
			msg.args = msg.args[1:]
			msg.params = " ".join(msg.args)
			if msg.source.channel.name == "PM": 
				msg.access_type = 0
				try:
					index = int(msg.args[-1])
					msg.args = msg.args [:-1]
					msg.params = " ".join(msg.args)
				except IndexError: pass
				except ValueError: pass
				else:
					try:	
						chan = datapipe.channels[index]
						print("\tIndex found. Rerouting PM command '{}' from channel 'PM' into '{}'.".format(func, chan.name))
						msg.source.channel = chan
					except IndexError:
						reply("Command not executed: There is no channel with index {}. There are {} channels registered. To see the list, message me with '.lc'.".format(index, len(datapipe.channels)), msg)	

			else: 
				msg.access_type = 1
			func_params = datapipe.functions[func]
			if msg.access_type in func_params[2]:
				# print("\tCorrect access type")
				msg.cf_level = 2
				if msg.source.character.name in config.admins: msg.cf_level=0
				elif (msg.source.channel.name!="PM") and (msg.source.character.name in msg.source.channel.ops): msg.cf_level = 1
				# elif msg.source.character.name in chanAdmins: msg.cf_level=1
				if msg.cf_level <= func_params[1]:
					# print ("\tHandling '{}'...".format(func_params[0]))
					handle_all_the_things(self, msg, func_params[0])
					return
				else:
					reply("You do not have the necessary permissions to execute function '{}' in channel '{}'.".format(func_params[0], msg.source.channel.name), msg)
					return
	except IndexError:
		traceback.print_exc()
		
	for songinst in datapipe.songs:
		if songinst.singer == msg.source.character.name:
			listen(msg, songinst)

	for song, lines in songs.dict_songs.items(): 
		try:
			if songs.matcher(lambda x: x==" ", msg.params, lines[0]).ratio() > 0.75:
				asong=songs.Song(msg.source.character.name, song)
				datapipe.songs.append(asong)
				listen(msg, asong)
		except IndexError: pass
		except Exception as function_error:
				print("Error whilst listening to text command: {}".format(function_error, function_error.args), 2)
				traceback.print_exc()

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
			func = getattr(FListProtocol, '{}'.format(cmd), None)
			if callable(func):
				func(self, msgobj)
			else:
				utils.log("Cannot execute unregistered command '{}'. Check entry in config.functions/other sources and note proper capitalization.".format(msgobj.cmd, msgobj.args), 2)
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
	
def listen(msg, songinst):
	print("\tListening to {}; limit {}".format(songinst.song, songinst.level))
	try:
		songinst.nextline = songinst.songiterator.next()
	except StopIteration:
		reply("Song rejected.", 0)
		datapipe.songs.remove(songinst)
		return
	
	if songs.matcher(lambda x: x == " ", msg.params, songinst.nextline).ratio() > 0.7:
		songinst.level+=1
		if songinst.song in songs.dict_answers:
			try:
				sreply = songs.dict_answers[songinst.song][songinst.level]
				reply(str(sreply), msg, 2)
			except KeyError, IndexError:
				pass
	
	elif ("exec waath" in msg.params.lower()):
		datapipe.songs.remove(songinst)
	
	else:
		print("No match, no endline.")
		reply("Access denied", msg)
		datapipe.songs.remove(songinst)
		
	if songinst.level >= songinst.maxLevel:
		try:
			handle_all_the_things(datapipe.FListProtocol, msg, songinst.func)
		finally:
			datapipe.songs.remove(songinst)

def _telling(char):
	#message: ('Sender', 'Message', timestamp)
	messages=[]
	try:
		for x in datapipe.messageDict[char.name.lower()]:
			d = utils.timeFrac(datetime.datetime.now()-x[2])
			# returns (formatted string w/ fractoin, (major number, numeric fraction, time unit))
			messages.append((x[0], x[1], d))
	except KeyError: return []
	else:
		del(datapipe.messageDict[char.name.lower()])
		utils.saveData(datapipe.messageDict, '{} messages'.format(config.character))
		return messages			
			
def telling(char, chan):
	messages = _telling(char)
	c = len(messages)
	if c==0: return
	sendText("[color=green]{}, you have {} new message{}:[/color]".format(char.name, personality.spokenNumber(c), 's'*(c>1)), 1, char, chan)
	for x in messages:
		sendText("[color=yellow]<{}> [color=green]{}[/color] ({} ago)[/color]".format(x[0], x[1], x[2][0]), 2, char, chan)
						
def qsend():
	try:
		item = sendQueue.popleft()
		datapipe.FListProtocol.sendMessage(item.encode('utf-8'))
	except IndexError:	pass
		
def mainloop():
	try:
		"""doesn't do anything if EventQueue empty. instead of eventQueue, threading and conditions?"""
		item, self = recvQueue.popleft()
		if datapipe.personality != None: 
			datapipe.personality.code.handle(self, item) 
		if item.cmd not in ['MSG', 'PRI']:
			handle_all_the_things(self, item, item.cmd)
			return
		else:
			parseText(self, item)
	except IndexError: pass
	
if __name__ == '__main__':
	load(datapipe)
	datapipe.personality = personality.__init__(config)
	factory = WebSocketClientFactory("ws://chat.f-list.net:{}".format(config.port), debug = True)
	factory.protocol = FListProtocol
	EternalSender = task.LoopingCall(qsend)
	MainLoop = task.LoopingCall(mainloop)
	print('Booting Cogito, version {}. Connecting to account "{}". Condition all green. Get set.'.format(config.version, config.account))
	connectWS(factory)
	try:
		print('Starting reactor.')
		EternalSender.start(0.75)
		MainLoop.start(0.2)
		reactor.run()
	except:
		reactor.stop()
		traceback.print_exc()
