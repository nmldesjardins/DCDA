# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 11:52:16 2017

@author: Insight

create truncated df w/ just the top crimes, codes for top sentences
"""

from dflonglong import dflong
import numpy as np
import pandas as pd
import datetime
from featurefunctions import *
from featureDictsTrunc import *



#### Summary Variables ####
group = dflong.groupby('NameID')

# total number of cases for each person
dflong['nCases'] = group.CaseID.transform('nunique')

# total number of counts for each person
dflong['nCounts'] = group.CountID.transform('nunique')

# recidivist
dflong['recidivist'] = dflong.apply(lambda row:recid(row), axis=1)

# mark first case
dflong['RcvdDt'] = pd.to_datetime(dflong['RcvdDt'], dayfirst=True)
dflong['firstCaseDt'] = group.RcvdDt.transform('min')
dflong['firstCase'] = dflong.apply(lambda row:fcase(row), axis=1)


#### Demographic Variables ####
# age at time of case

dflong['DOBd'] = pd.to_datetime(dflong['DOB'], dayfirst=True)

# all are %d/%m/%y format; py interprets years before 68 as 2068
dflong['DOBd2'] = dflong['DOBd'].apply(lambda x: x.replace(year = x.year-100) if x.year > 2005 else x.replace(year = x.year))

dflong['age'] = (dflong.RcvdDt - dflong.DOBd2)/np.timedelta64(1,'Y')


# age categories
dflong['age_under18'] = dflong['age'].apply(lambda x :1 if x < 18 else 0)
dflong['age_1824'] = dflong['age'].apply(lambda x :1 if (17 < x < 25) else 0)
dflong['age_2534'] = dflong['age'].apply(lambda x :1 if (24 < x < 35) else 0)
dflong['age_3544'] = dflong['age'].apply(lambda x :1 if (34 < x < 45) else 0)
dflong['age_4554'] = dflong['age'].apply(lambda x :1 if (44 < x < 55) else 0)
dflong['age_5464'] = dflong['age'].apply(lambda x :1 if (54 < x < 65) else 0)
dflong['age_over65'] = dflong['age'].apply(lambda x :1 if x > 64 else 0)



# recode race
dflong['RaceNew'] = dflong.Race.astype(str)
dflong.replace({'RaceNew': {r'A.*': 'Asian',
                            r'B': 'Black',
                            r'H': 'HispanicLatino', 
                            r'I':'AmInAKNat',
                            r'NH': 'NatHIPacIsl', 
                            r'W' : 'White', 
                            r'U': 'Unknown',
                            r'MTO': 'OtherMult',
                            r'nan': None}}, regex=True, inplace=True)

dflong = pd.concat([dflong,pd.get_dummies(dflong.RaceNew,prefix='Race',dummy_na=False)],axis=1)


#### Statutes/Charges/Counts ####

## clean up ##

# extract chapter code from full statute code, where available 
dflong.StatuteCode2 = dflong.StatuteCode.apply(lambda x: 'no' if x == None else x)
dflong['statCh'] = dflong.StatuteCode2.apply(lambda x: x.split('.')[0])



# clean up statute descriptions
rep = ['in the (first|second|third|fourth) degree','attempted','\(.*?\)','-','felony','misdemeanor','2013','2015','2016']
 
dflong['newStatdesc'] = dflong.StatuteDesc

for i in rep:
    dflong['newStatdesc'] = dflong.newStatdesc.str.replace(i,'', case=False)
dflong['newStatdesc'] = dflong.newStatdesc.str.strip().str.lower()
dflong['newStatdesc'] = dflong.newStatdesc.apply(lambda x: 'no' if x == None else x)


# save just the most common crimes
common = ['assault', 'burglary', 'computer','contempt', 'mischief','trespass',
           'driving under the influence', 'driving while suspended/revoked', 
           'failure to perform duties', 'harassment', 'identity theft', 'menacing',
           'reckless driving', 'recklessly endangering with a motor', 
           'refusal to take test', 'sexual abuse', 'theft', 'possession of heroin',
           'possession of metham'] #47
commonp='|'.join(map(re.escape,common))

dflong = dflong[dflong['newStatdesc'].str.contains(commonp)]


## create features ##

# severity codes - use as is
dflong = pd.concat([dflong,pd.get_dummies(dflong.StatuteSeverityDesc,prefix='countSev_')],axis=1)


# create features for homogenous statutes
dflong['count_duii'] = dflong.statCh.str.contains('813').astype(int)
dflong['count_againstPersons'] = dflong.statCh.str.contains('163').astype(int)
dflong['count_againstProperty'] = dflong.statCh.str.contains('164').astype(int)


# pre-coded case attributes - only by case; don't match to counts
#dflong = pd.concat([dflong,pd.get_dummies(dflong.CaseAttribute,prefix='catt_')],axis=1)
#dflong = pd.concat([dflong,pd.get_dummies(dflong.CaseAttDesc,prefix='cattde_')],axis=1)


# all other statutes
dict2feat(statDictT,'newStatdesc',dflong)


#### Judgements ####

## clean up ##

dflong['EventType'] = dflong.EventType.str.lower()

dflong['condtopic'] = dflong['Description']
dflong['condtopic'] = dflong.condtopic.apply(lambda x: 'no' if x == None else x)
dflong['condtopic'] = dflong.condtopic.apply(lambda x: x.split(':')[0])
dflong['condtopic'] = dflong.condtopic.apply(lambda x: x.split('-')[-1])
dflong['condtopic']= dflong.condtopic.str.replace('\(.*?\)','')
dflong['condtopic'] =  dflong.condtopic.str.strip().str.lower()


## create features ##

# final disposition
dflong = pd.concat([dflong,pd.get_dummies(dflong.dispocode, prefix='disp')],axis=1)

# plea - use given categories +1 to encompass all guilty possibilities
dflong = pd.concat([dflong,pd.get_dummies(dflong.pleadesc, prefix='plea')],axis=1)
dflong['plea_allguilt'] = dflong.statCh.str.contains('guilty').astype(int)

# conditions on judgement - lots of variability; use all codes (173)
#dflong = pd.concat([dflong,pd.get_dummies(dflong.EventType, prefix='jccode')],axis=1)

# conditions on judgement - decompose into 10 broad topics
dict2feat(judgecondition_topicsDictT,'condtopic',dflong)



#### Sentences ####  

## clean up ##
dflong['senttypedesc'] = dflong.SentenceTypeDesc.str.lower().astype(str)

dflong['SentenceFromDesc'] = dflong['SentenceFromDesc'].astype(str)
dflong['senttime'] = dflong.SentenceFromDesc.str.strip().str.lower()
dflong['senttime'] = dflong.senttime.str.replace('life','100 years', case=False)

dflong['sentDurRaw'] = dflong.senttime.apply(lambda x: x.split(' ')[0])
dflong['sentDurRaw'] = dflong.sentDurRaw.str.replace('days','0', case=False)
dflong['sentDurRaw'] = dflong.sentDurRaw.str.replace('1:00','0', case=False)
dflong['sentDurRaw'] = dflong.sentDurRaw.str.replace('none','0', case=False)
dflong['sentDurRaw'] = dflong.sentDurRaw.str.replace('completed','0', case=False)
dflong['sentDurRaw'] = dflong['sentDurRaw'].astype(float)

dflong['sentDurUnit'] = dflong.senttime.apply(lambda x: x.split(' ')[-1])
dflong['sentDurUnit'] = dflong['sentDurUnit'].astype(str)



## create features ##

# truncated sentence types (does not enclude eligibility for programs, upward/downward dispositonal)
dict2feat(sentDictT,'senttypedesc',dflong)


# duration of sentence
dflong['timeMult'] = pd.Series()

dflong.ix[dflong.sentDurUnit.isin(['months','month']),'timeMult'] = 30.5
dflong.ix[dflong.sentDurUnit.isin(['day','days','days.']),'timeMult'] = 1.0
dflong.ix[dflong.sentDurUnit.isin(['year','years']),'timeMult'] = 365.0
dflong.ix[dflong.sentDurUnit.isin(['hours']),'timeMult'] = 0.042

dflong['sentDur_Days'] = dflong.timeMult * dflong.sentDurRaw
dflong['sentDur_Years'] = dflong.sentDur_Days/365


# fine/fee amount
# Amount1 and Amount2 are both floats; add together for total
dflong['sentPayTotal'] = dflong.Amount1.fillna(0) + dflong.Amount2.fillna(0)

# create duration/amt for each sentence type (these go together)
labs = sentDictT.keys()
sentTerm(labs, dflong, newvalT='sentDur_Years', newvalM = 'sentPayTotal')

