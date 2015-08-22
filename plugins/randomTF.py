##1dbdc6da34094db4e661ed43aac83d91
import traceback


def randomTransformation(self, msg):
	self.reply("HELLO WORLD", msg, 2)
	
def __init__(self):
	try:
		self.functions[".tf"]=("randomTransformation", 2, [0,1,2])
		self.helpDict[".tf"]="Suggests a random transformation to you"
	except:
		self.writeLog("Error initializing plugin 'Random TF'", 2)
		self.noteError()
		
def exit(self):
	pass