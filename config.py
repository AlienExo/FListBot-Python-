import json
from urllib import urlencode
import urllib2

# admins defines who can issue admin-level commands to the bot. Looks like this:
# admins = ["First Admin", "second admin", "xXx third admin-dono xXX"]
#please be precise, else python pukes up an error. TIA. 
admins = 	["Admin1", "Admin Number 2"]

#This is the login infor for the account Cogito runs over.
account=	"ACCOUNT"
character=	"CHARACTER"
password=	"PASSWORD"

#For channels, make sure you enter their PRECISE title, including any trailing spaces and/or punctuation! 
#channels=	['Development']
channels=	['Channel 1. ', 'Second Channel For the Bot']


host=		'chat.f-list.net'
port=		9722	#9722 - Real | 8722 - Dev
version=	"1.5.3.7"

#misc settings.
banter = False
banterchance = 1.0
min_ratio = 0.75

#Format: Command : (function_name, level required for access, message type required for access.)
#levels: 
	#2: normal user. 
	#1: channel admin/chat admin. 
	#0: admin defined above, in config.py
#message types: 
	#0: private message
	#1: in-channel
	#2: in-channel, mentioning config.character; e.g. Cogito: <function>
functions = {	
					".deop":			("deop", 		0, [0,1]),
					".shutdown":		("hibernation",	0, [0,2]),
					".join":			("join",		0, [0,1]),
					".leave":			("leave",		0, [0,1]),
					".minage":			("minage",		0, [0,1]),
					".op":				("op", 			0, [0,1]),
					
					".act":				("act",			1, [0,1]),
					".ban":				("ban", 		1, [0,1]),
					".black":			("blacklist",	1, [0,1]),
					".kick":			("kick",		1, [0,1]),
					".lj":				("lastJoined",	1, [0,1]),
					".lc":				("listIndices",	1, [0,1]),
					".r":				("rainbowText",	1, [0,1]),
					".say":				("say",			1, [0,1]),
					".white":			("whitelist",	1, [0,1]),
					".ignore":			("ignore",		1, [0,1]),
					
					".help":			("help", 		2, [0,1]),
					".tell":			("tell", 		2, [0,1])
					}
