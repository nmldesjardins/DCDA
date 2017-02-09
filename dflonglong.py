from connect import cnxn
import pandas as pd

""" 
select and merge variables from db
create dflong: raw data from db
                long by condition(count(case(person))))
"""
call_all=("SELECT tblNameActual.NameID, tblNameActual.FullName, tblNameActual.DOB,"
      " tblNameActual.Race, tblNameActual.Sex, tblNameActual.DLState, tblNameActual.NameType,"
      " tblCaseActual.CaseID, tblCaseActual.RcvdDt, tblCaseActual.Status, tblCaseActual.StatusDt,"
      " Charges.CountID, Charges.StatuteID, Charges.StatuteCode, Charges.StatuteDesc,"
      " Charges.StatuteSeverityCode, Charges.StatuteSeverityDesc,"
      " Sentence.SentenceTypeDesc, Sentence.SentenceFromDesc, Sentence.Amount1, Sentence.Amount2,"
      " Sentence.SentenceNotes, Condition.EventType, Condition.Description,"
      " Judgement.dispocode, Judgement.dispodesc, Judgement.pleacode, Judgement.pleadesc"
      " FROM tblNameActual"
      " JOIN tblCaseActual"
      " ON tblNameActual.NameID = tblCaseActual.NameID"
      " LEFT JOIN Charges"
      " ON tblCaseActual.CaseID = Charges.CaseID"
      " LEFT JOIN Condition"
      " ON Charges.CountID = Condition.CountID"
      " LEFT JOIN Judgement"
      " ON Charges.CountID = Judgement.CountID"
      " LEFT JOIN Sentence"
      " ON Charges.CountID = Sentence.CountID"
      " WHERE tblNameActual.NameID > 541"
      " AND tblNameActual.NameID != 219443"
      " AND tblNameActual.NameID != 219998"
      " AND tblNameActual.NameID != 222460"
      " AND tblNameActual.NameID NOT LIKE '%test%'" 
      " AND tblNameActual.FullName != 'Mickey Mouse'"
      " AND tblNameActual.FullName NOT LIKE '%UNKNOWN%'"
      " AND tblNameActual.FullName != 'NO DEFENDANT'"
      " AND tblNameActual.FullName != 'EXPUNGED'"
      " AND tblCaseActual.RcvdDt >= '2013-01-01'")

dflong = pd.read_sql(call_all,cnxn)

cnxn.close()