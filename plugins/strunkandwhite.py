##1dbdc6da34094db4e661ed43aac83d91
import random
import traceback

strunkandwhite="""""".split()

def strunk(self, msg):
	if len(msg.params)>0:
		
	else:
		self.reply(random.choice(strunkandwhite), msg, 2)
	
def __init__(self):
	try:
		self.functions[".strunk"]=("strunk", 2, [1])
		self.helpDict[".strunk"]="Displayes a random quote from Strunk and White's 'The Elements of Style'. Ues it well."
	except:
		self.writeLog("Error initializing plugin 'Strunk and White'", 2)
		self.noteError()
