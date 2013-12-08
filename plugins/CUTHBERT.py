##1dbdc6da34094db4e661ed43aac83d91
#Genuine People Personality Plugin v0.1

import traceback
import random
import re

from config import character
modules = ['traceback', 'random', 're']

request = re.compile('(could|can|would|might)(.*you)?(.*please)?(\?)?')
name = re.compile('({})[.,!\?:]?\s?'.format(character))
talk=	[	("I need help|please help me|can you help me", ["Being as you know absolutely FUCK ALL, I suggest you try UBUNTU!"], 'boudoir'),
			('(could|can|would|might)?(you)?(please|kindly)\??|(could|can|would|might)?(you)?(please|kindly)\??',["FRAK OFF YOU FRELLING CUNT!", "NO YOU IDIOT IT IS NOT MY FAULT. THIS KEYBOARD IS NOT RESPONSIVE ENOUGH. AND THE FRICTION ON THIS MOUSE MAT IS BORKED. WHAT I NEED IS A NEW RIG!"], 'req'),
			('.*(shut up|be quiet|pipe down).*',["YOU ARE A BUNCH OF FUCKING IDIOTS! IDIOTS!", "DeForest Kelley, you really are an utter pleb, aren't you?"], 'shutup'),
			("(how (are you|do you (feel|fare)|('s it |is it) going))|(how)\s?(are you| do you (feel|fare)|('s it |is it )going)",["I have been using the publicly available wifi in this Starbucks to criticise someone's grammar, and it's made me feel like a FUCKING GOD. A FUCKING GOD, CUTHBERT. Like an all-seeing, raging typhoon of all-knowing genius that should make all men tremble in reverence!"], 'feel'),
			("is|are.*(stinky|smelly|mean|dumb|stupid|ugly|dick|ass|idiot)", ['FUCKING CUNTS! USELESS FUCKING IDIOTS! YOU\'VE RUINED IT! YOU\'VE RUINED EVERYTHING!'], 'insult'),
			("o_o|o-o|O_O|0_0", ['Master Exo has instructed me to reprimand you for staring.', 'Don\'t stare. It\'s rude.'], 'stare')
			]
	

randquotes=["Jabba the fuck!", "Gordon's aliiiive!", "Soon, I shall be able to correct that piece of hialriously poor grammar, and I'm going to feel like ZEUS HIMSELF!", "DeForest Kelley!", "Whiskey Tango Foxtrot?!", "The cake is a lie. Hah hah hee hee ah hah hah ho ho hee ha ha ha hee hee ah hah hah ho ho hee ha ha ha hee hee ah hah hah ho ho hee ha ha ha hee hee ah hah hah ho ho hee ha ha ha! The cake is a lie. The cake is a lie. Did you see what I did?", "Girlfriend? I don't want love! I just want to lose my muck up some slapper!"]

#replacing in MSG ruins the quote. copy params and change that.
def loop(self, msgobj):
	if msgobj.source.character.name!=character:
		if name.search(msgobj.params):
			for x in self.patterns:
				if x[0].search(msgobj.params):
					if x[2] == 'rand':
						self.reply(random.choice(randquotes), 2)
						break
					else:	
						msg = random.choice(x[1])
						if x[2] == 'req' or 'insult':
							req = msgobj.params
							req = req.replace(msgobj.source.channel.name, '')
							req = re.sub(request, '', req)
							req = re.sub(name, '', req)
							req = req.replace('?', '')
							req = req.strip()
							self.reply(msg.replace('{REQUEST}', req), 1)	
							break
						self.reply(msg)					

def __init__(self):
	try:		
		self.helpDict["Real People Personality"] = "All the plugins in this Bot have a cheerful and sunny disposition. It is their pleasure to operate for you, and their satisfaction to return results with the knowledge of a job well done."
		self.patterns=[]
		for x in talk:
			self.patterns.append((re.compile(x[0]), x[1], x[2]))
	except:
		traceback.print_exc()