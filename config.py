# admins defines who can issue admin-level commands to the bot. Looks like this:
# admins = ["First Admin", "second admin", "xXx third admin-dono xXX"]
#please be precise, else python pukes up an error. TIA. 
admins = 	["Exo", "Kalikrates"]

#This is the login infor for the account Cogito runs over.
account=	"Cogito"
character=	"Cogito"
password=	"1ChD3Nk34Ls=!"

#For channels, make sure you enter their PRECISE title, including any trailing spaces and/or punctuation! 
#channels=	['Development']
channels=	['Gay/Bi Male Human(oid)s. ', 'Coaches, Sweat and Muscles', 'Manly Males of Extra Manly Manliness', 'The Felines Lair~!']

host=		'chat.f-list.net'
port=		9722	#9722 - Real | 8722 - Dev
version=	"2.1"

banter = True
banterchance = 1.0
messagelimit = 7
minSendDelay = 1.0

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
			".shutdown":	("hibernation",	0, [0]),
			".join":		("join",		0, [0,1]),
			".leave":		("leave",		0, [0,1]),
			".lockdown":	("lockdown",	0, [0,1,2]),
			".minage":		("minage",		0, [0,1]),
			".scan":		("scan",		0, [1]),
					
			".act":			("act",			1, [0,1]),
			".noAge":		("alertNoAge",	1, [0,1]),
			".underAge":	("alertUnderAge",	1, [0,1]),
			".ban":			("ban", 		1, [0,1]),
			".black":		("blacklist",	1, [0,1]),
			".deop":		("deop", 		1, [0,1]),
			".kick":		("kick",		1, [0,1]),
			".lj":			("lastJoined",	1, [0,1]),
			".op":			("op", 			1, [0,1]),
			".r":			("rainbowText",	1, [0,1]),
			".say":			("say",			1, [0,1]),
			".white":		("whitelist",	1, [0,1]),
			".ignore":		("ignore",		1, [1]),
					
			".auth":		("auth",		2, [0]),
			".bingo":		("bingo", 		2, [0,1]),
			".lc":			("listIndices",	2, [0]),
			".help":		("help", 		2, [0,1]),
			".tell":		("tell", 		2, [0,1])}
			
masterkey = "425133f6b2a9a881d9dc67f5db17179e"