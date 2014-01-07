from difflib import SequenceMatcher as matcher

class Song():
	def __init__(self, singer, song):
		self.singer			= singer
		self.song 			= song
		self.level 			= 0		
		lines 				= dict_songs[song]
		self.songiterator 	= iter(lines)
		self.maxLevel 		= len(lines)
		self.func 		= functions[song]
		
		
functions = {'EXEC_HIBERNATION':"hibernation", 'METHOD_METAFALICA':"_method_metafalica", 'EXEC_LINKER':"_op"}
		
dict_songs =	{
				'EXEC_HIBERNATION':["Was yea ra enne ar ciel", 
									"Rrha num ra sleipir etealune na near na morto ciel"],
									
				'EXEC_CHRONICLE=KEY':[	"Was au ga whai pauwel gaunji yasra whou na cenjue sor tou zuieg", 
										"Was ki ra, grandi en eterne slepir, presia aterra cremia sos viuy lonfa, yehar lamenza der soare mea"],
										
				'EXEC_DESPEDIA':[	"Rrha yea ra haf yor, forgandal knawa Manac yor, Manac"],
									
									
				'EXEC_LINKER':[	"Was yea ra frreie yor wart en chs manaf an yor synk sor al memora en knawa ar tonelico"],
								
				'EXEC_NULLASCENSION':[	"Rrha apea gagis paul ini ar ciel", 
										"Wee num ra, gran faja dius manafaln sheak, pat syec yeal."],
										
				'EXEC_PURGER':[	"Was ki ra selena anw hymmnos PURGER", 
								"En ma i ga chs syec van nel an hymme endia"],
								
				'EXEC_RE=NATION':[	"Was yea ra waath near en hymme RE=NATION mea"],
									
				'EXEC_SOL=FAGE':[	"Rrha ki ra nha_HYMMNOS/1x01 >> pat mea en xest DIVIEGA_SIANN > A0.",
									"Rrha ki ra enne sos yor",
									"Rrha ki ra parge_HYMMNOS/1x01 anw DIVIEGA=SIANN > A0."],
									
				'EXEC_SPHILIA':["Kiafa hynne mea? pagle tes yor",
								"Kiafa sarla? Pagle tes yor",
								"Was yea ra pauwel en wael yor",
								"Echrra en chs ar dor",
								"Yorr faf, so",
								"Yorr hierle",
								"Mea paul yor",
								"Yorr nille mea",
								"Yorr desfel",
								"Yorr ween shell",
								"Mea paul yor",
								"Mea nille yor",
								"Kiafa hynne mea, sarla na layy, ar knawa yor",
								"Vinan yor, noglle yor, presia messe noce yor tes mea"],
				
				'EXEC_VIENA':[	"Was yea erra chs sheak, en sol anw yeal.",
								"Was quel erra chs lusye eazas.",
								"Presia firle anw harton, van yor jyel der polon, yanje."],
				
				'EXEC_over.METHOD_SUBLIMATION':[],
				
				'METHOD_IMPLANTA':[],
				
				'METHOD_METAFALICA':["Was paks ra faja juez/.", "Over the earth, for many years dry without rain, sounds of droplets fall, each fleeting, each precious..."],
				
				'METHOD_REPLEKIA':[	"xO herr mLYOrArA du sphaela, m.t.y.y. giz wOsLYI du giz/.", 
									"xN rre hLYImLYUmOrO a.u.k. zess quesa byui q.l.s. du sechel/.", 
									"xA herr nAtAnO hymmnos, ut ouvyu m.r.r. du daedu ag ujes/."]}
						
dict_answers = {
				'EXEC_SPHILIA':{1:"\"Fou paks ga kiafa hynne yor.\"",
								2:"\"Wee paks ga faf yora accrroad mea?\"",
								3:"\"Wee paks ga chs mea?\"",
								4:"\"Was paks ga chs na mea, en paul yor yora harton mea...Faura, cexm here, shellan mea. Fowrlle art fluy, presia sonwe.\"",
								5:"\"Was ki ga faf so.\"",
								6:"\"Was ki ga hierle.\"",
								7:"\"Was ki ga paul yor.\"",
								8:"\"Yorr nille mea.\"",
								9:"\"Was ki ga desfel.\"",
								10:"\"Was ki ga ween shell.\"",
								11:"\"Was ki ga paul yor.\"",
								12:"\"Mea nille yorr.\"",
								16:"\"Mea irs here aulla omnis en noes irs sphilar aulla omnis\""},
				'METHOD_METAFALICA':{1:"Was granme ra chs sos yor/.", 2:"Soon the blooming flowers will color this land."}
			}