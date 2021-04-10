import numpy as np
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
        for i in range(cube.shape[1]):
            for j in range(cube.shape[2]):
                prof = []
                batch = []
                for k in range(cube.shape[0]):
                    if cube[k, i, j] != -1:
                        if(genes[cube[k,i,j]].prof_id in prof) : 
                            fitness= fitness - 1
                        else : 
                            prof.append(genes[cube[k,i,j]].prof_id)

                        if(genes[cube[k,i,j]].batch_id in batch) : 
                            fitness= fitness - 1
                        else : 
                            batch.append(genes[cube[k,i,j]].batch_id)
        
        return fitness

    def mutate(self, rate):
        if np.random.random() < rate:
            i = 0
            j = 0
            while i == j:
                i = np.random.randint(0, self.timetable.shape[0])
                j = np.random.randint(0, self.timetable.shape[0])
            self.timetable = self.mut(self.timetable, i, j)

    def mut(self, timetable, i, j):
        temp = timetable[i]
        timetable[i] = timetable[j]
        timetable[j] = temp
        return timetable

    def crossover(self, chrom):
        i = 0
        j = 0
        while i == j:
            i = np.random.randint(0,self.timetable.shape[0] + 1)
            j = np.random.randint(0,self.timetable.shape[0] + 1)
        if i > j:
            j, i = i, j

        newTable = self.cross(self.timetable, chrom.timetable, i, j)
        newChrom = deepcopy(self)
        newChrom.timetable = newTable
        return newChrom

    def cross(self, table1, table2, i, j):
        newTable = table1.tolist()
        temp = table2[i:j]
        for k in temp:
            newTable.remove(k)
        newTable[i:i] = temp
        return np.array(newTable)

    def searchGene(self, id):
        for g in self.genes:
            if g.id == id:
                return g
