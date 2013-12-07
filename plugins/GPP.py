##1dbdc6da34094db4e661ed43aac83d91
#Genuine People Personality Plugin v0.1

import traceback
import random
import re

from config import character
modules = ['traceback', 'random', 're']

request = re.compile('(could|can|would|might)(.*you)?(.*please)?(\?)?')
name = re.compile('({})[.,!\?:]?\s?'.format(character))
talk=	[	("((how's |how is ).*life.*\?)",["Life? Don't talk to me about life."], 'life'),
			("I need help|please help me|can you help me", ['Please state the nature of your boudoir emergency.', "I am programmed in multiple techniques."], 'boudoir'),
			("open the pod bay doors", ["I'm afraid I can't do that, Dave."], 'podbay'),
			('(could|can|would|might)?(you)?(please)\??|(could|can|would|might)?(you)?(please)\??',["Here I am, brain the size of a planet, and they ask me to '{REQUEST}'. Call that job satisfaction? 'cos I don't.", "I would like to say that it is a very great pleasure, honour and privilege for me to '{REQUEST}', but I can't because my lying circuits are all out of commission.", "'{REQUEST}'... I won't enjoy it.", "That depends on whether or not I can find my frilly apron. With my luck, I probably can.", "'{REQUEST}'. You're really asking me to {REQUEST}?", "{REQUEST}. Of -course-, right away. With pleasure. [Sarcasm Self-Test Complete]"], 'req'),
			('.*(shut up|be quiet|pipe down).*',["Pardon me for breathing, which I never do anyway so I don't know why I bother to say it, oh God, I'm so depressed."], 'shutup'),
			("(how (are you|do you (feel|fare)|('s it |is it) going))|(how)\s?(are you| do you (feel|fare)|('s it |is it )going)",["I got very bored and depressed, so I went and plugged myself into the internet. I talked to it at great length and explained my view of the universe to it. It commited suicide.", "I think you ought to know I'm feeling very depressed.", "I didn't ask to be made, no one consulted me or considered my feelings in the matter."], 'feel'),
			("is|are.*(stinky|smelly|mean|dumb|stupid|ugly|dick|ass|idiot)", [':\'(', 'What did I ever do to you?', 'I\'m rubber, you\'re glue.', 'No, YOU\'RE {REQUEST}'], 'insult'),
			("o_o|o-o|O_O|0_0", ['Master Exo has instructed me to reprimand you for staring.', 'Don\'t stare. It\'s rude.'], 'stare')
			]
	

randquotes=["...and then of course I've got this terrible pain in all the subroutines down my left hand side...", "I'm not getting you down at all, am I?", "I'd make a suggestion, but you wouldn't listen. No one ever does.", "This will all end in tears.", "I've calculated your chance of survival, but I don't think you'll like it."]

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