"""
    defines dictionaries of semi-hierarchical features (e.g., drug -> opiates)
    feeds to createfeatures to create the features
    
"""
## Statutes (Counts/Charges)
statDict = {
    'count_poss' : ['possession'],
    'count_delivery' : ['delivery'],
    'count_manufact' : ['manufacture'],
    'count_drug_marijuana' : ['marijuana'],
    'count_drug_opioid' : ['oxycodone','hydrocodone','methadone','heroin'],
    'count_drug_drugs' : ['methamphetamine','oxycodone','hydrocodone','methadone','marijuana','heroin','mdma','cocaine','controlled substance'],
    'count_assault' : 'assaul?',
    'count_reckEndang' : 'recklessly endangering',
    'count_sexAll' : ['sodomy','sexual','rape','incest','intimate','sexually','indecency'],
    'count_sexVio' : ['sodomy','rape','penetration','sexual abuse'],
    'count_menace_stalk' : ['menacing','menace','stalking','invasion of personal privacy','mistreatment'],
    'count_officer_vic' : ['officer','uniform'],
    'count_murder' : ['murder','manslaughter','homicide'],
    'count_child_vic' : ['a minor','child','under 18 years'],
    'count_humanTraff' : ['trafficking','buying or selling a person'],
    'count_custodial' : ['custodial interference','nonsupport'],
    'count_kidnap' : ['kidnapping'],
    'count_strangle' : ['strangulation'],
    'count_violentVperson_nosex' : ['kidnapping'] + ['strangulation'] + ['murder','manslaughter','homicide'] + ['stun gun','body armor'],
    'count_coerc' : 'coercion',
    'count_nonlethweap' : ['stun gun','body armor'],
    'count_sexOffend' : ['sex offender'],
    'count_harass' : ['harassment','harass'],
    'count_firearm' : ['firearm','gun'],
    'count_weaponAll' : ['firearm','gun'] + ['weapon', 'destructive device','body armor'],
    'count_dead_vic' : ['memorial','corpse'],
    'count_disorderlyCond' : ['disorderly'],
    'count_count_racketeer' : ['racketerring','racketeering'],
    'count_theft' : ['theft'],
    'count_burglaryRobbery' : ['burglary', 'robbery'],
    'count_BurgRobbThefUnlawPoss' : ['burglary', 'robbery']+['theft']+['rented or leased personal property'],
    'count_mischief' : ['mischief'],
    'count_trespass' : ['trespass'],
    'count_litter' : ['trash','littering','litter'],
    'count_stoleCar' : ['stolen vehicle','unauthorized use of a vehicle','entry into a motor vehicle','rented or leased motor vehicle'],
    'count_computer' : ['computer crime'],
    'count_arson' : ['arson','burning'],
    'count_forest' : ['forest products','forest land'],
    'count_moneyLaunder' : ['money laundering'],
    'count_resist' : ['resisting arrest'],
    'count_bribes' : 'brib?',
    'count_interfering' : ['interfering with a peace officer','false information','hindering','initiating a false report','interfering with a firefighter','obstructing','false swearing','perjury','unsworn falsification'],
    'count_misconduct' : 'official misconduct',
    'count_EscapeFlee' : ['escape','unauthorized departure','fleeing'],
    'count_impersonate' : ['impersonation'],
    'count_fraudAll' : 'fraud?',
    'count_prostitution' : 'prostitut?',
    'count_animal_vic' : ['animal','dog'],
    'count_driving' : ['driver','driving'],
    'count_fakeid' : ['drivers licence','false information','production of identification','misuse of licence',"person's license"],
    'count_mip' : ['minor in possession'],
    'count_servingAlch' : ['serving without','furnishing alcohol'],
    'count_conspiracy' : ['conspiracy'],
    'count_solic' : ['solicitation'],
    'count_obtAssist' : ['public assistance','nutritional assistance'],
    'count_mortFraud' : ['mortgage'],
    'count_other' : ['other'],
    'count_boat' : ['boat'],
    'count_contracting' : ['contracting without a license'],
    'count_fireworks' : ['fireworks'],
    'count_juryInst' : ['jury instructions'],
    'count_forfeit' : 'forfeit?',
    'count_tax' : ['tax'],
    'count_contempt' : ['contempt'],
    'count_failToApp' : ['failure to appear'],
    'count_gang' : ['gang']
}



## Conditions on Judgement
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


## Sentences   
# truncated sentence types (does not enclude eligibility for programs, upward/downward dispositonal)
sentDict = {'senttypeT_jail' : ['jail'],
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
    'senttypeM_allmoney': ['fine','fee','cost','restitution']
}



# unit of duration of sentence
# this way isn't ideal, but was having issues getting a more straightforward for - if loop to run
timeDict = {'month': ['month'],
            'day': ['day'],
            'week':['week'],
            'hour':['hour'],
            'year' : ['year']
            }
