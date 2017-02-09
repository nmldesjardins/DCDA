from createFirstCrimes import dfcount1
from restructure import dfcount

import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import pylab as pl
import plotly.plotly as py
import plotly.graph_objs as go
from patsy import dmatrices
from sklearn import metrics
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.preprocessing import normalize
import statsmodels.api as sm

"""
    This module produces tables and plots of the top crimes and recidivism rates by
    sentencing and demographic groups.
    It also runs preliminary logistic regressions predicting recidivism from each type of
    feature, and a preliminary ExtraTreesClassifier to get a sense of the most important features
"""


#### Descriptive Analyses ####

# Examine differences in the number of counts for each of the top crimes for non-recidivists, 
# recidivists' first cases, and recidivists' subsequent cases

dfwide_recid = pd.DataFrame(dfcount.groupby(['recidivist','firstCase'])['newStatdesc2'].value_counts())



### Focus on First Cases Only ###
# These are the first cases for recidivists + only cases for non-recidivists
# They are only included if charges were in top 19 crimes

## Determine available data
# number of cases
len(dfcount1.CaseID.unique())
# number of defendants
len(dfcount1.NameID.unique())


## Frequency of Charges by Demographic Groups

# race 
# because the sample is primarily (98%) White, exclude to get better view of minority groups
raceall_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.Race)
race_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.Race.loc[dfcount1['Race']!='White2'])
race_crime.div(race_crime.sum(1).astype(float), axis=0).plot(kind='bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))


# crimes by gender
gender_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.Sex)
gender_crime.div(gender_crime.sum(1).astype(float),axis=0).plot(kind='bar',stacked=True)
plt.legend(bbox_to_anchor=(0,1))

        
# crimes by age
# remove cases with unknown ages (> 100; entered as 1900-05-25)
a = dfcount1.loc[dfcount1['age']<100].copy()
age_crime = pd.crosstab(a.newStatdesc2, a.agecat)
age_crime.div(age_crime.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))
     

## Crimes by Sentences

sent_crime = pd.crosstab(dfcount1.newStatdesc2, dfcount1.sentcat)
sent_crime.div(sent_crime.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))


sent_crime2 = pd.crosstab(dfcount1.sentTypes, dfcount1.newStatdesc2, margins=True)

# use combined conditions + sentences
sent_crime3 = pd.crosstab(dfcount1.newStatdesc2, dfcount1.js)

#### Recidivism ####

# recidivism by sentence
sent_recid = pd.crosstab(dfcount1.recidivist, dfcount1.sentcat)
sent_recid.div(sent_recid.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

sent_recid2 = pd.crosstab(dfcount1.sentTypes.loc[(dfcount1['sentTypes']>20) & (dfcount1['sentTypes']!='')],dfcount1.recidivist.astype(bool)).plot(kind='bar')
plt.legend(bbox_to_anchor=(0,1))

sent_recid2 = pd.crosstab(dfcount1.sentTypes, dfcount1.recidivist)

# recidivism by crime
crime_recid = pd.crosstab(dfcount1.newStatdesc2, dfcount1.recidivist)
crime_recid.div(crime_recid.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

rate = dfcount1.groupby(['newStatdesc2','js']).recidivist.mean()

# recidivism by crime severity
sev_recid = pd.crosstab(dfcount1.recidivist, dfcount1.StatuteSeverityDesc)
sev_recid.div(sev_recid.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))

# recidivism by race
race_recid = pd.crosstab(dfcount1.recidivist, dfcount1.Race)
# exclude White defendants
race_recid2 = pd.crosstab(dfcount1.recidivist, dfcount1.Race.loc[dfcount1['Race']!='White2'])
race_recid2.div(race_recid2.sum(1).astype(float),axis=0).plot(kind = 'bar', stacked=True)
plt.legend(bbox_to_anchor=(0,1))


# get counts of counts for all combinations
# note that these produce VERY small groups - use with caution
dfcount1.groupby(['recidivist','Race','js','newStatdesc2']).newStatdesc2.count()

dfcount1.groupby(['recidivist','Sex','js','newStatdesc2']).newStatdesc2.count()

dfcount1.groupby(['recidivist','agecat','js','newStatdesc2']).newStatdesc2.count()

dfcount1.groupby(['recidivist','js','newStatdesc2']).newStatdesc2.count()

# fines and durations
# remove outliers for fines
dfcount1.loc[(dfcount1['sentPayTotal']>0) & (dfcount1['sentPayTotal']<10000)].groupby(['recidivist'])['sentPayTotal'].mean()
dfcount1.loc[(dfcount1['sentPayTotal']>0) & (dfcount1['sentPayTotal']<10000)].groupby(['recidivist'])['sentPayTotal'].mean()
dfcount1.loc[(dfcount1['sentPayTotal']>0) & (dfcount1['sentPayTotal']<10000)].groupby(['newStatdesc2'])['sentPayTotal'].mean()
dfcount1.loc[(dfcount1['sentPayTotal']>0) & (dfcount1['sentPayTotal']<10000)].groupby(['newStatdesc2','recidivist'])['sentPayTotal'].mean()

# only include durations > 0
dfcount1.loc[dfcount1['sentDur_Years']>0].groupby(['recidivist'])['sentDur_Years'].mean()
dfcount1.loc[dfcount1['sentDur_Years']>0].groupby(['recidivist'])['sentDur_Years'].mean()
dfcount1.loc[dfcount1['sentDur_Years']>0].groupby(['newStatdesc2'])['sentDur_Years'].mean()
dfcount1.loc[dfcount1['sentDur_Years']>0].groupby(['newStatdesc2','recidivist'])['sentDur_Years'].mean()

# correlation
dfcount1[['sentPayTotal','sentDur_Years']].corr()


#### Logistic Regression ####
# preliminary descriptive regressions (not predictive - no training or validation)
# include each feature group separately for simplicity

# crimes only
y_c, X_c = dmatrices('recidivist ~ stat_assault + stat_burglary + stat_computerCrime + \
                     stat_contempt + stat_drivingSuspRev + stat_duii + stat_failuretoperf + \
                     stat_harassment + stat_heroin + stat_identityTheft + stat_menacing +\
                     stat_methamphetamine + stat_mischief  + stat_sexualAbuse +\
                     stat_testRef + stat_theft + stat_trespass + stat_recklessDriving',
                     dfcount1, return_type = 'dataframe')

# flatten y 
y_c = np.ravel(y_c)

m = sm.Logit(y_c, X_c)
mres = m.fit()
mres.summary()


## sentences 

# specific time/money
y_s, X_s = dmatrices('recidivist ~ MoneysenttypeM_fees + MoneysenttypeM_fine + MoneysenttypeM_restitution +\
                     Time_senttypeT_postPrisSuperviz + Time_senttypeT_prison + Time_senttypeT_jail +\
                     Time_senttypeT_commService + Time_senttypeT_probation + Time_senttypeT_elecmonit',
                     dfcount1, return_type = 'dataframe')
y_s = np.ravel(y_s)
X_s = normalize(X_s)

m = sm.Logit(y_s, X_s)
mres = m.fit()
mres.summary()

# aggregated time/money
y_s2, X_s2 = dmatrices('recidivist ~   MoneysenttypeM_allmoney + Time_senttypeT_allincarceration +\
                     Time_senttypeT_commService + Time_senttypeT_allsupervision',
                     dfcount1, return_type = 'dataframe')

y_s2 = np.ravel(y_s2)
X_s2 = normalize(X_s2)

m = sm.Logit(y_s2, X_s2)
mres = m.fit()
mres.summary()



# sentence category

y_js, X_js = dmatrices('recidivist ~ js_commServ + js_probation + js_fine +\
                       js_prison + js_jail + js_domesticVio', dfcount1,
                       return_type = 'dataframe')

y_js = np.ravel(y_js)
m = sm.Logit(y_js, X_js)
mres = m.fit()
mres.summary()

# demographic variables
y_d, X_d = dmatrices('recidivist ~ age_under18 + age_1824 + age_2534 + \
                     age_3544 + age_4554 + age_5464 + age_over65 + \
                      Race_Black2 + Race_HispanicLatino2  +\
                     Race_AmInAKNat2 + Race_Asian2 + Race_NatHIPacIsl2 + \
                     Race_White2 + Race_Unknown2 + Sex_F  + Sex_U + Sex_M', 
                    dfcount1, return_type = 'dataframe')


y_d = np.ravel(y_d)

m = sm.Logit(y_d, X_d)
mres = m.fit(maxiter=50)
mres.summary()




### Extra Trees Classifier: Get Preliminary Feature Importance
# rename sanctions column
dfcount1 = dfcount1.rename(columns = { 'countSev__Punitive Sanctions': 'countSev__PunitiveSanctions'})  

# note: here, including only the two-way interactions
# processor fails when 3-way and 4-way interactions are included                     
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

# create dataframe to store feature importances
features = pd.DataFrame()
features['features'] = X_ALL.columns

# initialize the classifier
forest = ExtraTreesClassifier(n_estimators = 250, random_state = 123)
# fit the model
forest.fit(X_ALL, y_ALL)

features['importances'] = forest.feature_importances_
features['std'] = np.std([tree.feature_importances_ for tree in forest.estimators_], axis = 0)
features['indices'] = np.argsort(features.importances)[::-1]


# get top 20 features
features.sort_values(by = 'importances', ascending = False).head(20)

forest.score(X_ALL, y_ALL)
