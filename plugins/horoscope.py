##1dbdc6da34094db4e661ed43aac83d91
import traceback
import random
import re
months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
mon_len={1:0, 2:32, 3:60, 4:91, 5:121, 6:152, 7:182, 8:213, 9:243, 10:274, 11:305, 12:335}

"""
jan 31
feb 59
mar 90
apr 120
may 151
jun 181
jul 212
aug 243
sep 273
oct 304
nov 334
dec 365

Capricorn	0-20
Aquarius	21-50
Pisces		51-79
Aries		80-110
Taurus		111-141
Gemini		142-172
Cancer		173-202
Leo			203-234
Virgo		235-266
Libra		267-296
Scorpio		297-326
Sagittarius	327-356
Capricorn	357-365
"""

signs=[(20,'Capricorn'), (50,'Aquarius'), (79,'Pisces'), (110,'Aries'), (141,'Taurus'), (172,'Gemini'), (202,'Cancer'), (234,'Leo'), (266,'Virgo'), (296,'Libra'), (326,'Scorpio'), (356,'Sagittarius'), (366,'Capricorn')]

date = re.compile('(?P<day>\d{1,2})(.|(st|nd|rd|th))?(\s)?(?P<month>(\d{1,2}|\w{3,9}))')

def horoscope(self):
	day, month = date.search(self.params).group('day', 'month')
	day = int(day)
	try:
		month = int(month)
	except ValueError:
		FLAG = False
		for x in months:
			if x == month:
				month = months.index(x)+1
				FLAG = True
		if not FLAG:	
			self.say("Unable to parse '{}' as month. Syntax: .hs DD.MM".format(month), 0)
	day=day+mon_len[month]
	for x in signs:
		if abs(day-x[0])<31:
			sign = x[1]
	
	horoscope = []
	for x in range(2):
		horoscope.append(random.choice(self.horoscopes))
	check = False
	while check==False:
		if horoscope[0]==horoscope[1]:
			horoscope=horoscope[-1:]
			horoscope.append(random.choice(self.horoscopes))
		else: check = True
	horoscope = ' '.join(horoscope)
	horoscope = horoscope.replace('{NAME}', random.choice(self.channels[self.source.channel].users))
	horoscope = horoscope.replace('{SIGN}', sign)
	self.say("[{}]: {}".format(sign, horoscope), 1)
	
def __init__(self):
	try:
		self.horoscopes=self.loadData('horoscopes', list)
		self.cf_list[".hs"]="horoscope" #this maps to the function to be executed on command receiving.
		self.cf_levels['.hs']=2 #0 - creator only, 1 - admin, 2 - public
		self.cf_access_types['.hs']=[0,1,2] #execute if message from 0- direct, 1 - nick in chan, 2 - chan
		self.dict_help[".hs"]="Prints your current horoscope. Usage '.h <DD.MM>, e.g. .h 29.5"
		
	except Exception as error:
		self.writeLog("---Error initializing plugin '.horoscope': {}".format(error), 2)
		traceback.print_exc()