from difflib import SequenceMatcher as matcher

singer=""
song = ""
song_flag=False
valid=False
dict_limits={}



dict_firstlines = 	{
					"Was yea ra enne ar ciel":'EXEC_HIBERNATION',
					"Was yea ra frreie yor wart en chs manaf an yor synk sor al memora en knawa ar tonelico":'EXEC_LINKER',
					"Rrha apea gagis paul ini ar ciel,":'EXEC_NULLASCENSION',
					#"Rrha ki ra exec hymmnos PURGER en yehar nha near yor":'EXEC_PURGER',
					"Was yea ra waath near en hymme RE=NATION mea.":'EXEC_RE=NATION',
					#"Rrha ki ra nha_HYMMNOS/1x01 >> pat mea en xest DIVIEGA=SIANN > A2.":'EXEC_SOL=FAGE',
					"Kiafa hynne mea? Pagle tes yor":'EXEC_SPHILIA',
					#"Hierle faura murfan anw yeeel ciel.":'EXEC_VIENA',
					#"":'EXEC_over.METHOD_SUBLIMATION',
					#"xN rre harr f.s. tes maoh ess ouvyu sechel":'METHOD_IMPLANTA',
					"hYAmmrA cEzE hymmnos ceku":'METHOD_METAFALICA',
					#"xA rre wArAmA maen a.u.k. zess titia":'METHOD_REPLEKIA',
					}
					
dict_songs =	{
				'EXEC_CHRONICLE=KEY':[	"Was au ga whai pauwel gaunji yasra whou na cenjue sor tou zuieg", 
										"Was ki ra, grandi en eterne slepir, presia aterra cremia sos viuy lonfa, yehar lamenza der soare mea"],
										
				'EXEC_DESPEDIA':[	"Rrha yea ra haf yor, forgandal knawa Manac yor, Manac"],
									
				'EXEC_HIBERNATION':["Initiate shutdown sequence.", 
									"As administrator, I order: Sleep."],
									
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
				
				'METHOD_METAFALICA':["hYAmmrA cEzE hymmnos ceku"],
				
				'METHOD_REPLEKIA':[	"xO herr mLYOrArA du sphaela, m.t.y.y. giz wOsLYI du giz/.", 
									"xN rre hLYImLYUmOrO a.u.k. zess quesa byui q.l.s. du sechel/.", 
									"xA herr nAtAnO hymmnos, ut ouvyu m.r.r. du daedu ag ujes/."], 
									
				}
						
dict_answers = {
				'EXEC_SPHILIA':["\"Fou paks ga kiafa hynne yor.\"",
								"\"Wee paks ga faf yora accrroad mea?\"",
								"\"Wee paks ga chs mea?\"",
								"\"Was paks ga chs na mea, en paul yor yora harton mea...Faura, cexm here, shellan mea. Fowrlle art fluy, presia sonwe.\"",
								"\"Was ki ga faf so.\"",
								"\"Was ki ga dict_answershierle.\"",
								"\"Was ki ga paul yor.\"",
								"\"Yorr nille mea.\"",
								"\"Was ki ga desfel.\"",
								"\"Was ki ga ween shell.\"",
								"\"Was ki ga paul yor.\"",
								"\"Mea nille yorr.\"",
								"\"Mea irs here aulla omnis en noes irs sphilar aulla omnis\""]
			}
			
dict_alimits = {'EXEC_SPHILIA':[1,2,3,4,5,6,7,8,9,10,11,12,16]}