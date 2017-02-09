# for local test only:
from testload import dflong

# for sql:
#from dflonglong import dflong

"""
    uses regex to clean up the statute descriptions
    generates chapter code for each ORS statutes
    defines semi-hierarchical features (e.g., drug -> opiates)
    
"""

# extract chapter code from full statute code
dflong['statCh'] = dflong.StatuteCode.apply(lambda x: x.split('.')[0])

# clean up statute descriptions
rep=['in the (first|second|third|fourth) degree','attempted','\(.*?\)','-','felony','misdemeanor','2013','2015','2016']
dflong['newStatdesc']=dflong.StatuteDesc
for i in rep:
    dflong['newStatdesc'] = dflong.newStatdesc.str.replace(i,'', case=False)
dflong['newStatdesc']=dflong.newStatdesc.str.strip().str.lower()



# dictionary
statDict = {
    'poss' : ['possession'],
    'delivery' : ['delivery'],
    'manufact' : ['manufacture'],
    'drug_marijuana' : ['marijuana'],
    'drug_opioid' : ['oxycodone','hydrocodone','methadone','heroin'],
    'drug_drugs' : ['methamphetamine','oxycodone','hydrocodone','methadone','marijuana','heroin','mdma','cocaine','controlled substance'],
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

statDict[key] = 'count_'+key

# iterate through dictionary to create binary features
def statfeatures(words, colname, origvar):
    if isinstance(words, list) == False:
        pat=words
    else:
        pat='|'.join(map(re.escape,words))
    dflong[colname]=dflong.origvar.str.contains(pat)

for key in statDict:
    colname=key
    statfeatures(statDict[key],colname,newStatdesc)

# create features for homogenous statutes
dflong['wildlife_hunt'] = dflong.statCh.str.contains('497|496|498')       
dflong['fraud'] = dflong.statCh.str.contains('165')
dflong['duii'] = dflong.statCh.str.contains('813')

# severity codes
dflong=pd.concat([dflong,pd.get_dummies(dflong.StatuteSeverityDesc,prefix='countSev_')],axis=1)

############### conditions and judgments #########
# disposition
dflong = pd.concat([dflong,pd.get_dummies(dflong.dispocode, prefix='disp')],axis=1)

# plea
dflong = pd.concat([dflong,pd.get_dummies(dflong.pleadesc, prefix='plea')],axis=1)
dflong['plea_allguilt'] = dflong.statCh.str.contains('guilty')

# conditions on judgement
# use all codes (173)
dflong['EventType'] = dflong.EventType.str.lower()

dflong = pd.concat([dflong,pd.get_dummies(dflong.EventType, prefix='jccode')],axis=1)



## for broader topics
dflong['condtopic'] = dflong['Description']
dflong['condtopic'] = dflong.condtopic.apply(lambda x: x.split(':')[0])
dflong['condtopic'] = dflong.condtopic.apply(lambda x: x.split('-')[-1])
dflong['condtopic']= dflong.condtopic.str.replace('\(.*?\)','')
dflong['condtopic'] =  dflong.condtopic.str.strip().str.lower()
dflong.condtopic.drop_duplicates()

judgecondition_topicsDict = {
    'jcond_eval' : ['eval'], # any evalution
    'jcond_domesticvio' : ['domestic violence','stddvb','stddva'],
    'jcond_sexoff' : ['sex offender','stdso'],
    'jcond_nocontact' : ['nocon'],
    'jcond_jail':['jail'],
    'jcond_prison' : ['prison'],
    'jcond_parole' : ['parole'],
    'jcond_probation' : ['probation'],
    'jcond_fine' : ['fine'],
    'jcond_duii' : ['stdduii']
}

for key in judgecondition_topicsDict:
    colname=key
    statfeatures(judgecondition_topicsDict[key],colname,condtopic)
    
############ sentences ###############   
# truncated sentence types (does not enclude eligibility for programs, upward/downward dispositonal)
sentDict = {'jail' : ['jail'],
    'probation' : ['probation'],
    'restitution' : ['restitution'],
    'fine': ['fine'],
    'gridblock': ['gridblock'],
    'superviz' : ['post-prison supervision'],
    'prison' : ['prison'],
    'fees':['fee','cost'],
    'elecmonit':['electronic monitoring']
}

sentDict[key] = 'sent_'+key

dflong['senttypedesc']=dflong.SentenceTypeDesc.str.lower()

for key in sentDict:
    colname=key
    statfeatures(sentDict[key],colname,origvar=senttypedesc)
    

