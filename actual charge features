# clean up descriptions
statutes['statCh'] = statutes.StatuteCode.apply(lambda x: x.split('.')[0])

rep=['in the (first|second|third|fourth) degree','attempted','\(.*?\)','-','felony','misdemeanor','2013','2015','2016']
statutes['newdesc']=statutes.StatuteDesc
for i in rep:
    statutes['newdesc'] = statutes.newdesc.str.replace(i,'', case=False)
statutes['newdesc']=statutes.newdesc.str.strip().str.lower()
len(statutes.newdesc.unique())


# dictionary
statDict = {
    'poss' : ['possession'],
    'delivery' : ['delivery'],
    'man' : ['manufacture'],
    'marijuana' : ['marijuana'],
    'opioid' : ['oxycodone','hydrocodone','methadone','heroin'],
    'drugs' : ['methamphetamine','oxycodone','hydrocodone','methadone','marijuana','heroin','mdma','cocaine','controlled substance'],
    'assault' : 'assaul?',
    'reck_endand' : 'recklessly endangering',
    'sex' : ['sodomy','sexual','rape','incest','intimate','sexually','indecency'],
    'sex_vio' : ['sodomy','rape','penetration','sexual abuse'],
    'menace_stalk' : ['menacing','menace','stalking','invasion of personal privacy','mistreatment'],
    'officer_vic' : ['officer','uniform'],
    'murder' : ['murder','manslaughter','homicide'],
    'child_vic' : ['a minor','child','under 18 years'],
    'human_traff' : ['trafficking','buying or selling a person'],
    'custodial' : ['custodial interference','nonsupport'],
    'kidnap' : ['kidnapping'],
    'strang' : ['strangulation'],
    'violent_vs_person_nosex' : ['kidnapping'] + ['strangulation'] + ['murder','manslaughter','homicide'] + ['stun gun','body armor'],
    'coerc' : 'coercion',
    'nonlethweap' : ['stun gun','body armor'],
    'sex_off' : ['sex offender'],
    'harass' : ['harassment','harass'],
    'firearm' : ['firearm','gun'],
    'weapon' : ['firearm','gun'] + ['weapon', 'destructive device','body armor'],
    'dead_vic' : ['memorial','corpse'],
    'disord' : ['disorderly'],
    'racketeer' : ['racketerring','racketeering'],
    'theft' : ['theft'],
    'burg_rob' : ['burglary', 'robbery'],
    'burgrobth' : ['burglary', 'robbery']+['theft']+['rented or leased personal property'],
    'mischief' : ['mischief'],
    'trespass' : ['trespass'],
    'litter' : ['trash','littering','litter'],
    'stolecar' : ['stolen vehicle','unauthorized use of a vehicle','entry into a motor vehicle','rented or leased motor vehicle'],
    'computer' : ['computer crime'],
    'arson' : ['arson','burning'],
    'forest' : ['forest products','forest land'],
    'money' : ['money laundering'],
    'resist' : ['resisting arrest'],
    'bribes' : 'brib?',
    'interfering' : ['interfering with a peace officer','false information','hindering','initiating a false report','interfering with a firefighter','obstructing','false swearing','perjury','unsworn falsification'],
    'misconduct' : 'official misconduct',
    'out' : ['escape','unauthorized departure','fleeing'],
    'impers' : ['impersonation'],
    'fraud1' : 'fraud?',
    'prostitute' : 'prostitut?',
    'animal_vic' : ['animal','dog'],
    'driving' : ['driver','driving'],
    'fakeid' : ['drivers licence','false information','production of identification','misuse of licence',"person's license"],
    'mip' : ['minor in possession'],
    'servingalch' : ['serving without','furnishing alcohol'],
    'conspiracy' : ['conspiracy'],
    'solic' : ['solicitation'],
    'obtassist' : ['public assistance','nutritional assistance'],
    'mortfraud' : ['mortgage'],
    'other' : ['other'],
    'boat' : ['boat'],
    'cont' : ['contracting without a license'],
    'fireworks' : ['fireworks'],
    'jury' : ['jury instructions'],
    'forfeit' : 'forfeit?',
    'tax' : ['tax'],
    'contempt' : ['contempt'],
    'failtoapp' : ['failure to appear'],
}




def statfeatures(words, colname):
    if isinstance(words, list) == False:
        pat=words
    else:
        pat='|'.join(map(re.escape,words))
    statutes[colname]=statutes.newdesc.str.contains(pat)


for key in statDict:
    colname=key
    statfeatures(statDict[key],colname)

statutes    


statutes['wildlife_hunt'] = statutes.statCh.str.contains('497|496|498')       
statutes['fraud'] = statutes.statCh.str.contains('165')
statutes['duii'] = statutes.statCh.str.contains('813')

        
