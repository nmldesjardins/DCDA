"""
run connect.py first to open connectionto db
may want to come back and do this as a join w/ case and names
"""

import pandas as pd

counts = pd.read_sql("SELECT * FROM tblCountActual",cnxn)
print counts.head()

countatt = pd.read_sql("SELECT * FROM tblCountAttributes",cnxn)
print countatt.head()
#cnxn.close()