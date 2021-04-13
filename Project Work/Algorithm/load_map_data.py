def load() : 

  df = pd.read_csv("DTT_Data.csv")
  df.columns

  genes = []

  prof_set = {}

  batch_set = {}

  for i in range(len(df)) : 

    subject_name = df['Subject'].values[i]
    subject_id = df['Subject ID'].values[i]
    
    prof_name = df['Name of Prof.'].values[i]
    
    prof_id = -1

    if prof_name in prof_set :
      prof_id = prof_set[prof_name]
    else :
      prof_id = len(prof_set)
      prof_set[prof_name] = prof_id

    batch_name = df['Batch'].values[i]
    batch_id = -1

    if batch_name in batch_set :
      batch_id = batch_set[batch_name]
    else :
      batch_id = len(batch_set)
      batch_set[batch_name] = batch_id

    lec_count = df['No. of lecture'].values[i]

    for i in range(lec_count) :
      g = Gene(len(genes), prof_name,prof_id, subject_name , subject_id , batch_name , batch_id)
      genes.append(g)

  return genes