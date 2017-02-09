from restructure import dfcount 
import pandas as pd
import re
import numpy as np

"""
    this module cals the truncated, restructured dataframe from restructure
    it selects only the first cases for each defendant
    and then re-engineers some of the features for analysis
"""

# select only the first cases

dfcount1 = dfcount.loc[dfcount['firstCase']==1].copy()

# simplify top crime classifications
dfcount1['newStatdesc2'] = dfcount1.newStatdesc.astype(str)
dfcount1['newStatdesc2'] = dfcount1.newStatdesc.map( {'unlawful possession of methamphetamine': 'methamphetamine',
                            'identity theft' : 'identityTheft',
                            'aggravated identity theft' : 'identityTheft',
                            'theft': 'theft', 
                            'theft 1 by receiving' : 'theft',
                            'aggravated theft' : 'theft',
                            'theft of services' : 'theft',
                            'theft 3 by receiving' : 'theft',
                            'theft by deception' : 'theft',
                            'theft 2 by receiving' : 'theft',
                            'mail theft; receipt of stolen mail c/f' : 'theft',
                            'theft of lost or mislaid property' : 'theft',
                            'theft by extortion' : 'theft',
                            'theft  a violation': 'theft',
                            'mail theft; receipt of stolen mail a/m':'theft',
                            'reckless driving':'recklessDriving',
                            'recklessly endangering with a motor vehicle': 'recklessEndg',
                            'criminal mischief  with a motor vehicle' :'mischief',
                            'criminal mischief' : 'mischief',                           
                            'unlawful possession of heroin': 'heroin', 
                            'refusal to take test for intoxicants' : 'testRef', 
                            'harassment': 'harassment',
                            'telephonic harassment': 'harassment',
                            'sexual harassment' : 'harassment',
                            'aggravated harassment' : 'harassment',
                            'criminal trespass': 'trespass',
                            'criminal trespass while in possession of a firearm':'trespass',
                            'menacing': 'menacing',
                            'driving while suspended/revoked': 'drivingSuspRev',
                            'burglary':'burglary',
                            'possession of a burglary tool or theft device' : 'burglary',  
                            'driving under the influence of intoxicants  alcohol' : 'duii',
                            'driving under the influence of intoxicants' : 'duii',
                            'assaulting a law enforcement animal' : 'assault',
                            'assault  against former victim' : 'assault',
                            'assault' : 'assault',
                            'assault   witnessed by a minor' : 'assault',
                            'assault  with a motor vehicle' : 'assault',
                            'assaulting a public safety officer' : 'assault',
                            'vehicular assault of a bicyclist or pedestrian' : 'assault',
                            'contempt of court' : 'contempt',
                            'sexual abuse': 'sexualAbuse',
                            'encouraging child sexual abuse': 'sexualAbuse',
                            'computer crime' : 'computerCrime',
                            'failure to perform duties of driver when property is damaged': 'failuretoperf',
                            'failure to perform duties of driver to injured persons': 'failuretoperf'
                            })

# create dummies from shorter desc
dfcount1 = pd.concat([dfcount1,pd.get_dummies(dfcount1.newStatdesc2,prefix='stat',dummy_na=False)],axis=1)


#### recode demographics and create dummy variables ####

# race
dfcount1.replace({'Race': {'A  ': 'Asian2',
                            'ASI' : 'Asian2',
                            'B  ': 'Black2',
                            'H  ': 'HispanicLatino2', 
                            'I  ':'AmInAKNat2',
                            'NH ': 'NatHIPacIsl2', 
                            'W  ' : 'White2', 
                            'U  ': 'Unknown2',
                            'MTO': 'OtherMult2',
                            'nan': None}}, inplace=True)
dfcount1 = pd.concat([dfcount1,pd.get_dummies(dfcount1.Race,prefix='Race',dummy_na=False)],axis=1)

# sex
dfcount1 = pd.concat([dfcount1,pd.get_dummies(dfcount1.Sex,prefix='Sex',dummy_na=False)],axis=1)
dfcount1 = dfcount1.rename(columns = { 'Sex_F  ': 'Sex_F',
                                      'Sex_M  ' : 'Sex_M',
                                      'Sex_U  ' : 'Sex_U'})

# age
# create single indicator variable
def labage(row):
    if row['age_under18']==1:
        return 'under18'
    elif row['age_1824']==1:
        return 'age_1824'
    elif row['age_2534']==1:
        return 'age_2534'
    elif row['age_3544']==1: 
        return 'age_3544'
    elif row['age_4554']==1:
        return 'age_4554'
    elif row['age_5464']==1:
        return 'age_5564'
    else:
        return 'over65'

dfcount1['agecat'] = dfcount1.apply(lambda row: labage(row), axis=1)

#### Sentencing ####
# create indicator variable from Sentences sentence type
def sentType(row):
     if row['senttypeT_jail'] == 1:
         return 'jail' 
     if row['senttypeM_fees'] == 1 :
         return 'fee'
     if row['senttypeM_fine'] == 1 :
         return 'fine'
     if row['senttypeT_postPrisSuperviz'] == 1:
         return 'postPrisSup'
     if row['senttypeM_restitution'] == 1 :
         return 'restitut_only'
     if row['senttypeT_prison'] == 1:
         return 'prison'
     if row['senttypeT_commService']==1:
         return 'commService'
     if row['senttypeT_probation'] == 1 :
         return 'probation'
     if row['senttypeT_elecmonit'] == 1:
         return 'elecMonit'

dfcount1['sentcat'] = dfcount1.apply(lambda row: sentType(row), axis=1)         

# make codes binary
dfcount1['senttypeM_fees'] = dfcount1.senttypeM_fees.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeM_fine'] = dfcount1.senttypeM_fine.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_postPrisSuperviz'] = dfcount1.senttypeT_postPrisSuperviz.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeM_restitution'] = dfcount1.senttypeM_restitution.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_prison'] = dfcount1.senttypeT_prison.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_jail'] = dfcount1.senttypeT_jail.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_allincarceration'] = dfcount1.senttypeT_allincarceration.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttype_domesticViolence'] = dfcount1.senttype_domesticViolence.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_allsupervision'] = dfcount1.senttypeT_allsupervision.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_probation'] = dfcount1.senttypeT_probation.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeM_allmoney'] = dfcount1.senttypeM_allmoney.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_elecmonit'] = dfcount1.senttypeT_elecmonit.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['senttypeT_commService'] = dfcount1.senttypeT_commService.apply(lambda x: 1 if x>= 1 else 0)

# create string variable - will be used to generate all combinations of sentences
dfcount1['senttype_Feesa'] = dfcount1.senttypeM_fees.replace(1, 'fee').astype(str)
dfcount1['senttypeM_finea'] = dfcount1.senttypeM_fine.replace(1, 'fine').astype(str)
dfcount1['senttypeT_postPrisSuperviza'] = dfcount1.senttypeT_postPrisSuperviz.replace(1, 'postPriSup').astype(str)
dfcount1['senttypeM_restitutiona'] = dfcount1.senttypeM_restitution.replace(1, 'restitut').astype(str)
dfcount1['senttypeT_prisona'] = dfcount1.senttypeT_prison.replace(1, 'prison').astype(str)
dfcount1['senttypeT_jaila'] = dfcount1.senttypeT_jail.replace(1, 'jail').astype(str)
dfcount1['senttypeT_probationa'] = dfcount1.senttypeT_probation.replace(1, 'probation').astype(str)
dfcount1['senttypeT_elecmonita'] = dfcount1.senttypeT_elecmonit.replace(1, 'elecMonit').astype(str)
dfcount1['senttypeT_commServicea'] = dfcount1.senttypeT_commService.replace(1, 'elecMonit').astype(str)

# generate all possible combinations
dfcount1['sentTypes']=dfcount1.senttypeT_jaila + dfcount1.senttype_Feesa + \
dfcount1.senttypeM_finea + dfcount1.senttypeT_postPrisSuperviza + dfcount1.senttypeM_restitutiona +\
dfcount1.senttypeT_commServicea + dfcount1.senttypeT_probationa + dfcount1.senttypeT_elecmonita

dfcount1['sentTypes']=dfcount1.sentTypes.str.replace('0',"")

## create indicators from the judgement conditions

def jcondType(row):
     if row['jcond_parole'] >= 1:
         return 'parole' 
     if row['jcond_eval'] >= 1 :
         return 'evaluation'
     if row['jcond_jail'] >= 1 :
         return 'jail'
     if row['jcond_duii'] >= 1:
         return 'duii package'
     if row['jcond_testing'] >= 1  :
         return 'testing'
     if row['jcond_crufew'] >= 1:
         return 'curfew'
     if row['jcond_prison']>=1:
         return 'prison'
     if row['jcond_fine']  >= 1 :
         return 'fine'
     if row['jcond_probation'] >= 1:
         return 'probation'
     if row['jcond_comserv'] >= 1:
         return 'commServ'
     if row['jcond_nocontact'] >= 1:
         return 'noContactOrder'
     if row['jcond_nocontact'] >= 1:
         return 'noContactOrder'
dfcount1['jcondCat'] = dfcount1.apply(lambda row: jcondType(row), axis=1)   
dfcount1.jcondCat.value_counts()      


dfcount1['jcond_parole'] = dfcount1.jcond_parole.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_duii'] = dfcount1.jcond_duii.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_eval'] = dfcount1.jcond_eval.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_jail'] = dfcount1.jcond_jail.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_testing'] = dfcount1.jcond_testing.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_crufew'] = dfcount1.jcond_crufew.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_prison'] = dfcount1.jcond_prison.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_fine'] = dfcount1.jcond_fine.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_motVeh'] = dfcount1.jcond_motVeh.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_drug'] = dfcount1.jcond_drug.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_probation'] = dfcount1.jcond_probation.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_sexoff'] = dfcount1.jcond_sexoff.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_alcohol'] = dfcount1.jcond_alcohol.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_domesticvio'] = dfcount1.jcond_domesticvio.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_comserv'] = dfcount1.jcond_comserv.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['jcond_nocontact'] = dfcount1.jcond_nocontact.apply(lambda x: 1 if x>= 1 else 0)


dfcount1['jcond_parolea'] = dfcount1.jcond_parole.replace(1, 'Parole').astype(str)
dfcount1['jcond_duiia'] = dfcount1.jcond_duii.replace(1, 'DUII').astype(str)
dfcount1['jcond_evala'] = dfcount1.jcond_eval.replace(1, 'Eval').astype(str)
dfcount1['jcond_jaila'] = dfcount1.jcond_jail.replace(1, 'Jail').astype(str)
dfcount1['jcond_testinga'] = dfcount1.jcond_testing.replace(1, 'Testing').astype(str)
dfcount1['jcond_curfewa'] = dfcount1.jcond_crufew.replace(1, 'Curfew').astype(str)
dfcount1['jcond_prisona'] = dfcount1.jcond_prison.replace(1, 'Prison').astype(str)
dfcount1['jcond_finea'] = dfcount1.jcond_fine.replace(1, 'Fine').astype(str)
dfcount1['jcond_motVeha'] = dfcount1.jcond_motVeh.replace(1, 'MotVeh').astype(str)
dfcount1['jcond_druga'] = dfcount1.jcond_drug.replace(1, 'Drug').astype(str)
dfcount1['jcond_probationa'] = dfcount1.jcond_probation.replace(1, 'Probation').astype(str)
dfcount1['jcond_sexoffa'] = dfcount1.jcond_sexoff.replace(1, 'SexOff').astype(str)
dfcount1['jcond_alcohola'] = dfcount1.jcond_alcohol.replace(1, 'Alch').astype(str)
dfcount1['jcond_domesticvioa'] = dfcount1.jcond_domesticvio.replace(1, 'DV').astype(str)
dfcount1['jcond_comserva'] = dfcount1.jcond_comserv.replace(1, 'CommServ').astype(str)
dfcount1['jcond_nocontacta'] = dfcount1.jcond_nocontact.replace(1, 'NoCont').astype(str)

dfcount1['jcond_Combo'] = dfcount1.jcond_parolea + dfcount1.jcond_duiia + dfcount1.jcond_evala +\
dfcount1.jcond_jaila + dfcount1.jcond_testinga + dfcount1.jcond_curfewa + \
dfcount1.jcond_prisona + dfcount1.jcond_finea + dfcount1.jcond_motVeha +\
dfcount1.jcond_druga + dfcount1.jcond_probationa + dfcount1.jcond_sexoffa +\
dfcount1.jcond_alcohola + dfcount1.jcond_domesticvioa + dfcount1.jcond_comserva +\
dfcount1.jcond_nocontacta

dfcount1['jcond_Combo']=dfcount1.jcond_Combo.str.replace('0',"")


# there is some overlap between senttype and jcond, but they're mostly independent
 # use both to maximize data

dfcount1['js_commServ'] = dfcount1.jcond_comserv + dfcount1.senttypeT_commService
dfcount1['js_probation'] = dfcount1.jcond_probation + dfcount1.senttypeT_probation
dfcount1['js_fine'] = dfcount1.jcond_fine + dfcount1.senttypeM_fine
dfcount1['js_prison'] = dfcount1.jcond_prison + dfcount1.senttypeT_prison
dfcount1['js_jail'] = dfcount1.jcond_jail + dfcount1.senttypeT_jail
dfcount1['js_domesticVio'] = dfcount1.jcond_domesticvio + dfcount1.senttype_domesticViolence


dfcount1['js_probation'] = dfcount1.js_probation.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['js_fine'] = dfcount1.js_fine.apply(lambda x: 1 if x>= 1 else 0)
dfcount1['js_jail'] = dfcount1.js_jail.apply(lambda x: 1 if x>= 1 else 0)


def jsType(row):
     if row['js_jail'] >= 1 :
         return 'jail'
     if row['js_prison']>=1:
         return 'prison'
     if row['js_fine']  >= 1 :
         return 'fine'
     if row['js_probation'] >= 1:
         return 'probation'
     if row['js_commServ'] >= 1:
         return 'commServ'

dfcount1['js'] = dfcount1.apply(lambda row: jsType(row), axis=1)   

