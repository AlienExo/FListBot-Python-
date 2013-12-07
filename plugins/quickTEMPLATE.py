#deleteme
#1dbdc6da34094db4e661ed43aac83d91
modules = ['traceback']
#import traceback

def FUNCTION(self):
	pass
	
def loop(self):
	pass

def __init__(self):
	try:
		self.cf_list["COMMAND"]="FUNCTION"
		self.cf_levels['COMMAND']=2
		self.cf_access_types['COMMAND']=[0,1,2]
		self.dict_help["COMMAND"]="Help Entry For Command"
	except:
		self.writeLog("Error initializing plugin 'PLUGINNAME'", 2)
		self.noteError()
		
def exit(self):
	pass