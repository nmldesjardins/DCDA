# Run connect.py first to open db connection


import pandas as pd
# get number of cases for each person
# filters for tests cases, but keeps unknowns/no defendant/expunged
# this does NOT filter for date (some older records included, could be inaccurate)

call_all = ('SELECT tblNameActual.FullName, tblNameActual.NameID,' 
        ' COUNT(tblCaseActual.CaseID) as cases' 
        ' FROM tblNameActual'
        ' JOIN tblCaseActual'
        ' ON tblCaseActual.NameID = tblNameActual.NameID'
        ' WHERE tblNameActual.NameID > 541' 
        " AND tblNameActual.NameID != 219998"
        " AND tblNameActual.NameID != 222460"
        " AND tblNameActual.NameID NOT LIKE '%test%'" 
        " AND tblNameActual.FullName != 'Mickey Mouse'"
        ' Group BY tblNameActual.FullName, tblNameActual.NameID'
        ' ORDER BY cases')


ncases = pd.read_sql(call_all,cnxn)
print ncases.head()

# only get cases from 2013 forward

call13 = ('SELECT tblNameActual.FullName, tblNameActual.NameID,' 
        ' COUNT(tblCaseActual.CaseID) as cases' 
        ' FROM tblNameActual'
        ' JOIN tblCaseActual'
        ' ON tblCaseActual.NameID = tblNameActual.NameID'
        ' WHERE tblNameActual.NameID > 541' 
        " AND tblNameActual.NameID != 219998"
        " AND tblNameActual.NameID != 222460"
        " AND tblNameActual.NameID NOT LIKE '%test%'" 
        " AND tblNameActual.FullName != 'Mickey Mouse'"
        " AND tblCaseActual.RcvdDt >= '2013-01-01'"
        ' Group BY tblNameActual.FullName, tblNameActual.NameID'
        ' ORDER BY cases')

ncases13 = pd.read_sql(call13,cnxn)
print ncases13.head()

print ncases13.describe()

# only get cases from 2013 forward, exclude unknowns

call13ex = ('SELECT tblNameActual.FullName, tblNameActual.NameID,' 
        ' COUNT(tblCaseActual.CaseID) as cases' 
        ' FROM tblNameActual'
        ' JOIN tblCaseActual'
        ' ON tblCaseActual.NameID = tblNameActual.NameID'
        ' WHERE tblNameActual.NameID > 541' 
        " AND tblNameActual.NameID != 219998"
        " AND tblNameActual.NameID != 222460"
        " AND tblNameActual.NameID NOT LIKE '%test%'" 
        " AND tblNameActual.FullName != 'Mickey Mouse'"
        " AND tblNameActual.FullName NOT LIKE '%UNKNOWN%'"
        " AND tblNameActual.FullName != 'NO DEFENDANT'"
        " AND tblNameActual.FullName != 'EXPUNGED'"
        " AND tblCaseActual.RcvdDt >= '2013-01-01'"
        ' Group BY tblNameActual.FullName, tblNameActual.NameID'
        ' ORDER BY cases')

ncases13_ex = pd.read_sql(call13ex,cnxn)

#cnxn.close()


## check data

xtb = pd.crosstab(index=ncases13['cases'], columns='count')
print xtb # two highest (43, 75) are unknowns

# histogram
import matplotlib.pyplot as plt
import numpy as np

plt.hist(ncases13_ex['cases'], bins=20)
plt.title("Number of Cases Per Person")
plt.xlabel("# Cases Against")
plt.ylabel("Individuals")

# create recidivsim feature
def recid (row):
    if row['cases'] == 1:
        return 0
    return 1

ncases13_ex['recid01'] = ncases13_ex.apply(lambda row:recid(row), axis=1)


for i in ncases13_ex:
    if ncases13_ex['cases']==1:
        ncases13_ex['recid01']==0
    else:
        ncases13_ex['recid01']==1
