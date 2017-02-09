# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 11:38:40 2017

@author: Insight
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 18:34:00 2017

@author: Insight
"""

"""
    defines dictionaries of semi-hierarchical features (e.g., drug -> opiates)
    feeds to createfeatures to create the features
    truncated dictionaries: only for top crimes, top sentences
    
"""
## Statutes (Counts/Charges)
statDictT = {
    'count_poss' : ['possession'],
    'count_drug_heroin' : ['heroin'],
    'count_drug_meth': ['methamphetamine'],
    'count_drug_drugs' : ['methamphetamine','oxycodone','hydrocodone','methadone','heroin','mdma','cocaine','controlled substance'],
    'count_assault' : 'assaul?',
    'count_reckEndang' : 'recklessly endangering',
    'count_menace' : ['menacing','menace'],
    'count_harass' : ['harassment','harass'],
    'count_theft' : ['theft'],
    'count_burglary' : ['burglary'],
    'count_mischief' : ['mischief'],
    'count_trespass' : ['trespass'],
    'count_computer' : ['computer crime'],
    'count_driving' : ['driver','driving'],
    'count_contempt' : ['contempt'],
    'count_IDtheft' : ['identity theft'],
    'count_suspRev': ['driving while suspended'],
    'count_sexAbuse' : ['sexual abuse'],
    'count_testRefus' : ['refusal to take test'] ,
    'count_vehicle' : ['motor vehicle']  
}
    



## Conditions on Judgement
judgecondition_topicsDictT = {
    'jcond_eval' : ['eval'], # any evalution
    'jcond_domesticvio' : ['domestic violence','stddvb','stddva'],
    'jcond_sexoff' : ['sex offender','stdso'],
    'jcond_nocontact' : ['nocon'],
    'jcond_jail':['jail'],
    'jcond_prison' : ['prison'],
    'jcond_parole' : ['parole'],
    'jcond_probation' : ['probation'],
    'jcond_fine' : ['fine'],
    'jcond_duii' : ['stdduii'],
    'jcond_comserv' : ['community serivce'] ,
    'jcond_drug' : ['stddrg'],
    'jcond_weapon' : ['weapon','firearms'],
    'jcond_testing' : ['test','uas'],
    'jcond_alcohol' :['alcohol'],
    'jcond_crufew': ['curfew'],
    'jcond_motVeh' : ['traffic','vehicle']
}


## Sentences   
# truncated sentence types (does not enclude eligibility for programs, upward/downward dispositonal)
sentDictT = {'senttypeT_jail' : ['jail'],
    'senttypeT_probation' : ['probation'],
    'senttypeM_restitution' : ['restitution'],
    'senttypeM_fine': ['fine'],
    'senttype_gridblock': ['gridblock'],
    'senttypeT_postPrisSuperviz' : ['post-prison supervision'],
    'senttypeT_prison' : ['prison'],
    'senttypeM_fees':['fee','cost'],
    'senttypeT_elecmonit':['electronic monitoring'],
    'senttypeT_allincarceration' : ['jail','prison'],
    'senttypeT_allsupervision' : ['probation','supervision','electronic monitoring'],
    'senttypeM_allmoney': ['fine','fee','cost','restitution','surcharge'],
    'senttypeT_commService':['community service'],
    'senttype_domesticViolence' : ['domestic violence']
}



# unit of duration of sentence
# this way isn't ideal, but was having issues getting a more straightforward for - if loop to run
timeDict = {'month': ['month'],
            'day': ['day'],
            'week':['week'],
            'hour':['hour'],
            'year' : ['year']
            }
