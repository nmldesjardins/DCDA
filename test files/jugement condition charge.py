# merge charge - judgment - condition

call = ("SELECT * FROM Charges"
        " JOIN Judgement ON Charges.CountID = Judgement.CountID"
        " JOIN Condition ON Charges.CountID = Condition.CountID")
        
call = ("SELECT * FROM Charges"
        " JOIN Judgement ON Charges.CountID = Judgement.CountID"
        " JOIN Condition ON Charges.CountID = Condition.CountID")

cjc = pd.read_sql(call, cnxn)
cjc.head()
list(cjc)

# get rid of extra case ids

#cjc = cjc.T.drop_duplicates().T  - killed kernel
x = np.unique(cjc.columns, return_index=True)

# merge w/ case and demographic data
longdf = namescases.merge(cjc, on = 'CaseID')