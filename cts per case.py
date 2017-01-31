# get count of charges per case


import pandas as pd

call = ("SELECT tblNameActual.NameID, tblNameActual.FullName, tblCaseActual.CaseID,"
        " COUNT(Charges.CountID) as charges"
        " FROM tblNameActual"
        " JOIN tblCaseActual"
        " ON tblNameActual.NameID = tblCaseActual.NameID"
        " JOIN Charges"
        " ON tblCaseActual.CaseID = Charges.CaseID"
        " WHERE tblNameActual.NameID > 541"
        " AND tblNameActual.NameID != 219998"
        " AND tblNameActual.NameID != 222460"
        " AND tblNameActual.NameID NOT LIKE '%test%'" 
        " AND tblNameActual.FullName != 'Mickey Mouse'"
        " AND tblNameActual.FullName NOT LIKE '%UNKNOWN%'"
        " AND tblNameActual.FullName != 'NO DEFENDANT'"
        " AND tblNameActual.FullName != 'EXPUNGED'"
        " AND tblCaseActual.RcvdDt >= '2013-01-01'"
        " GROUP BY tblNameActual.NameID, tblNameActual.FullName, tblCaseActual.CaseID"
        " ORDER BY tblNameActual.NameID")
        
ctspercase = pd.read_sql(call,cnxn)

print ctspercase.head()

# histogram
import matplotlib.pyplot as plt
import numpy as np

plt.hist(ctspercase['charges'], bins=20)
plt.title("Number of Charges Per Person Per Case")
plt.xlabel("# Charges Against")
plt.ylabel("Individuals")



# get total count per person
grp = ctspercase['charges'].groupby(ctspercase.NameId.)
totc = grp.sum()

totc2 = ctspercase.groupby(['NameID'])['charges'].sum()
totc2.head()

# due to mismatch between caseActual and Charges, missing charge info for ~ 3000 defendants
totct = pd.DataFrame({'TotCharge': totc}).reset_index()


