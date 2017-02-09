"""
Build charge features
Later: Try w/ keywords, clustering
Now: Use statute chapter for broad category

"""
dfl = namescasescts
dfl.head()

len(dfl.StatuteDesc.unique()) #488
len(dfl.StatuteCode.unique()) #502

dfl.StatuteDesc[24] # get degree, crime, attempted
dfl.StatuteCode

#%%
dfl.StatuteCode.dtype
dfl.StatuteCodestr=dfl.Statute(dfl.StatuteCode)
list(dfl)
#%%

#def sp(row):
#    for row in dfl.StatuteCodestr.splitlines():
#        return row[:row.find(".")]

dfl['statCh'] = dfl['StatuteCode'].apply(lambda x: x.split('.')[0])

#dfl['statCh'] = dfl.StatuteCode.split('.')[0]

print dfl.StatuteCode.head()
print dfl.statCh.head()

#%%
len(dfl.statCh.unique())

# let's make a dictionary
chkeys = dfl.statCh.unique()
# weird ones:
#%%
print dfl.loc[dfl['statCh']=='33',['StatuteCode','StatuteDesc']]
print dfl.loc[dfl['statCh']=='163A',['StatuteCode','StatuteDesc']]
print dfl.loc[dfl['statCh']=='UCrJI',['StatuteCode','StatuteDesc']] #jury instructions
print dfl.loc[dfl['statCh']=='2016 c',['StatuteCode','StatuteDesc']] # marijuana posession after 2015
print dfl.loc[dfl['statCh']=='86A',['StatuteCode','StatuteDesc']] # mortgage fraud
print dfl.loc[dfl['statCh']=='BM91 2015 c',['StatuteCode','StatuteDesc']] # maijuana in public place after 2015
print dfl.loc[dfl['statCh']=='0',['StatuteCode','StatuteDesc']]

statDic = dict.fromkeys(chkeys)


#%%

# do better later. now, manual!
statDic['0'] = 'other'
statDic['UCrJI'] = 'jury instructions'
statDic['131'] = 'criminal forfeiture'
statDic['133'] = 'failure to appear'
statDic['161'] = 'conspiracy'
statDic['162'] = 'against state/public officer'
statDic['163'] = 'against persons'
statDic['163A'] = 'failure to report as sex offender'
statDic['164'] = 'offenses against property'
statDic['165'] = 'forgery'
statDic['166'] = 'weapon'
statDic['167'] = 'against general welfare and animals'
statDic['181'] = 'failure to report as sex offender'
statDic['2016 c'] = 'marijuana'
statDic['314'] = 'tax evasion'
statDic['33'] = 'contempt'
statDic['411'] = 'welfare fraud'
statDic['471'] = 'alcohol to intox/MIP'
statDic['475'] = 'meth/heroin possession and delivery'
statDic['476'] = 'deposit burning material on a highway or forest'
statDic['480'] = 'fireworks sale/possession'
statDic['496'] = 'wildlife violations'
statDic['497'] = 'fish and game licence violations'
statDic['498'] = 'hunting w artificial light'
statDic['609'] = 'maintaining dangerous dog'
statDic['701'] = 'contracting without license'
statDic['806'] = 'false info to police officer'
statDic['807'] = 'false info to police officer'
statDic['811'] = 'reckless driving/driving while suspended'
statDic['813'] = 'DUII'
statDic['819'] = 'stolen vehicle'
statDic['830'] = 'unlawfully abandoned boat'
statDic['86A'] = 'mortgage fraud'
statDic['BM91 2015 c'] = 'marijuana'


dfl['chargeCat'] = dfl['statCh'].map(statDic)
dfl.chargeCat.head()