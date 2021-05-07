import pandas as pd
from gene import *

def load(s) :
    df = pd.read_csv(s)

    Prof_ID = df[['ID of Prof.']].values
    Subject = []
    for i in range(len(Prof_ID)) : 
        Subject.append(str(df['Subject ID'].values[i]).split(','))

    New_Prof_ID = []
    for i in range(len(Prof_ID)) : 
        for j in range(len(Subject[i])) : 
            New_Prof_ID.append(Prof_ID[i][0])
            
    Name = df[['Name of Prof.']].values
    New_Name = []
    for i in range(len(Name)) : 
        for j in range(len(Subject[i])) : 
            New_Name.append(Name[i][0])

    Sub_ID = df[['Subject ID']].values
    New_Sub_ID = []
    for i in range(len(Sub_ID)) : 
        STR = str(df['Subject ID'].values[i]).split(',')
        for j in range(len(Subject[i])) : 
            New_Sub_ID.append(STR[j])

    Batch_ID = df[['Batch']].values
    New_Batch_ID = []
    for i in range(len(Batch_ID)) : 
        STR = str(df['Batch'].values[i]).split(',')
        for j in range(len(Subject[i])) : 
            New_Batch_ID.append(STR[j])

    Num_lecture = df[['No. of lecture']].values
    New_Num_lecture = []
    for i in range(len(Num_lecture)) : 
        STR = str(df['No. of lecture'].values[i]).split(',')
        for j in range(len(Subject[i])) : 
            New_Num_lecture.append(STR[j])

    Sub = df[['Subject']].values
    New_Sub = []
    for i in range(len(Num_lecture)) : 
        STR = str(df['Subject'].values[i]).split(',')
        for j in range(len(Subject[i])) : 
            New_Sub.append(STR[j])
            
    df2 = pd.DataFrame(columns=['ID of Prof.','Name of Prof.','Subject','Subject ID','Batch','No. of lecture'])
    df2['ID of Prof.'] = New_Prof_ID
    df2['Name of Prof.'] = New_Name
    df2['Subject'] = New_Sub
    df2['Subject ID'] = New_Sub_ID
    df2['Batch'] = New_Batch_ID
    df2['No. of lecture'] = New_Num_lecture

    arr = df2[['ID of Prof.','Name of Prof.','Subject','Subject ID','Batch']].values
    data_list = []
    t=0
    for i in range(len(arr)) : 
        temp = [t]
        t=t+1
        for j in range(len(arr[i])) : 
            temp.append(arr[i][j])
        data_list.append(temp)
            
    nol = df2['No. of lecture'].values
    da = []
    for i in range(len(nol)) : 
        for j in range(int(nol[i])) : 
            da.append(data_list[i])

    my_df = pd.DataFrame(data=da, columns=['Slot ID','ID of Prof.','Name of Prof.','Subject','Subject ID','Batch'])

    t=0
    slot_id = []
    for i in range(len(my_df)) : 
        slot_id.append(t)
        t=t+1
    
    my_df['Slot ID'] = slot_id

    disc = {}
    B = my_df['Batch'].values
    BID = []
    t=0
    for i in range(len(B)) : 
        if(B[i] in disc.keys()) : 
            BID.append(disc[B[i]])
            
        else : 
            disc[B[i]] = t
            t=t+1
            BID.append(disc[B[i]])
            
    my_df['Batch ID'] = BID

    my_data = my_df[['Slot ID','ID of Prof.','Name of Prof.','Subject','Subject ID','Batch','Batch ID']].values
    genes = []
    for i in range(len(my_data)) : 
        g = Gene(my_data[i][0],my_data[i][2],my_data[i][1],my_data[i][3],my_data[i][4],my_data[i][5],my_data[i][6])
        genes.append(g)
        #genes[i].display()

    return genes

