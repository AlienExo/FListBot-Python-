#1dbdc6da34094db4e661ed43aac83d91
from random import choice
import traceback

phrases = """It is certain.
It is decidedly so.
Without a doubt.
Yes - definitely.
You may rely on it.
As I see it, yes.
Most likely.
Outlook good.
Signs point to yes.
Yes.
Reply hazy, try again.
Ask again later.
Better not tell you now.
Cannot predict now.
Concentrate and ask again.
Don't count on it.
My reply is no.
My sources say no.
Outlook not so good.
Very doubtful.""".split('\n')

def eightball(self, msgobj):
	self.reply(choice(phrases))
	
def __init__(self):
	try:
		self.functions['.e']= ("eightball", 2, [0,1,2])
		self.helpDict['.e']="Ask the allmighty eightball. Marvel at its wise words. What could it meeeeeean? Usage: .e Question"
	except:
		print("Error initializing plugin 'eightball'")
		traceback.print_exc()