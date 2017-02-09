def features(words, colname, df, origvar):
    """ takes a string or list of strings (words)
        if a list, separates entries with |
        searches for (words) in (origvar)
        creates a new binary variable with a name (colname)
        where 1 = (words) were present in (origvar)
    """
    if isinstance(words, list) == False:
        pat=words
    else:
        pat='|'.join(map(re.escape,words))
    df[colname]=df[origvar].str.contains(pat).astype(int) #01 instead of bool

def dict2feat(dic,origvar,df):
    """ runs features() on each entry of a dictionary
        new variable returned with corresponding dictionary key name
    """
    for key in dic:
        colname=key
        features(dic[key],colname,df,origvar)


def sentPenalty(dic,)
    names = []
    for key in dic:
        if 'T' in key:
            new = 'Time_'+ key
        if 'M' in key:
            new = 'Money_'+ key
        names.append(new)
x = sentDict.keys()    

def sentTerm(x, df, newvalT, newvalM):
    for lab in x:
        if 'T' in lab:
            newT = 'Time_'+lab
            df[newT] = np.where(df[lab]==1, dflong[newvalT], 0)
        
        if 'M' in lab:
            newM = 'Money'+lab
            df[newM] = np.where(df[lab]==1, dflong[newvalM], 0)


def recid (row):
    """ returns 1 if person has more than 1 case """
    if row['nCases'] >= 2:
        return 1
    return 0


def fcase (row):
    """ returns 1 if the date of the case is the earliest date for that person """
    if row['RcvdDt'] == row['firstCaseDt']:
        return 1
    return 0



def recid2 (row):
    """ returns 1 if person has more than 1 case """
    if row['totCaseConvict'] >= 2 :
        return 1
    return 0

