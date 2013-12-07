##1dbdc6da34094db4e661ed43aac83d91
import traceback
import random
deck= 	{	"[The Fool]":(			"The infinite lies within the simple, just as the simple lies within the infinite.", "The Fool is the spirit in search of experience. He represents the mystical cleverness bereft of reason within us, the childlike ability to tune into the inner workings of the world. ", "protagonist of a story - path through life - journey - Joker's Wild"), 
			"[The Magician]":( 		"Attaining one's dream requires a stern will and unfailing determination.", "Points to the talents, capabilities and resources at the querent's disposal. ", "Action - Consciousness - Concentration - Personal power"), 
			"[The High Priestess]":("The silent voice within one's heart whispers the most profound wisdom.", "Shows when a secret is kept or revealed, when you are holding on to the truth or revealing it, the card associated with mystery, when powerful feminine influences and support currently in force for the querant.", "Knowingness - Love - Wisdom - Sound judgment - Serenity "), 
			"[The Empress]":( 		"Celebrate life's grandeur - its brilliance - its magnificence...", "The Empress is mother, a creator and nurturer. She can represent the creation of life, of romance, of art or business.", "Mothering - Fertility - Sexuality - Abundance"), 
			"[The Emperor]":( 		"Only courage in the face of doubt can lead one to the answer.", "The Emperor symbolizes the desire to rule over one's surroundings, and its appearance in a reading often suggests that the subject needs to accept that some things may not be controllable, and others may not benefit from being controlled.", "Fathering - Stability - Authority - Power"), 
			"[The Hierophant]":( 	"It is indeed a precious gift to understand the forces that guide oneself.", "It represents the first level of understanding. When it appears in a tarot spread, it is a warning to the Querant to reexamine his or her understanding of the meaning of things; of the structure of the world; of the powers that be. Watch out for hypocrisy.", "Education - Knowledge - Status quo - Institution"), 
			"[The Lovers]":( 		"There is both joy and wonder in coming to understand another.", "In some traditions, the Lovers represent relationships and choices. Its appearance in a spread indicates some decision about an existing relationship, a temptation of the heart, or a choice of potential partners.", "Affinity - Bonding - Romance - Heart"), 
			"[The Chariot]":( 		"One of life's greatest blessings is the freedom to pursue one's goals.", "Control is required over opposing emotions, wants, needs, people, or circumstances; to bring them together and give them a single direction, your direction. Confidence is also needed and, most especially, motivation.", "Egocentrism - Self-confidence - Conviction - Anxiety"), 
			"[Justice]":( 			"To find the one true path, one must seek guidance amidst uncertainty.", "When Justice appears, it usually signals that some injustice needs righting, that something in the world is dangerously out of balance. This could be interior, or some external wrong.", "Decision - Intellect - Analysis - Realism - Severity"), 
			"[The Hermit]":( 		"It requires great courage to look at oneself honestly, and forge one's own path.", "There are two possible ways this card can be interpreted: First, the need to withdraw from society to become comfortable with oneself. Second, the return from isolation to share his knowledge with others.", "Introspection - Silence - Guidance - Reflection"), 
			"[Fortune]":( 			"Alongside time exists fate, the bearer of cruelty.", "An element of change in the querant's life, such change being in station, position or fortune", "Sudden Events - Speed - New Developments - Life Cycles"), 
			"[Strength]":( 			"Only with strength can one endure suffering and torment.", "The modern interpretation of the card stresses discipline and control. The lion represents the primal or id-like part of the mind, and the woman, the 'higher' or more elevated parts of the mind. The card tells the Querent to be wary of base emotions and impulse. For example, in The Chariot card, the Querant is fighting a battle. The difference is that in Strength, the battle is mainly internal rather than external.", "Self-control - Being solid - Patience - Compassion"), 
			"[The Hanged Man]":( 	"In the face of disaster lies opportunity for renewal.", "A great awakening that is possible, and will know that after the sacred Mystery of Death there is a glorious Mystery of Resurrection.", "Sacrifice - Letting go - Surrendering - Passivity"), 
			"[Death]":( 			"It matters not who you are - Death awaits you.", "It is unlikely that this card actually represents a physical death. Typically it implies an end, possibly of a relationship or interest, and therefore implies an increased sense of self-awareness-not to be confused with self-consciousness or any kind of self-diminishment.", "Finishing up--Regeneration--Elimination of old patterns"), 
			"[Temperance]":( 		"Only through balancing freedom with reason can one find harmony.", "In addition to its literal meaning of temperance or moderation, the Temperance card is often interpreted as symbolizing the blending or synthesis of opposites.", "Equilibrium - Transcendence - Unification -- Healing"), 
			"[The Devil]":( 		"Throw off your false restraints and face what you have locked away.", "The Devil is the card of self-bondage to an idea or belief which is preventing a person from growing or being healthy. On the other hand, however, it can also be a warning to someone who is too restrained and/or dispassionate, which is yet another form of enslavement.", "Materialism - Ignorance - Stagnation - Self-bondage"), 
			"[The Tower]":( 		"In the face of overwhelming force, you must change or be changed.", "To some, it symbolizes failure, ruin and catastrophe. To others, the Tower represents the paradigms constructed by the ego, the sum total of all schema that the mind constructs to understand the universe. The Tower is struck by lightning when reality does not conform to expectation.", "Crisis - Revelation - Disruption - Realizing the truth "), 
			"[The Star]":( 			"A glimmer of hope is an inspiration to those in despair.", " Usually divined as hope for the future, it may indicate good things to come in the things represented by cards that may be close to the star in a reading layout.", "Good will - Optimism - Harmony - Renewal of forces"), 
			"[The Moon]":( 			"Though falsehoods and uncertainties cloud one's sight, you must search for the truth.", "The Moon can be interpreted with the feeling of uncertainty, where the past still haunts, unsure of a journey but still going ahead with it, feeling watched and because it is commonly associated with dreams, fantasies and mysteries this card can also be interpreted with surreal feelings and situations in your waking life.", "Lack of clarity - Tension - Doubt - Fantasy"), 
			"[The Sun]":( 			"Find inspiration and satisfaction in what you have seen and hope for the future.", "This card is generally considered positive. It is said to reflect happiness and contentment, vitality, self-confidence and success. Sometimes referred to as the best card in Tarot, it represents good things and positive outcomes to current struggles.", "Assurance - Energy - Personal power - Happiness"), 
			"[Judgement]":( 		"Having chosen both good and evil on your road, now face judgement.", "When Judgment appears in a reading, it is usually interpreted as a signal of an impending judgment, such as of postponed decisions. As the card symbolizes resurrection, it can also be interpreted to herald the return of individuals from the past.", "Judgment - Rebirth - Inner Calling - Absolution"), 
			"[The World]":(			"Reach what you truly desire. Find balance within and without.", "The World represents an ending to a cycle of life, a pause in life before the next big cycle beginning with the fool. It tells us full happiness is also to give back to the world, sharing what we have learned or gained.", "Fulfillment - Accomplishment - Success - Integration")
		}
		
spreads={	0:(1, "Single Card", ['your question as a whole']),
			1:(10, "Celtic Cross", ['the significator', 'the conditions surrounding the question or an obstacle, an aspect of the question you have not yet considered', 'what you hope for in relation to the question being asked', 'what you have already experienced in relation to the whole spread', 'what was in the past', 'the influence that will come in the future', 'the attitude of the question being asked', 'how family or friends will influence the question', 'the hopes and fears in relation to the question', 'the end result of all of the previous nine cards']),
			2:(5, "Star", ['what you see', 'what you can\'t see', 'what you can change', 'what you cannot change', 'what you can expect']),
			3:(3, "Three-way", ['the past','the present','the future']),
			4:(5, "Love", ['the past', 'the present', 'the future', 'the other person', 'obstacles or positives'])
		}

def tarot(self):
	try:
	
		if self.args[0]=="-q":
			self.say("{}".format(deck[random.choice(deck.keys())][0]), 2)
			return
		
		cards=[]
		spread = spreads[int(self.args[0])]
		while len(cards)<spread[0]:
			card = random.choice(deck.keys())
			if not card in cards: cards.append(card)
		if spread[0]==1: 
			self.say("{} - {}".format(card, deck[card][0]), 2)
			return
		
		a = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eight', 'ninth', 'tenth']
		c = 0
		
		self.say("Your have requested the {} spread, containing {} card(s).".format(spread[1], spread[0]), 2)
		while c < len(cards):
			self.say("The {} card, indicating {}, is {}.".format(a[c], spread[2][c], cards[c]), 2)
			c+=1	
		self.say("For further information about any card, type '.t -e [Card Title]', e.g. '.t -e The Fool'.", 0)
		
	except IndexError:
		self.say("Arguments specified incorrectly. Usage: '.t {}-{} <spread>', or '.t -e <explanation> [Card Title]'; e.g. '.t 0' or '.t -e The Fool'.".format(range(len(spreads))[0], range(len(spreads))[-1]), 0)
		traceback.print_exc()
	
	except ValueError:
		if self.args[0]=="-e":
			try:
				print self.params
				card = deck["[{}]".format(" ".join(self.args[1:]))]
				self.say("{}: {} [{}]".format(self.args[1], card[1], card[2]))
			except ValueError:
				self.say("Error: No card named '{}'.".format(self.args[1]), 0)
	
	except KeyError:
		self.say("{} is not a valid number for a spread. Spreads range from {} to {}".format(self.args[0], range(len(spreads))[0], range(len(spreads))[-1]), 0)
		traceback.print_exc()

def __init__(self):
	try:
		self.cf_list[".t"]="tarot"
		self.cf_levels['.t']=2
		self.cf_access_types['.t']=[0,1,2]
		self.dict_help[".t"]="A random card reading. Usage: '.t <spread number>'. Spreads range from {} to {}. For detail on a card, '.t -e <card name>'".format(range(len(spreads))[0], range(len(spreads))[-1])
	except Exception as error:
		self.writeLog("Error initializing plugin 'Tarot': {}".format(error), 2)
		self.noteError()