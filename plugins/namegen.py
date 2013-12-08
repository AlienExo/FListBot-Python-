##1dbdc6da34094db4e661ed43aac83d91
#!/usr/bin/python
import random
import traceback
import yaml
from collections import defaultdict	



def NameGen (n_ngrams, n_names):
	"Generates n_names names of length Length"
	voc = ('a', 'e', 'i', 'o', 'u')
	con = ('b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z')
	spe = ('st', 'rb', 'ck', 'sch', '\'')
	
	ngrams = (
		(voc, con),
		(voc, spe),
		(con, voc),
		(con, voc),
		(voc, voc, con),
		(spe, voc),
		(spe, con)
		)
	ngram_lookup = defaultdict(list)
	for ngram in ngrams:
		ngram_lookup[ngram[0]].append(ngram[1:])
	
	namelist=[]
	for __ in range(n_names):
		result = [random.choice((voc, con))]
		for _ in range(n_ngrams-1):
			ngrams = ngram_lookup[result[-1]]
			result.extend(random.choice(ngrams))
				
		name = ''.join(random.choice(l) for l in result)
		name = name.capitalize()
		namelist.append(name)
	return namelist

def namegen(self):
	if self.args[0]=="-r":
		self.args=self.args[1:]
		names=[]
		try: a = int(self.args[0])
		except ValueError: a=1
		for x in range(a):
			names.append(' '.join((random.choice(self.firstnames), random.choice(self.lastnames))))
		self.say(', '.join(names), 0)
	else:
		try:
			n_ngrams = int(self.args[0])
			n_names = int(self.args[1])
			if n_ngrams>10 or n_names>10:
				self.say("Name generation for parameters over 10 is locked out.", 0)
				return
				
			if n_ngrams < 3:
				self.say("Names shorter than three are not supported.", 0)
				return
		except ValueError:
			self.say("Syntax error - {} and {} not recognized as numbers".format(self.args[0], self.args[1]), 0)
			return
		
		try:
			names = NameGen(n_ngrams, n_names)
			for x in names:
				x = x.capitalize()
			names = ", ".join(names).rstrip(',')
			self.say(str(names), 0)
			
		except Exception as error:
			self.writeLog ("Error in Namegen: {}".format(error), 1)
			traceback.print_exc()
		
def __init__(self):
	try:
		with open('./data/names.yml', 'r') as inp:
			self.lastnames, self.firstnames = yaml.load_all(inp)
		self.functions['.n']=("namegen", 2, [0,1,2])
		self.helpDict['.n']="Generates X names of Y length. Usage: .n <x> <y>  Alternative: .n -r <x> returns <x> real names (mixed genders)."
	except Exception as error:
		self.writeLog("Error initializing plugin 'namegen': {}".format(error), 2)
		self.noteError()