#1dbdc6da34094db4e661ed43aac83d91
#Genuine People Personality Plugin v0.1.2

import traceback
import random
import re

from config import character
modules = ['traceback', 'random', 're']

request = re.compile('(could|can|would|might)(.*you)?(.*please)?(\?)?')
name = re.compile('({})[.,!\?:]?\s?'.format(character))
talk=	[	("I need help|please help me|can you help me", ['No problem. I''ll just need a little...[b]favour[/b] in return.', "Oh, I know lots of things. [i]Lots[/i] of things..."], 'boudoir'),
			("is|are.*(stinky|smelly|mean|dumb|stupid|ugly|dick|ass|idiot)", ['It''s funny how dumb you are', 'And I take it you''re some kind of living ventriloquist dummy? I''m just kidding, I know who you are, {NAME}', 'I gotta hand it to you kids. You''re a lot more clever than I gave you credit for. Especially the fat one.'], 'insult'),
			("o_o|o-o|O_O|0_0", ['Eat NIGHTMARES.'], 'stare')
			
			
			]
	

randquotes=["Boy, these arms are durable!", "Hey, want to hear my impression of you in about 3 seconds? [i]Ahhhhhhhhhhhhhh![/i]", "Remember, reality is an illusion, the universe is a hologram, buy gold!", "It's funny how dumb you are!", "Here! Deer teeth. For you, kid!"]

#replacing in MSG ruins the quote. copy params and change that.
def loop(self, msgobj):
	if msgobj.source.character.name!=character:
		if name.search(msgobj.params):
			for x in self.patterns:
				if x[0].search(msgobj.params):
					if x[2] == 'rand':
						self.reply(random.choice(randquotes), msgobj, 2)
						break
					else:	
						msg = random.choice(x[1])
						if x[2] == 'req' or 'insult':
							req = msgobj.params
							req = req.replace(msgobj.source.channel.name, '')
							req = re.sub(request, '', req)
							req = re.sub(name, '', req)
							req = req.replace('/me', '')
							req = req.replace('?', '')
							req = req.replace(' me ', ' you ')
							req = req.replace('{NAME}', msgobj.source.character.name)
							req = req.strip()
							req.capitalize()
							self.reply(msg.replace('{REQUEST}', req), msgobj, 1)	
							break
						self.reply(msg, msgobj)					

def __init__(self):
	try:		
		self.helpDict["Bill Cypher"] = "A darkness approaches. A day will come in the future where everything you care about will change... Until then I'll be watching you! I'll be watching you..."
		self.patterns=[]
		for x in talk:
			self.patterns.append((re.compile(x[0]), x[1], x[2]))
	except:
		traceback.print_exc()