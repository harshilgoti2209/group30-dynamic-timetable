import pandas as pd
import numpy as np
import random
df = pd.read_csv("DTT_Dataset_V1.csv")
ID=df[['Subject ID']]

BID = []
for i in range(66) : 
    BIDs = []
    IDs = str(df['Subject ID'].values[i]).split(',')
    for j in range(len(IDs)) : 
        BIDs.append(IDs[j][2:5]) 
        
    BID.append(BIDs)

SBID = []
for i in range(len(BID)) : 
    STR = ""
    for j in range(len(BID[i])) : 
        STR = STR + BID[i][j]
        if(j!=len(BID[i])-1) : 
            STR = STR + ","
    SBID.append(STR)
    
df['Batch']=SBID

lec = [2,3]
N = []
for i in range(66) : 
    Ns = []
    IDs = str(df['Subject ID'].values[i]).split(',')
    for j in range(len(IDs)) : 
        Ns.append(np.random.choice(lec, p=[0.2,0.8]))
        
    N.append(Ns)

SN = []
for i in range(len(BID)) : 
    STR = ""
    for j in range(len(N[i])) : 
        STR = STR + str(N[i][j])
        if(j!=len(N[i])-1) : 
            STR = STR + ","
    SN.append(STR)

df['No. of lecture']=SN

df.to_csv('DTT_Dataset_V2.csv',index = False)