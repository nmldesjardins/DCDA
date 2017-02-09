"""
Run connect.py first to open db connection
Gets all demographic and case info
"""
import pandas as pd

call=("SELECT tblNameActual.*, tblCaseActual.NameID, tblCaseActual.CaseID,"
      " tblCaseActual.RcvdDt, tblCaseActual.Status, tblCaseActual.StatusDt, Charges.*"
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
      " AND tblCaseActual.RcvdDt >= '2013-01-01'")

namescases = pd.read_sql(call,cnxn)

print namescases.head()

xtb = pd.crosstab(index=namescases['RcvdDt'], columns='count')
print xtb
#cnxn.close