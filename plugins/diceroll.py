#1dbdc6da34094db4e661ed43aac83d91
import traceback
import random

def diceroll(datapipe, self):
	try:
		source = self.source.character
		b = self.args[0].lower().split("d")
		c = b[1].split("+")
		if self.params.lower().find("dc")!=-1:
			dcmode = True
			try:
				DC = int(self.args[2])
			except:
				self.reply("Cannot roll to DC '{}'. Syntax: '.d <>d<>+<> DC <>'".format(a), 0)
				return
		else:
			dcmode = False
			
		try:
			b[0] = int(b[0])
			c[0] = int(c[0])
			c[1] = int(c[1])
		except IndexError:
			c=[c[0], 0]
		except ValueError:
			self.reply("Invalid input. (Not a number?)", 0)
		if not (b[0]>15) or (c[0]>100) or (c[1]>25):
			results = []
			for x in range(b[0]):
				results.append(random.choice(range(1, c[0]+1))+c[1])
			if not dcmode:
				self.say("{} rolled {}d{}+{} => {}, total {}".format(source, b[0], c[0], c[1], results, sum(results)), 2)
			else:
				dclist = []
				for x in results:
					if x > DC:
						dclist.append("Success")
					else:
						dclist.append("Failure")
				self.reply("Rolling {}d{}+{}, DC {} => {!s}".format(b[0], c[0], c[1], DC, dclist))
		else:
			self.reply("Out of range - only support up to 15d100+25")
	except Exception as error:
		self.writeLog("Error in module diceroll: {}".format(error), 3)
		self.reply("There has been an error during diceroll execution. We apologize.", self.access_type)
		traceback.print_exc()

def __init__(self):
	try:
		self.functions['.d']=("diceroll", 2, [0,1,2])
		self.helpDict[".d"]="Rolls a die. Usage .r <a>d<b>(+<c>) (DC d), e.g. .r 3d6+5 DC 4"
	except:
		self.writeLog("Error initializing plugin 'diceroll'", 2)
		self.noteError()
		traceback.print_exc()