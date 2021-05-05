class Gene : 
    def __init__ (self, slot_id, prof_name, prof_id, subject, subject_id, batch, batch_id) : 
        self.slot_id = slot_id
        self.prof_name = prof_name
        self.prof_id = prof_id
        self.subject = subject
        self.subject_id = subject_id
        self.batch = batch
        self.batch_id = batch_id
        
    def display(self) : 
        print(self.slot_id, self.prof_name, self.prof_id, self.subject, self.subject_id, self.batch, self.batch_id)

    def toStudentString(self):
        """
            Returns the string that represents the students who are taking course representing this gene
        """
        return "{0}th year, section {1}, {2} {3}".format(self.batch, self.batch_id, self.batch, self.batch_id)