# -*- coding: utf-8 -*-
"""
Created on Thu Feb 02 21:45:11 2017

@author: Insight
"""

from truncatedFeatures import dflong
from featureDictsTrunc import *
import pandas as pd

"""
    after features are created, this module restructures the long dataframe.
    whereas dflong has multiple sentences for each count (and multiple counts for each 
    case, and multiple cases for each person), this module restructures the data
    to be long by count only: it combines the sentencing conditions for each
    count onto a single row.
"""

#### Judgement Condition ####
## Judgement Condition / Sentence / Count --> Judgement/Count

# create df that counts judgement condition for each sentence on each charge
var = judgecondition_topicsDictT.keys()
var1 = var[0]
var = var[1:len(var)]
          
df_jc = pd.DataFrame(dflong[['jcond_parole',
 'jcond_weapon',
 'jcond_duii',
 'jcond_eval',
 'jcond_jail',
 'jcond_testing',
 'jcond_crufew',
 'jcond_prison',
 'jcond_fine',
 'jcond_motVeh',
 'jcond_drug',
 'jcond_probation',
 'jcond_sexoff',
 'jcond_alcohol',
 'jcond_domesticvio',
 'jcond_comserv',
 'jcond_nocontact','CountID']])

df_jc = pd.DataFrame(df_jc.drop_duplicates())
df_jc.head()

# initalize df
dfwide_jc = pd.DataFrame(dflong.groupby(['CountID'])[var1].sum())
for i in var:
    tmp = pd.DataFrame(dflong.groupby(['CountID'])[i].sum())
    dfwide_jc = pd.merge(dfwide_jc,tmp,left_index=True,right_index=True)


dfwide_jc['CountID'] = dfwide_jc.index


#### Sentences ####

# get all sentences for a given count on one row
# include yes/no + attached amount/duration + total amount/duration

# identify sentence-relevant columns
scols = dflong.columns.to_series().str.contains('sent')
scols['CountID'] = True

# get just those columns
dflong_s = dflong[dflong.columns[scols]]

# remove excess rows (one row = one portion of the sentence)
dflong_s = pd.DataFrame(dflong_s.drop_duplicates())
list(dflong_s)
# define variable names
varS = list(dflong_s)[6:len(list(dflong_s))]

# initalize df
dfwide_sent = pd.DataFrame(dflong_s.groupby(['CountID'])['senttypeM_fees'].sum())

# get sums for rest of vars
for i in varS:
    tmp = pd.DataFrame(dflong_s.groupby(['CountID'])[i].sum())
    dfwide_sent = pd.merge(dfwide_sent,tmp,left_index=True,right_index=True)
dfwide_sent['CountID'] = dfwide_sent.index


#### plea and disposition ####

pcols = dflong.columns.to_series().str.contains('plea_')
pcols['CountID'] = True
dflong_p = dflong[dflong.columns[pcols]]

dflong_p = pd.DataFrame(dflong_p.drop_duplicates())
varPd=list(dflong_p)[1:len(list(dflong_p))]
varP = list(dflong_p)[2:len(list(dflong_p))]

dfwide_plea = pd.DataFrame(dflong_p.groupby(['CountID'])['plea_Acquitted'].sum())

# get sums for rest of vars
for i in varP:
    tmp = pd.DataFrame(dflong_p.groupby(['CountID'])[i].sum())
    dfwide_plea = pd.merge(dfwide_plea,tmp,left_index=True,right_index=True)
dfwide_plea['CountID'] = dfwide_plea.index


dcols = dflong.columns.to_series().str.contains('disp_')
dcols['CountID'] = True
dflong_d = dflong[dflong.columns[dcols]]
varDd = list(dflong_d)[1:len(list(dflong_d))]

dflong_d = pd.DataFrame(dflong_d.drop_duplicates())
dflong_d= dflong_d.rename(columns = lambda x: x.strip())

varD = list(dflong_d)
varD = varD[2:len(varD)]

dfwide_d = pd.DataFrame(dflong_d.groupby(['CountID'])['disp_CD'].sum())

# get sums for rest of vars
for i in varD:
    tmp = pd.DataFrame(dflong_d.groupby(['CountID'])[i].sum())
    dfwide_d = pd.merge(dfwide_d,tmp,left_index=True,right_index=True)
dfwide_d['CountID'] = dfwide_d.index



#### Count-level sentence and judgement condition ####

dfwide = pd.merge(dfwide_jc, dfwide_sent)
dfwide = pd.merge(dfwide, dfwide_plea)
dp = list(dfwide)

dfwide = pd.merge(dfwide, dfwide_d)
len(dfwide.CountID.unique())
dfwide = pd.DataFrame(dfwide.drop_duplicates())

#### Count-level all variables ####
dp = dp + varDd + ['senttypedesc','senttime','sentDurRaw','sentDurUnit','timeMult']
dp +=  ['SentenceTypeDesc','SentenceFromDesc','Amount1', 'Amount2','SentenceNotes']
dp += ['EventType','Description','condtopic']
dp +=['dispocode','dispodesc','pleacode','pleadesc']
#dp = dp[2:len(dp)]+['jcond_weapon']  - use if creating features for all the codes

dropcol = [value for value in dp if value != 'CountID']

dflong2 = dflong.drop(dropcol,axis=1)
dflong2.head()


dflong3 = pd.DataFrame(dflong2.drop_duplicates())

"""
    troubleshooting duplicate counts
    
len(dflong3)
list(dflong3)
pd.set_option("display.max_columns",250)
dflong3.loc[dflong3['CountID']==372436]
dflong3.CountID.isnull().sum()

pd.set_option("display.max_rows",100)

dflong3.CountID.loc[dflong3.duplicated(subset='CountID') == True]
dflong3['dupe']=dflong3.duplicated(subset='CountID')

dflong3 = dflong3.sort_values('CountID')
dflong3.CountID.loc[dflong3['dupe']==True]

dflong3[['CountID','pleacode','dispocode']].loc[dflong3['dupe']==True]


dflong.loc[dflong['CountID']==337967]
dupegrupe = pd.concat(g for _, g in dflong3.groupby("CountID") if len(g)>1)
dupegrupe

x = pd.concat(dflong.CountID,dflong3.duplicated(subset = 'CountID'))

"""
# produce final dataframe:

dfcount = pd.merge(dflong3,dfwide,on='CountID',how = 'left')
