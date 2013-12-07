import json
from urllib import urlencode
import urllib2

account=	"ACCOUNT"
character=	"CHARACTER"
password=	"PASSWORD"

banter = True
banterchance = 1.0
minage = 13

channels=	['CHANNEL 1']
#channels=	['Development']
# admins defines who can issue admin-level commands to the bot. Looks like this:
# admins = ["first name", "secondname", "THirdNAme"]
#please be precise, else python pukes up an error. TIA. 
admins = 	["ADMINS"]

host=		'chat.f-list.net'
port=		9722	#9722 - Real | 8722 - Dev
version=	"1.0.1.5"

flood_pause = 0.75
min_ratio = 0.75
bashlim = 	15

ignore_commands = ['FLN', 'STA', 'NLN', 'PIN', 'MSG', 'PRI', 'TPN', 'LIS', 'ORS', 'IDN', 'VAR', 'CDS', 'COL', 'ICH', 'JCH', 'LCH']


#Format: Command : function. Is called for getattr().
cf_list = {	
					"EXEC_HIBERNATION":"hibernation",
					".help":"help",
					".tell":"tell",
					".op":"op",
					".deop":"deop",
					".k":"kick",
					".b":"ban",
					".white":"whitelist",
					".black":"blacklist",
					".lj":"lastJoined",
					".r":"rainbow",
					".s":"say",
					".a":"act",
					".kick":"kick",
					".ban":"ban",
					".leave":"leave",
					".join":"join"
					}
					
#lvl 1 - need admin nick | lvl 2 - free access.
cf_levels = {		'EXEC_HIBERNATION'				:1,
					'.help'							:2,
					'.tell'							:2,
					'.op'							:1,
					'.deop'							:1,
					'.k'							:1,
					'.b'							:1,
					'.black'						:1,
					'.white'						:1,
					'.lj'							:1,
					'.r'							:1,
					'.s'							:1,
					'.a'							:1,
					'.join'							:1,
					'.leave'						:1,
					'.kick'							:1,
					'.ban'							:1
					}	
					
#lvl 0 - direct message only | lvl 1 - channel and nick | lvl 2 - channel
cf_access_types = 	{
					'EXEC_HIBERNATION'				:[0,1],
					'.help'							:[0,1],
					'.tell'							:[0,1],
					'.op'							:[0,1],
					'.deop'							:[0,1],
					'.k'							:[0,1],
					'.b'							:[0,1],
					'.black'						:[0,1],
					'.white'						:[0,1],
					'.lj'							:[0],
					'.r'							:[0,1],
					'.s'							:[0,1],
					'.a'							:[0,1],
					'.join'							:[0,1],
					'.leave'						:[0,1],
					'.kick'							:[0,1],
					'.ban'							:[0,1]
					}			

