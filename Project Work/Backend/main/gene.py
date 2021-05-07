class Gene : 
    def __init__ (self, slot_id, prof_name, prof_id, subject, subject_id, batch, batch_id, email) : 
        self.slot_id = slot_id
        self.prof_name = prof_name
        self.prof_id = prof_id
        self.subject = subject
        self.subject_id = subject_id
        self.batch = batch
        self.batch_id = batch_id
        self.email = email
        
    def display(self) : 
        print(self.slot_id, self.prof_name, self.prof_id, self.subject, self.subject_id, self.batch, self.batch_id, self.email)
