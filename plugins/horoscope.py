#1dbdc6da34094db4e661ed43aac83d91
import traceback
import random
import re
months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
elements=["Hydrogen", "Helium", "Lithium", "Beryllium", "Boron", "Carbon", "Nitrogen",  "Oxygen",  "Fluorine",  "Neon",  "Sodium",  "Magnesium",  "Aluminum",  "Silicon",  "Phosphorus",  "Sulfur",  "Chlorine",  "Argon",  "Potassium",  "Calcium",  "Scandium",  "Titanium",  "Vanadium",  "Chromium",  "Manganese",  "Iron",  "Cobalt",  "Nickel",  "Copper",  "Zinc",  "Gallium",  "Germanium",  "Arsenic",  "Selenium",  "Bromine",  "Krypton",  "Rubidium",  "Strontium",  "Yttrium",  "Zirconium",  "Niobium",  "Molybdenum",  "Technetium",  "Ruthenium",  "Rhodium",  "Palladium",  "Silver",  "Cadmium",  "Indium",  "Tin",  "Antimony",  "Tellurium",  "Iodine",  "Xenon",  "Cesium",  "Barium",  "Hafnium",  "Tantalum",  "Tungsten",  "Rhenium",  "Osmium",  "Iridium",  "Platinum",  "Gold",  "Mercury",  "Thallium",  "Lead",  "Bismuth",  "Polonium",  "Astatine", "Radon", "Francium", "Radium", "Unnilquadium", "Unnilpentium", "Unnilhexium", "Unnilseptium", "Unniloctium", "Unnilennium", "Ununnilium", "Unununium", "Ununbium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium", "Promethium", "Samarium", "Europium", "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium", "Actinium", "Thorium", "Protactinium", "Uranium", "Neptunium", "Plutonium", "Americium", "Curium", "Berkelium", "Californium", "Einsteinium", "Fermium", "Mendelevium", "Nobelium", "Lawrencium"]
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

date = re.compile('(?P<day>\d{1,2})(\s)*(/|.|(st|nd|rd|th))?(\s)*(?P<month>(\d{1,2}|\w{3,9}))')

def horoscope(self, msgobj):
	day, month = date.search(msgobj.params).group('day', 'month')
	day = int(day)
	try:
		month = int(month)
	except ValueError:
		month = month.capitalize()
		FLAG = False
		for x in months:
			if x == month:
				month = months.index(x)+1
				FLAG = True
		if not FLAG:	
			self.reply("Unable to parse '{}' as month. Syntax: .hs DD.MM".format(month), 0)
	if month>12:
		sday = day
		day = month
		month = sday
	day=day+mon_len[month]
	for x in signs:
		if abs(day-x[0])<31:
			sign = x[1]
	print sign
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
	horoscope = horoscope.replace('{NAME}', random.choice(msgobj.source.channel.users))
	horoscope = horoscope.replace('{DAY}', random.choice(days))
	horoscope = horoscope.replace('{ELEMENT}', random.choice(elements))
	horoscope = horoscope.replace('{SIGN}', sign)
	rsign = sign
	while rsign == sign:
		rsign = random.choice(signs)[1]
	horoscope = horoscope.replace('{RSIGN}', rsign)
	

	self.reply("[{}]: {}".format(sign, horoscope), 1)
	
def __init__(self):
	try:
		self.horoscopes=self.loadData('horoscopes', list)
		self.functions[".hs"]=("horoscope", 2, [1])
		self.helpDict[".hs"]="Prints your current horoscope. Usage '.h <DD.MM>, e.g. .h 29.5"
		
	except Exception as error:
		self.writeLog("---Error initializing plugin '.horoscope': {}".format(error))
		traceback.print_exc()