# get demo, case, charge data (will be long by count)

import pandas as pd

call=("SELECT tblNameActual.*, tblCaseActual.CaseID,"
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

namescasescts = pd.read_sql(call,cnxn)

print namescasescts.head()
