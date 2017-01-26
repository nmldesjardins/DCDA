# Run connect.py first to open db connection


import pandas as pd
# get number of cases for each person
# filters for tests cases, unknowns

call = ('SELECT tblNameActual.FullName, tblNameActual.NameID,' 
        ' COUNT(tblCaseActual.CaseID) as cases' 
        ' FROM tblNameActual'
        ' JOIN tblCaseActual'
        ' ON tblCaseActual.NameID = tblNameActual.NameID'
        ' WHERE tblNameActual.NameID > 541' 
        " AND tblNameActual.FullName != 'Mickey Mouse'"
        " AND tblNameActual.FullName NOT LIKE '%UNKNOWN%'"
        " AND tblNameActual.FullName != 'NO DEFENDANT'"
        " AND tblNameActual.FullName != 'EXPUNGED'"
        ' Group BY tblNameActual.FullName, tblNameActual.NameID'
        ' ORDER BY cases')


ncases = pd.read_sql(call,cnxn)
print ncases.head()

#cnxn.close()