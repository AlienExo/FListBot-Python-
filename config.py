import json
from urllib import urlencode
import urllib2

account=	"Cogito"
character=	"Cogito"
password=	"1ChD3Nk34Ls=!"

banter = True
banterchance = 1.0
minage = 13

channels=	['Gay/Bi Male Human(oid)s. ', 'Manly Males of Extra Manly Manliness']
#channels=	['Development']
# admins defines who can issue admin-level commands to the bot. Looks like this:
# admins = ["First Admin", "second admin", "xXx third admin-dono xXX"]
#please be precise, else python pukes up an error. TIA. 
admins = 	["Exo", "Kalikrates"]

host=		'chat.f-list.net'
port=		9722	#9722 - Real | 8722 - Dev
version=	"1.0.1.5"

flood_pause = 0.75
min_ratio = 0.75
bashlim = 	15

ignore_commands = ['FLN', 'STA', 'NLN', 'PIN', 'MSG', 'PRI', 'TPN', 'LIS', 'ORS', 'IDN', 'VAR', 'CDS', 'COL', 'ICH', 'JCH', 'LCH']


#Format: Command : (function_name, level required for access, message type required for access.)
#levels: 
	#2 - normal user. 
	#1 - channel admin/chat admin. 
	#0 - admin defined above, in config.py
#message types: 
	#0: private message
	#1: in-channel
	#2: in-channel, mentioning config.character; e.g. Cogito: <function>
functions = {	
					"EXEC_HIBERNATION":	("hibernation",	1, [0,1]),
					".help":			("help", 		2, [0,1]),
					".tell":			("tell", 		2, [0,1]),
					".op":				("op", 			1, [0,1]),
					".deop":			("deop", 		1, [0,1]),
					".k":				("kick", 		1, [0,1]),
					".b":				("ban", 		1, [0,1]),
					".white":			("whitelist",	1, [0,1]),
					".black":			("blacklist",	1, [0,1]),
					".lj":				("lastJoined",	1, [0,1]),
					".r":				("rainbowText",	1, [0,1]),
					".s":				("say",			1, [0,1]),
					".a":				("act",			1, [0,1]),
					".kick":			("kick",		1, [0,1]),
					".ban":				("ban",			1, [0,1]),
					".leave":			("leave",		1, [0,1]),
					".join":			("join",		1, [0,1]),
					".minage":			("minage",		1, [0,1])
					}