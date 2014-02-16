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
		
		
functions = {'EXEC_HIBERNATION':"hibernation", 'METHOD_METAFALICA':"_method_metafalica", 'EXEC_LINKER':"_admin", 'EXEC_CHRONICLE=KEY':'hibernation', 'EXEC_SPHILIA':'pass', "EXEC_PURGER":'exec_purger', 'EXEC_DESPEDIA':'lockdown', 'METHOD_ALTERNATION':""}
		
dict_songs =	{
				'EXEC_HIBERNATION':["Was yea ra enne ar ciel./", 
									"Rrha num ra sleipir etealune na near na morto ciel./"],
									
				'EXEC_CHRONICLE=KEY':[	"Wee ki ra selena anw yasra wiene en chs CHRONICLE=KEY sos yor/.", 
										"Was ki ra, grandi en eterne slepir./"],
										
				'EXEC_DESPEDIA':[	"Rrha yea ra haf yor, forgandal knawa Manac yor, Manac./"],
															
				'EXEC_LINKER':[	"Was yea ra frreie yor wart en chs manaf an yor/.", 
								"Synk sor al memora en knawa Ar tonelico/."],
								
				'EXEC_NULLASCENSION':[	"Rrha apea gagis paul ini ar ciel./", 
										"Wee num ra, gran faja dius manafaln sheak, pat syec yeal./"],
										
				'EXEC_PURGER':[	"Rrha ki ra exec hymmnos PURGER/.", "Was ki ra selena anw hymmnos PURGER en ma i ga chs syec van nel an hymme endia./", ""],
								
				'EXEC_RE=NATION':[	"Was yea ra waath near en hymme RE=NATION mea./"],
									
				'EXEC_SOL=FAGE':[	"Rrha ki ra nha_HYMMNOS/1x01 >> pat mea en xest DIVIEGA_SIANN > A0./",
									"Rrha ki ra enne sos yor./",
									"Rrha ki ra parge_HYMMNOS/1x01 anw DIVIEGA=SIANN > A0./"],
									
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
												
				'METHOD_METAFALICA':[	"Was paks ra faja juez/.", 
										"Ueber der Erde, seit vielen Jahren verdorrt ohne Regen, fallen sanfte Tropfen - ein jeder vergaenglich, ein jeder kostbar..."],
				
				'METHOD_REPLEKIA':[	"xO herr mLYOrArA du sphaela, m.t.y.y. giz wOsLYI du giz/.", 
									"xA herr nAtAnO hymmnos, ut ouvyu m.r.r. du daedu ag ujes/."],
									
				'METHOD_ALTERNATION':['sLYAnAsA ut Cogito ag tLYAhAkAtA du ahjeas/.', 'cAzA YAragym ag nYAyAgEt YAxinfar esyfo/.', 'Please, give me power.', 'Please, give hope to the people.', 'To save', 'this world', 'please recognize me.']					
				}
						
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
				'METHOD_METAFALICA':{1:"Was granme ra chs sos yor/.", 2:"Schon bald tauchen Blueten das Land in helle Farben."},
				'METHOD_ALTERNATION':{3:'For what reason?', 4:'For whose sake?', 5:'Your wish?', 6:'You desire?'}
			}