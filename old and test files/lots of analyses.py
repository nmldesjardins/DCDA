# -*- coding: utf-8 -*-
"""
Created on Sun Feb 05 12:23:37 2017

@author: Insight
"""

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from patsy import dmatrices
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.cross_validation import cross_val_score
import pylab as pl
import statsmodels.api as sm
from matplotlib.font_manager import FontProperties
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import normalize
from scipy.stats import zscore


dfwide_recid = pd.DataFrame(dfcount.groupby(['recidivist','firstCase'])['newStatdesc2'].value_counts())

dfwide_recid.to_csv("crime by recidivism, first vs later case.csv")

desc = dfcount.groupby('recidivist').mean()
desc.to_csv("means by recidivism.csv")

desc_stat = dfcount.groupby('newStatdesc').mean()
desc_stat.to_csv("means by crime.csv")


dfcount.Time_senttypeT_jail.describe()


## available data
len(dfcount1.CaseID.unique())
len(dfcount1.NameID.unique())






# crimes by race
dfcount1.loc[dfcount1['Race']=='White2'].newStatdesc2.value_counts()
raceall_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.Race)
race_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.Race.loc[dfcount1['Race']!='White2'])
race_crime.div(race_crime.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

plt.pcolor(raceall_crime)
plt.yticks(np.arange(0.5,len(raceall_crime.index),1),raceall_crime.index)
plt.xticks(np.arange(0.5,len(raceall_crime.columns),1),raceall_crime.columns)


plt.pcolor(race_crime)
plt.yticks(np.arange(0.5,len(race_crime.index),1),race_crime.index)
plt.xticks(np.arange(0.5,len(race_crime.columns),1),race_crime.columns, rotation=45)


# crimes by gender
gender_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.Sex)
gender_crime.div(gender_crime.sum(1).astype(float),axis=0).plot(kind='bar',stacked=True)
plt.legend(bbox_to_anchor=(0,1))

        
a = dfcount1.loc[dfcount1['age']<100].copy()
age_crime = pd.crosstab(a.newStatdesc2, a.agecat)
age_crime.div(age_crime.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))
     


x[sents].corr(method = 'spearman')


sents = ['senttypeM_fees',
 'senttypeM_fine',
 'senttype_gridblock',
 'senttypeT_postPrisSuperviz',
 'senttypeM_restitution',
 'senttypeT_prison',
 'senttypeT_jail',
 'senttypeT_allincarceration',
 'senttypeT_commService',
 'senttype_domesticViolence',
 'senttypeT_allsupervision',
 'senttypeT_probation',
 'senttypeM_allmoney',
 'senttypeT_elecmonit']
 
len(dfcount1.sentTypes.unique())



"""
sent_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.sentcat)
sent_crime.div(sent_crime.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

""""
sent_crime2 = pd.crosstab(dfcount1.sentTypes, dfcount1.newStatdesc2, margins=True)
sent_crime2.to_csv("sentence combination by first crime.csv")

plt.pcolor(sent_crime)
plt.yticks(np.arange(0.5,len(sent_crime.index),1),sent_crime.index)
plt.xticks(np.arange(0.5,len(sent_crime.columns),1),sent_crime.columns)

smeanm= dfcount1.groupby(['newStatdesc2','recidivist']).mean()
smeanm.to_csv("crime means.csv")

# recidivism by sentence
sent_recid = pd.crosstab(dfcount1.recidivist, dfcount1.sentcat)
sent_recid.div(sent_recid.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

sent_recid2 = pd.crosstab(dfcount1.sentTypes.loc[(dfcount1['sentTypes']>20) & (dfcount1['sentTypes']!='')],dfcount1.recidivist.astype(bool)).plot(kind='bar')
plt.legend(bbox_to_anchor=(0,1))

sent_recid2 = pd.crosstab(dfcount1.sentTypes, dfcount1.recidivist)
sent_recid2.to_csv("recid by sentence type.csv")

# recidivism by crime
""""
crime_recid = pd.crosstab(dfcount1.newStatdesc2, dfcount1.recidivist)
crime_recid.div(crime_recid.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))
""""
rate = dfcount1.groupby(['newStatdesc2','js']).recidivist.mean()
rate.to_csv("recid rates.csv")

plt.pcolor(crime_recid)
plt.yticks(np.arange(0.5,len(crime_recid.index),1),crime_recid.index)
plt.xticks(np.arange(0.5,len(crime_recid.columns),1),crime_recid.columns)


crime_recid = pd.crosstab(dfcount1.recidivist, dfcount1.newStatdesc2.loc[dfcount1['newStatdesc2']=='duii']).plot(kind = 'bar')
crime_recid.div(crime_recid.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

# recidivism by race
race_recid = pd.crosstab(dfcount1.recidivist, dfcount1.Race)
race_recid2 = pd.crosstab(dfcount1.recidivist, dfcount1.Race.loc[dfcount1['Race']!='White2'])
race_recid2.div(race_recid2.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

# recidivism by severity
sev_recid = pd.crosstab(dfcount1.recidivist, dfcount1.StatuteSeverityDesc)
sev_recid.div(sev_recid.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

# race by severity
sev_race = pd.crosstab(dfcount1.recidivist, dfcount1.StatuteSeverityDesc)
sev_race2 = pd.crosstab(dfcount1.StatuteSeverityDesc, dfcount1.Race.loc[dfcount1['Race']!='White2'])
sev_race2.div(sev_race2.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))




groupall = dfcount1.groupby(['recidivist','Race','sentTypes','newStatdesc2'])

groupall.newStatdesc2.count().to_csv("recid by race sent crime.csv")

groupall = dfcount1.groupby(['recidivist','Sex','sentTypes','newStatdesc2'])

groupall.newStatdesc2.count().to_csv("recid by sex sent crime.csv")

groupall = dfcount1.groupby(['recidivist','agecat','sentTypes','newStatdesc2'])

groupall.newStatdesc2.count().to_csv("recid by age sent crime.csv")


groupall = dfcount1.groupby(['recidivist','sentcat','newStatdesc2'])

groupall.newStatdesc2.count().to_csv("recid by sent crime.csv")




groupRS = dfcount1.groupby(['Race','sentTypes'])
groupRS.newStatdesc2.count()

dfcount1.Race.value_counts()

dfcount1.sentTypes.value_counts()


## jcond instead of sentencing


dfcount1.jcond_Combo.value_counts()

len(dfcount1.jcond_Combo.unique())
## logistic regression
# create matrix
# use only first crimes

# descriptive tables
# by race
racestat = pd.crosstab(dfcount1.Race, dfcount1.newStatdesc, margins = True)

raceFine = pd.crosstab(dfcount1.Race, dfcount1.MoneysenttypeM_fine, margins = True)

dfcount1.groupby(['Race'])['MoneysenttypeM_fine'].mean()

dfcount1.groupby(['newStatdesc2'])['MoneysenttypeM_fine'].mean()

 

sent_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.js)
sent_crime.to_csv("comb sent crime.csv")


sent_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.js)
sent_crime.to_csv("comb sent crime.csv")

js2 = ['js_jail','js_prison','js_fine','js_probation','js_commServ']
x = dfcount1.groupby(['newStatdesc2','recidivist']).js_commServ.sum()
x.to_csv("sents.csv")

# just crimes

y_c, X_c = dmatrices('recidivist ~ stat_assault + stat_burglary + stat_computerCrime + \
                     stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                     stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                     stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                     stat_testRef + stat_theft + stat_trespass + stat_recklessDriving',
                     dfcount1, return_type = 'dataframe'
                     )

# flatten y 
y_c = np.ravel(y_c)


model = LogisticRegression()
modelC = model.fit(X_c, y_c)
modelC.score(X_c,y_c)
y_c.mean()
pd.DataFrame(zip(X_c.columns,np.transpose(model.coef_)))

m = sm.Logit(y_c, X_c)
mres = m.fit()
mres.summary()
mres.score()

# just sentences MoneysenttypeM_fees + MoneysenttypeM_fine,MoneysenttypeM_restitution +

# specific time/money
y_s, x_s = dmatrices('recidivist ~ MoneysenttypeM_fees + MoneysenttypeM_fine + MoneysenttypeM_restitution +\
                     Time_senttypeT_postPrisSuperviz + Time_senttypeT_prison + Time_senttypeT_jail +\
                     Time_senttypeT_commService + Time_senttypeT_probation + Time_senttypeT_elecmonit',
                     dfcount1, return_type = 'dataframe')


sentvals = ['MoneysenttypeM_fees', 'MoneysenttypeM_fine', 'MoneysenttypeM_restitution',
                     'Time_senttypeT_postPrisSuperviz','Time_senttypeT_prison', 'Time_senttypeT_jail',
                     'Time_senttypeT_commService','Time_senttypeT_probation','Time_senttypeT_elecmonit']

normalize(dfcount1[sentvals])

y_s, X_s = dmatrices('recidivist ~   MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                     Time_senttypeT_commService + Time_senttypeT_allsupervision',
                     dfcount1, return_type = 'dataframe')



y_s = np.ravel(y_s)
x_s = normalize(X_s)



m = sm.Logit(y_s, x_s)
mres = m.fit()
mres.summary()

# sentence category
y_s, X_s = dmatrices('recidivist ~   senttypeM_fees + senttypeM_fine +\
                      senttypeM_restitution +\
                     senttypeT_prison + senttypeT_jail + senttypeT_probation +\
                     senttypeT_elecmonit + senttypeT_commService +  senttypeT_jail:senttypeT_probation +\
                     senttypeT_probation:senttypeM_fine +\
                     senttypeT_jail:senttypeT_probation:senttypeM_fine +\
                     senttypeT_jail:senttypeT_probation:senttypeM_fees ',
                     dfcount1, return_type = 'dataframe')


m = sm.Logit(y_s, X_s)
mres = m.fit()
mres.summary()


# w/ j cond instead
y_j, X_j = dmatrices('recidivist ~ jcond_parole + jcond_duii + jcond_eval + \
                     jcond_jail + jcond_prison +\
                     jcond_fine  + jcond_drug + jcond_probation + \
                     jcond_sexoff + jcond_alcohol + jcond_domesticvio  +\
                     jcond_nocontact', dfcount1, return_type = 'dataframe')

jconds = ['jcond_parole','jcond_duii', 'jcond_eval', 'jcond_jail', 'jcond_testing',
          'jcond_crufew','jcond_prison','jcond_fine', 'jcond_motVeh', 'jcond_drug',
          'jcond_probation', 'jcond_sexoff', 'jcond_alcohol', 'jcond_domesticvio',
          'jcond_comserv', 'jcond_nocontact']
m = sm.Logit(y_j, X_j)
mres = m.fit()
mres.summary()



# w/ combined variables
y_js, X_js = dmatrices('recidivist ~ js_commServ + js_probation + js_fine +\
                       js_prison + js_jail + js_domesticVio', dfcount1,
                       return_type = 'dataframe')

m = sm.Logit(y_js, X_js)
mres = m.fit()
mres.summary()

y_d, X_d = dmatrices('recidivist ~ age_under18 + age_1824 + age_2534 + \
                     age_3544 + age_4554 + age_5464 + age_over65 + \
                      Race_Black2 + Race_HispanicLatino2  +\
                     Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                     Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M', 
                    dfcount1, return_type = 'dataframe')

y_d, X_d = dmatrices('recidivist ~ \
                      Race_Black + Race_HispanicLatino +\
                     Sex_F  + Sex_U', 
                    dfcount1, return_type = 'dataframe')
y_d = np.ravel(y_d)

m = sm.Logit(y_d, X_d)
mres = m.fit(maxiter=50)
mres.summary()

modelD = model.fit(X_d, y_d)
modelD.score(X_d, y_d)

pd.DataFrame(zip(X_d.columns,np.transpose(modelD.coef_)))

pd.crosstab(dfcount1.Race, dfcount1.recidivist.astype(bool)).plot(kind = 'bar')
pd.crosstab(dfcount1.Sex, dfcount1.recidivist.astype(bool)).plot(kind = 'bar')



### get feature importance

y_all, X_all = dmatrices('recidivist ~ age_under18 + age_1824 + age_2534 + \
                         age_3544 + age_4554 + age_5464 + age_over65 + \
                         Race_Black2 + Race_HispanicLatino2  +\
                         Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                         Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M +\
                         jcond_parole + jcond_duii + jcond_eval + \
                         jcond_jail + jcond_prison +\
                         jcond_fine  + jcond_drug + jcond_probation + \
                         jcond_sexoff + jcond_alcohol + jcond_domesticvio  +\
                         jcond_nocontact + \
                         senttypeM_fees + senttypeM_fine + senttypeM_restitution +\
                         senttypeT_prison + senttypeT_jail + senttypeT_probation +\
                         senttypeT_elecmonit + senttypeT_commService + \
                         MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                         Time_senttypeT_commService + Time_senttypeT_allsupervision +\
                         stat_assault + stat_burglary + stat_computerCrime + \
                         stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                         stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                         stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                         stat_testRef + stat_theft + stat_trespass + stat_recklessDriving + \
                         countSev__Felony + countSev__Misdemeanor + countSev__Violation +\
                         countSev__PunitiveSanctions', dfcount1, return_type = 'dataframe')
y_all = np.ravel(y_all)

features = pd.DataFrame()
features['features'] = X_all.columns


forest = ExtraTreesClassifier(n_estimators = 250, random_state = 123)

forest.fit(X_all, y_all)

features['importances'] = forest.feature_importances_
features['std'] = np.std([tree.feature_importances_ for tree in forest.estimators_], axis = 0)
features['indices'] = np.argsort(features.importances)[::-1]



features.sort_values(by = 'importances', ascending = False).head(10)

                         
dfcount1 = dfcount1.rename(columns = { 'countSev__Punitive Sanctions': 'countSev__PunitiveSanctions'})  

# note: compiles ok w/ all 3-way interactions; explodes if 4-ways are included                       
y_ALL, X_ALL = dmatrices('recidivist ~ age_under18 + age_1824 + age_2534 + \
                         age_3544 + age_4554 + age_5464 + age_over65 + \
                         Race_Black2 + Race_HispanicLatino2  +\
                         Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                         Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M +\
                         js_jail + js_prison +\
                         js_fine  + js_probation + \
                         js_commServ + \
                         MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                         Time_senttypeT_commService + Time_senttypeT_allsupervision +\
                         stat_assault + stat_burglary + stat_computerCrime + \
                         stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                         stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                         stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                         stat_testRef + stat_theft + stat_trespass + stat_recklessDriving + \
                         countSev__Felony + countSev__Misdemeanor + countSev__Violation + (age_under18 + age_1824 + age_2534 + \
                         age_3544 + age_4554 + age_5464 + age_over65 + \
                         Race_Black2 + Race_HispanicLatino2  +\
                         Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                         Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M) :\
                         (js_jail + js_prison +\
                         js_fine  + js_probation + \
                         js_commServ)  +\
                         (age_under18 + age_1824 + age_2534 + \
                         age_3544 + age_4554 + age_5464 + age_over65 + \
                         Race_Black2 + Race_HispanicLatino2  +\
                         Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                         Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M):\
                         (MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                         Time_senttypeT_commService + Time_senttypeT_allsupervision) +\
                         (age_under18 + age_1824 + age_2534 + \
                         age_3544 + age_4554 + age_5464 + age_over65 + \
                         Race_Black2 + Race_HispanicLatino2  +\
                         Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                         Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M):\
                         (stat_assault + stat_burglary + stat_computerCrime + \
                         stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                         stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                         stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                         stat_testRef + stat_theft + stat_trespass + stat_recklessDriving) +\
                         (age_under18 + age_1824 + age_2534 + \
                         age_3544 + age_4554 + age_5464 + age_over65 + \
                         Race_Black2 + Race_HispanicLatino2  +\
                         Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                         Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M) :\
                         (countSev__Felony + countSev__Misdemeanor + countSev__Violation) + (countSev__Felony + countSev__Misdemeanor + countSev__Violation) :\
                         (stat_assault + stat_burglary + stat_computerCrime + \
                         stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                         stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                         stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                         stat_testRef + stat_theft + stat_trespass + stat_recklessDriving) + (countSev__Felony + countSev__Misdemeanor + countSev__Violation) :\
                         (MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                         Time_senttypeT_commService + Time_senttypeT_allsupervision) +\
                         (countSev__Felony + countSev__Misdemeanor + countSev__Violation) :\
                         (js_jail + js_prison + js_fine  + js_probation + \
                         js_commServ) + (js_jail + js_prison + js_fine  + js_probation + \
                         js_commServ) :\
                         (MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                         Time_senttypeT_commService + Time_senttypeT_allsupervision) +\
                         (js_jail + js_prison + js_fine  + js_probation + \
                         js_commServ) :\
                         (stat_assault + stat_burglary + stat_computerCrime + \
                         stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                         stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                         stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                         stat_testRef + stat_theft + stat_trespass + stat_recklessDriving) +\
                         (stat_assault + stat_burglary + stat_computerCrime + \
                         stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                         stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                         stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                         stat_testRef + stat_theft + stat_trespass + stat_recklessDriving) :\
                         (MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                         Time_senttypeT_commService + Time_senttypeT_allsupervision)', 
                          dfcount1, return_type = 'dataframe')
                   

                    

y_ALL = np.ravel(y_ALL)

features = pd.DataFrame()
features['features'] = X_ALL.columns


forest = ExtraTreesClassifier(n_estimators = 250, random_state = 123)

forest.fit(X_ALL, y_ALL)

features['importances'] = forest.feature_importances_
features['std'] = np.std([tree.feature_importances_ for tree in forest.estimators_], axis = 0)
features['indices'] = np.argsort(features.importances)[::-1]

for f in range(X_ALL.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

for f in range(features.shape[1]):
    print("%d. %str (%f)" % (f + 1, features, features['indices'][f]))

importances = forest.feature_importances_
indices = np.argsort(features.importances)[::-1]
std = np.std([tree.feature_importances_ for tree in forest.estimators_], axis = 0)

features.sort_values(by = 'importances', ascending = False).head(20)
# don't do this - 16110 features; later just do ones > mean? top 10?
plt.figure()
plt.title("Feature Importances")
features.sort_values(features['importances']).head(10)
plt.bar(range(X_ALL.shape[1]), importances[indices], color = "r", yerr = std[indices], align = 'center')
plt.xticks(range(X_ALL.shape[1]), indices, rotation = 45)
plt.xlim([-1, X_ALL.shape[1]])


forest.predict(X_all)
forest.score(X_all, y_all)
forest.get_params()



# from statmodels instead

# get top5
dfcount1.newStatdesc2.value_counts()

# zscore money/time -- issue w/ z scores is they can be beyond -1:1
# normalize w/ max
dfcount1['allmoney_norm'] = dfcount1.MoneysenttypeM_allmoney/dfcount1.MoneysenttypeM_allmoney.max()
dfcount1['allsuperv_norm'] = dfcount1.Time_senttypeT_allsupervision/dfcount1.Time_senttypeT_allsupervision.max()
dfcount1['allincarc_norm'] = dfcount1.Time_senttypeT_allincarceration/dfcount1.Time_senttypeT_allincarceration.max()
dfcount1['allcommSer_norm'] = dfcount1.Time_senttypeT_commService/dfcount1.Time_senttypeT_commService.max()



y, X = dmatrices('recidivist ~ stat_assault + stat_duii + stat_theft +\
                 stat_recklessEndg + stat_recklessDriving +\
                 MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                 Time_senttypeT_allsupervision + Time_senttypeT_commService +\
                 (stat_assault + stat_duii + stat_theft +\
                 stat_recklessEndg + stat_recklessDriving) :\
                 (MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                 Time_senttypeT_allsupervision + Time_senttypeT_commService)',
                  dfcount1, return_type = 'dataframe')

y, X = dmatrices('recidivist ~ stat_assault + stat_duii + stat_theft +\
                 stat_recklessEndg + stat_recklessDriving +\
                 MoneysenttypeM_allmoney +\
                 (stat_assault + stat_duii + stat_theft +\
                 stat_recklessEndg + stat_recklessDriving) :\
                 (MoneysenttypeM_allmoney)',
                  dfcount1, return_type = 'dataframe')                
                   

# flatten y 
y = np.ravel(y)
X = normalize(X)

m = sm.Logit(y, X)
mres = m.fit()
mres.summary()
mres.score()

# just sentences MoneysenttypeM_fees + MoneysenttypeM_fine,MoneysenttypeM_restitution +

# specific time/money
y_s, x_s = dmatrices('recidivist ~ MoneysenttypeM_fees + MoneysenttypeM_fine + MoneysenttypeM_restitution +\
                     Time_senttypeT_postPrisSuperviz + Time_senttypeT_prison + Time_senttypeT_jail +\
                     Time_senttypeT_commService + Time_senttypeT_probation + Time_senttypeT_elecmonit',
                     dfcount1, return_type = 'dataframe')

mD2res.pred_table()

##### ploting money for 5 top crimes


y, X = dmatrices('recidivist ~ stat_assault + stat_duii + stat_theft +\
                 stat_recklessEndg + stat_recklessDriving +\
                 MoneysenttypeM_allmoney +\
                 (stat_assault + stat_duii + stat_theft +\
                 stat_recklessEndg + stat_recklessDriving) :\
                 (MoneysenttypeM_allmoney)',
                  dfcount1.loc[dfcount1['MoneysenttypeM_allmoney']<20000], return_type = 'dataframe')                
                   

# flatten y 
y = np.ravel(y)
X = normalize(X)

m = sm.Logit(y, X)
mres = m.fit()
mres.summary()



# evenly spaced range of money values - 
dfcount1.loc[dfcount1['MoneysenttypeM_allmoney']>0].MoneysenttypeM_allmoney.plot(kind='hist')


def sigmoid(t):
    return (1/(1+np.e**(-t)))
    
y = sigmoid(dfcount1.demo_pred)
plt.plot(y)


def isolate_and_plot(variable):
    groups = pd.pivot_table(dfcount1, values = ['demo_pred'], index=[variable,'Race'], aggfunc=np.mean)
    colors = 'rbgyrbgy'
    for col in dfcount1.Race.unique():
        plt_data = groups.ix[groups.index.get_level_values(1)==col]
        pl.plot(plt_data.index.get_level_values(0), plt_data['demo_pred'], color = colors[int(col)])
        
    pl.xlabel(variable)
    pl.ylabel("P(recid = 1)")
    pl.show()

isolate_and_plot('Sex_M')

    
    
    
    
    
np.exp(mD2res.params)

# probs for all combinations
def cartesian(arrays, out=None):
    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n, len(arrays)], dtype = dtype)
    
    m = n / arrays[0].size
    out[:,0] = np.repeat(arrays[0],m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m,1:])
        for j in xrange(1,arrays[0].size):
            out[j*m: (j+1)*m,1:] = out[0:m,1:]
    return out

combos = pd.DataFrame(cartesian([['M','F','U'],['White','Black','HispanicLatino'],[1.]]))  
combos.columns = ['sex','race','intercept']
dummy_sex = pd.get_dummies(combos['sex'],prefix = 'Sex')
dummy_race = pd.get_dummies(combos['race'], prefix = 'Race')

combos = combos.join(dummy_sex)
combos = combos.join(dummy_race.ix[:, 'Race_White':])

combos[X_d]

combos['rec_pred'] = mD2res.predict(combos)


# all
y_all, X_all = dmatrices('recidivist ~ count_duii + count_againstPersons + count_againstProperty + \
                     count_menace + count_poss + count_computer + count_drug_drugs + \
                     count_trespass + count_assault + count_driving + count_theft +\
                     count_reckEndang + count_drug_heroin + count_burglary + count_suspRev +\
                     count_harass + count_mischief + count_sexAbuse + count_testRefus +\
                     count_vehicle + count_IDtheft + count_drug_meth + count_contempt +\
                     MoneysenttypeM_allmoney +\
                      Time_senttypeT_jail + Time_senttypeT_probation +\
                     age_under18 + age_1824 + age_2534 + \
                     age_3544 + age_4554 + age_5464 + age_over65 + \
                      Race_Black + Race_HispanicLatino + Race_White +\
                     Sex_F  + Sex_U +\
                     (count_duii + count_againstPersons + count_againstProperty + \
                     count_menace + count_poss + count_computer + count_drug_drugs + \
                     count_trespass + count_assault + count_driving + count_theft +\
                     count_reckEndang + count_drug_heroin + count_burglary + count_suspRev +\
                     count_harass + count_mischief + count_sexAbuse + count_testRefus +\
                     count_vehicle + count_IDtheft + count_drug_meth + count_contempt) : \
                     (MoneysenttypeM_allmoney +\
                      Time_senttypeT_jail + Time_senttypeT_probation)',
                     dfcount1, return_type = 'dataframe'
                     )

y_all = np.ravel(y_all)


m = sm.Logit(y_all, X_all)
mres = m.fit(maxiter=100)
m.summary()

modelA = model.fit(X_all, y_all)
modelA.summary()
modelA.score(X_all, y_all)
y_all.mean()
pd.DataFrame(zip(X_all.columns,np.transpose(modelA.coef_)))

dfcount1[['sentPayTotal','sentDur_Years']].corr()


##
x = dfcount1[['NameID','Race','Sex','DLState','age']].copy()
x = x.drop_duplicates()


exp(.496)