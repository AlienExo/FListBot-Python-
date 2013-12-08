##1dbdc6da34094db4e661ed43aac83d91
from datetime import datetime
import traceback

def countdown(self):
	try:
		if self.args[0]=="-a":
			for x in self.cds:
				self.say("{} - {}".format(x, deltacalc(cds[x])))
			return
		else:
			date, time = self.args[0], self.args[1]
			descr = self.args[2:].join(' ')
			dt = date +" "+ time
			dt = datetime.datetime.strptime(dt, "%d.%m.%Y %H:%M")
			print(dt)
			delta = datetime.datetime.now()-dt
			self.say("Event '{}' will occur in {}.".format(descr, self._timecalc(delta)), 2)
	except IndexError:
		for x in self.cds.keys()[:5]:
			self.say("Event '{}' in {}".format(x, self._timecalc(self.cds[x])), 2)
			
def __init__(self):
	try:
		self.functions[".cd"]=("countdown", 1, [0,1,2])
		self.helpDict[".cd"]="Shows the time left until an event. Usage: .cd (lists the next five), .cd -a (lists all), .cd dd.mm.yyyy hh:mm (new countdown)"
		self.cds=self._loaddata('countdowns')
		print self.cds
	except:
		self.writeLog("Error initializing plugin 'countdown'", 2)
		self.noteError()

def loop(self):
	for x in self.cds:
		points = self._timecalc(self.cds[x]).split()
		print points
		
def exit(self):
	self._savedata(self.cds, 'countdowns')