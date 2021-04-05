import pandas as pd
import numpy as np
import random
df = pd.read_csv("DTT_Dataset_V2.csv")
ID = df[['ID of Prof.']].values

Subject = []
for i in range(len(ID)) : 
    Subject.append(str(df['Subject ID'].values[i]).split(','))

New_ID = []
for i in range(len(ID)) : 
    for j in range(len(Subject[i])) : 
        New_ID.append(ID[i][0])

Name = df[['Name of Prof.']].values
New_Name = []
for i in range(len(Name)) : 
    for j in range(len(Subject[i])) : 
        New_Name.append(Name[i][0])

SID = df[['Subject ID']].values
New_SID = []
for i in range(len(SID)) : 
    STR = str(df['Subject ID'].values[i]).split(',')
    for j in range(len(Subject[i])) : 
        New_SID.append(STR[j])
        
BID = df[['Batch']].values
New_BID = []
for i in range(len(BID)) : 
    STR = str(df['Batch'].values[i]).split(',')
    for j in range(len(Subject[i])) : 
        New_BID.append(STR[j])
        
N = df[['No. of lecture']].values
New_N = []
for i in range(len(N)) : 
    STR = str(df['No. of lecture'].values[i]).split(',')
    for j in range(len(Subject[i])) : 
        New_N.append(STR[j])

Sub = df[['Subject']].values
New_Sub = []
for i in range(len(N)) : 
    STR = str(df['Subject'].values[i]).split(',')
    for j in range(len(Subject[i])) : 
        New_Sub.append(STR[j])
        
df2 = pd.DataFrame(columns=['ID of Prof.','Name of Prof.','Subject','Subject ID','Batch','No. of lecture'])
df2['ID of Prof.'] = New_ID
df2['Name of Prof.'] = New_Name
df2['Subject'] = New_Sub
df2['Subject ID'] = New_SID
df2['Batch'] = New_BID
df2['No. of lecture'] = New_N

df2.to_csv('DTT_Dataset_final.csv',index = False)