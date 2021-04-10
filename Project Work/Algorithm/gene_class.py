class Gene : 

  def __init__(self,id ,prof_name, prof_id , subject_name , subject_id , batch_name , batch_id) :
    self.id = id
    self.prof_id = prof_id
    self.subject_id = subject_id
    self.batch_id = batch_id
    self.prof_name = prof_name
    self.subject_name = subject_name
    self.batch_name = batch_name    

  def print(self) :
    s = """
            id: {0}
            prof_name: {1}
            prof_id: {2}
            subject_name: {3}
            subject_id: {4}
            batch_name : {5}
            batch_id : {6}
        """.format(self.id, self.prof_name ,self.prof_id, self.subject_name,self.subject_id,self.batch_name,self.batch_id)
    print(s)
