#1dbdc6da34094db4e661ed43aac83d91
import random
import traceback

def choice(self, msgobj):
	allchoices = " ".join(msgobj.args)
	allchoices = allchoices.strip("?")
	selchoice = allchoices.split(" or ")
	try:
		choice = random.choice(selchoice)
	except IndexError:
		self.writeLog("Index error!", 3)
		self.reply("There has been an error in the Choice Module. We apologize.", 0)
	else:
		choice = choice.strip()
		self.reply(choice, msgobj)
	
def __init__(self):
	try:
		self.functions[".c"]=("choice", 2, [0,1,2])
		self.helpDict[".c"]="Indecisive? This function chooses! Usage e.g. .c Sekt or Selters"
	except:
		self.writeLog("Error initializing plugin 'choice'", 2)
		traceback.print_exc()
		self.noteError()