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
        cube = timetable.reshape((num_Batch, noClassInDay, noDays)) 

        vis_prof = -1 * np.ones(100)
        vis_batch = -1 * np.ones(num_Batch)

        for i in range(cube.shape[1]):
            for j in range(cube.shape[2]):
                
                time_slot = i*noDays + j

                for k in range(cube.shape[0]):
                    if cube[k, i, j] != -1:
                        if(vis_prof[genes[cube[k,i,j]].prof_id] == time_slot) :
                            fitness= fitness - 1
                        else : 
                            vis_prof[genes[cube[k,i,j]].prof_id] = time_slot

                        if(vis_batch[genes[cube[k,i,j]].batch_id] == time_slot) : 
                            fitness= fitness - 1
                        else : 
                            vis_batch[genes[cube[k,i,j]].batch_id] = time_slot
        
        return (fitness)

    def mutate(self, rate):
        if np.random.uniform(0,1) < rate:
            i = 0
            j = 0
            while i == j:
                i = np.random.randint(0, self.timetable.shape[0])
                j = np.random.randint(0, self.timetable.shape[0])
            self.timetable = self.mut(self.timetable, i, j)

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

                    elif slot_2 != -1 and vis_prof[genes[slot_1].prof_id] != time_slot and vis_batch[genes[slot_1].batch_id] != time_slot and selected_slot[genes[slot_1].slot_id] == 0 :
                        
                            newTable[pos] = genes[slot_1].slot_id
                            selected_slot[genes[slot_1].slot_id] = 1
    
                            vis_prof[genes[slot_1].prof_id] = time_slot
                            vis_batch[genes[slot_1].batch_id] = time_slot

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
