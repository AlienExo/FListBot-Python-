import personality
import FListAPI
import random
import utils

lines = utils.loadData('EDI', dict, './personalities/EDI/')

def __init__():
	print("\tEDI initialized. ")
	
def JCH(msgobj):
	if msgobj.source.character.name=="Jalon Renk":

	msgobj.reply("Space Husband Unit 'Jalon Renk' recognized. Welcome.")
			
		
def test():
	print("\tEDI.py successfully called test()")

def handle(FListProtocol, msg):
	if random.random()<0.1: FListProtocol.reply("I always work at optimal capacity.", msg)
	try:
		func = getattr(Functions, msg.cmd)
		if callable(func): func(FList, msg)	
	except AttributeError: pass
	
def telling(FListProtocol, char, chan):
	messages = FListProtocol._telling(char)
	lm = len(messages)
	FListProtocol.reply("Commander {}, you have {} new message{} at your private terminal.".format(char, lm, "s"*(lm>1)))
	for message in messages:
		FListProtocol.reply("<{}> {} ({})".format(message[0], message[1], message[2]))
		