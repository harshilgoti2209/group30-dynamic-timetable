import numpy as np
import random
from copy import deepcopy
from gene import *

class Chromosome:

    def __init__(self, genes, days, classesInDay, num_Batch):
        self.timetable = (-1) * np.ones((days * classesInDay * num_Batch), dtype=np.int32)
        self.genes = genes
        self.days = days
        self.classesInDay = classesInDay
        self.num_Batch = num_Batch
        for gene in genes:
            i = np.random.randint(0, self.timetable.shape[0])
            while self.timetable[i] != -1:
                i = np.random.randint(0, self.timetable.shape[0])
            self.timetable[i] = gene.slot_id

    def fitness(self):
        return self.calcFitness(self.timetable, self.genes, self.num_Batch, self.classesInDay, self.days)

    def calcFitness(self, timetable, genes, num_Batch, noClassInDay, noDays):
        fitness = 0
        vis_prof = -1 * np.ones(100)
        vis_batch = -1 * np.ones(num_Batch)

        for i in range(noClassInDay):
            for j in range(noDays):
                
                time_slot = i*noDays + j

                for k in range(num_Batch):

                    slot = timetable[k*noClassInDay*noDays + i*noDays + j]

                    if slot != -1:
                        if(vis_prof[genes[slot].prof_id] == time_slot) :
                            fitness= fitness - 1
                        else : 
                            vis_prof[genes[slot].prof_id] = time_slot

                        if(vis_batch[genes[slot].batch_id] == time_slot) : 
                            fitness= fitness - 1
                        else : 
                            vis_batch[genes[slot].batch_id] = time_slot
        
        return (fitness)

    def mutate(self,rate) :
        return self.mutation(rate,self.timetable, self.genes, self.num_Batch, self.classesInDay, self.days)

    def mutation(self, rate, timetable, genes, num_Batch, noClassInDay, noDays) : 

        if np.random.uniform(0,1) < rate:
            #Instead of randomly assigning i and j, find the two which are clashing and then swap those two.
            vis_prof = -1 * np.ones(100)
            vis_batch = -1 * np.ones(num_Batch)

            s1 = -1
            s2 = -1

            for i in range(noClassInDay):
                for j in range(noDays):

                    if s1 != -1 and s2 != -1 : 
                        break

                    time_slot = i*noDays + j

                    for k in range(num_Batch):

                        slot = timetable[k*noClassInDay*noDays + i*noDays + j]

                        if slot != -1 :
                            if(vis_prof[genes[slot].prof_id] == time_slot or vis_batch[genes[slot].batch_id] == time_slot) :

                                if s1 == -1 : 
                                    s1 = slot    
                                elif s2 == -1 and s1 != slot :
                                    s2 = slot

                            vis_prof[genes[slot].prof_id] = time_slot
                            vis_batch[genes[slot].batch_id] = time_slot
            
            if s1 != -1 and s2 != -1 :
                self.timetable = self.mut(self.timetable, s1, s2)

    def mut(self, timetable, i, j) :
        temp = timetable[i]
        timetable[i] = timetable[j]
        timetable[j] = temp
        return timetable
    
    def crossover(self,chrom) :
        return self.docrossover(chrom,self.genes,self.num_Batch,self.classesInDay,self.days)

    def docrossover(self, chrom, genes,num_Batch, noClassInDay, noDays) :
        
        newTable = (-1) * np.ones((noDays * noClassInDay * num_Batch), dtype = np.int32)
        selected_slot =  np.zeros((noDays * noClassInDay * num_Batch), dtype = np.int32)
        
        #Selection without creating clash
        vis_prof = -1 * np.ones(100)
        vis_batch = -1 * np.ones(num_Batch)

        for i in range(noClassInDay):
            for j in range(noDays):
                
                time_slot = i*noDays + j

                for k in range(num_Batch) :
                    
                    pos = (k*noClassInDay*noDays) + (i*noDays) + j

                    slot_1 = self.timetable[pos]
                    slot_2 = chrom.timetable[pos]

                    if slot_1 != -1 and vis_prof[genes[slot_1].prof_id] != time_slot and vis_batch[genes[slot_1].batch_id] != time_slot and selected_slot[genes[slot_1].slot_id] == 0 :
                        
                            newTable[pos] = genes[slot_1].slot_id
                            selected_slot[genes[slot_1].slot_id] = 1
    
                            vis_prof[genes[slot_1].prof_id] = time_slot
                            vis_batch[genes[slot_1].batch_id] = time_slot

                    elif slot_2 != -1 and vis_prof[genes[slot_2].prof_id] != time_slot and vis_batch[genes[slot_2].batch_id] != time_slot and selected_slot[genes[slot_2].slot_id] == 0 :
                        
                            newTable[pos] = genes[slot_2].slot_id
                            selected_slot[genes[slot_2].slot_id] = 1
    
                            vis_prof[genes[slot_2].prof_id] = time_slot
                            vis_batch[genes[slot_2].batch_id] = time_slot

        #Find empty slots in current time table & shuffle
        empty_slots = []

        for i in range(noDays* noClassInDay*num_Batch) : 
            if newTable[i] == -1 :
                empty_slots.append(i)

        random.shuffle(empty_slots)

        #Fill the non-selected lectures in these empty slots
        ptr = 0

        for gene in genes : 
            if selected_slot[gene.slot_id] == 0 :
                newTable[empty_slots[ptr]] = gene.slot_id
                ptr = ptr + 1

        newChrome = deepcopy(self)
        newChrome.timetable = newTable
        return newChrome

    def searchGene(self, id):
        for g in self.genes:
            if g.slot_id == id:
                return g
