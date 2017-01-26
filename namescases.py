"""
Run connect.py first to open db connection
Gets all demographic and case info
"""
import pandas as pd

call=("SELECT * FROM tblNameActual"
      " JOIN tblCaseActual"
      " ON tblNameActual.NameID = tblCaseActual.NameID"
      " WHERE tblNameActual.NameID > 541"
      " AND tblNameActual.FullName != 'Mickey Mouse'"
      " AND tblNameActual.FullName NOT LIKE '%UNKNOWN%'"
      " AND tblNameActual.FullName != 'NO DEFENDANT'"
      " AND tblNameActual.FullName != 'EXPUNGED'")

namescases = pd.read_sql(call,cnxn)

print namescases.head()

cnxn.close