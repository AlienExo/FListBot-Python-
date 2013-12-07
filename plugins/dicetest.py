##1dbdc6da34094db4e661ed43aac83d91

modules = ['traceback', 'random']
#import traceback
#import random

def diceroll():
	try:
		b = "1d20+5".lower().split("d")
		c = b[1].split("+")
		dcmode = False
			
		try:
			b[0] = int(b[0])
			c[0] = int(c[0])
			c[1] = int(c[1])
		except IndexError:
			c=[c[0], 0]
		except ValueError:
			print("Invalid input. (Not a number?)", 0)
		if not (b[0]>15) or (c[0]>100) or (c[1]>25):
			results = []
			for x in range(b[0]):
				results.append(random.choice(range(1, c[0]+1))+c[1])
			if not dcmode:
				print("{} rolled {}d{}+{} => {}, total {}".format(source, b[0], c[0], c[1], results, sum(results)), 2)
			else:
				dclist = []
				for x in results:
					if x > DC:
						dclist.append("Success")
					else:
						dclist.append("Failure")
				print("Rolling {}d{}+{}, DC {} => {!s}".format(b[0], c[0], c[1], DC, dclist), 2)
		else:
			print("Out of range - only support up to 15d100+25")
	except Exception as error:
		print("Error in module diceroll: {}".format(error), 3)
		print("There has been an error during diceroll execution. We apologize.")
		traceback.print_exc()

def __init__(self):
	pass
	