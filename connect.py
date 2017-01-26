import pyodbc
cnxn = pyodbc.connect("DRIVER={ODBC Driver 13 for SQL Server};"
                      "SERVER=DAWEB1;" 
                      "DATABASE=JustWare;"
                      "Trusted_Connection=yes")
