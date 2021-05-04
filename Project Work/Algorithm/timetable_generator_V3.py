from chromo import Chromosome
from models import *
from copy import deepcopy
import numpy as np
import pandas as pd
import sys, getopt

class GA:
    
    def __init__(self, popSize,genes, num_Batch, days, classesInDay):
        self.chroms = [Chromosome(genes, days, classesInDay, num_Batch) for x in range(popSize)]
        self.genes = genes
       
    def calcFitness(self):
        fitnesses = []
        for c in self.chroms:
            fitnesses.append(c.fitness())
        return np.array(fitnesses)
    
    def mutate(self, rate):
        for c in self.chroms:
            c.mutate(rate)
    
    def selection(self, iteration=1, mutationRate=0.1, group=4, parentToChildRatio=.5):
        fitnesses = self.calcFitness()
        best = self.chroms[0]
        maxFitness = fitnesses[0]
        noParents = int(parentToChildRatio * len(self.chroms))
        noChildren = len(self.chroms) - noParents
        x = []
        for j in range(iteration):
            fitnesses = self.calcFitness()
            argsorted = fitnesses.argsort()
            x.append(fitnesses[argsorted[-1]])
            if fitnesses[argsorted[-1]] > maxFitness:
                maxFitness = fitnesses[argsorted[-1]]
                best = deepcopy(self.chroms[argsorted[-1]])
            print("Generation: {0}, Fitness: {1} , Total Fitness : {2} ".format(j, maxFitness , sum(fitnesses)))
            
            randParents = np.random.randint(0, len(self.chroms), (noChildren, group))
            newChroms = []

            for i in range(1, noParents + 1):
                newChroms.append(self.chroms[argsorted[-i]])

            for ip in range(noChildren):
                ps = randParents[ip]
                fourFitness = []
                for i in ps:
                    fourFitness.append(self.chroms[i].fitness())
                fourFitness = np.array(fourFitness)
                argFourSort = fourFitness.argsort()
                p1 = self.chroms[ps[argFourSort[-1]]]
                p2 = self.chroms[ps[argFourSort[-2]]]
                child = p1.crossover(p2)
                newChroms.append(child)

            self.chroms = newChroms
            self.mutate(mutationRate)
        return best

    def bestFit(self):
        fitnesses = self.calcFitness()
        argsorted = fitnesses.argsort()
        return self.chroms[argsorted[-1]]

p = 20
genes = load()
days = 6
classesInDay = 4
num_Batch = 24
ga = GA(p, genes, num_Batch, days, classesInDay)
best = ga.selection(iteration = 50, mutationRate = 0.2, group = 4, parentToChildRatio = 0.6)
cube = best.timetable.reshape((num_Batch, classesInDay, days))

for v in range(10) : 
    for i in range(cube.shape[1]) : 
        for j in range(cube.shape[2]) : 
            proff = []
            batch = []
            for k in range(cube.shape[0]) : 
                if(cube[k,i,j] != -1) : 
                    if(genes[cube[k,i,j]].prof_id in proff) : 
                        for ii in range(cube.shape[1]) : 
                            for jj in range(cube.shape[2]) : 
                                flag = 0
                                for kk in range(cube.shape[0]) : 
                                    if(cube[kk,ii,jj] != -1) : 
                                        if( (genes[cube[kk,ii,jj]].prof_id == genes[cube[k,i,j]].prof_id) or (genes[cube[kk,ii,jj]].batch_id == genes[cube[k,i,j]].batch_id)) : 
                                            flag = 1
                                            break
                                        if(flag == 1) : 
                                            break
                                if(flag == 0) : 
                                    for kk in range(cube.shape[0]) : 
                                        if(cube[kk,ii,jj] == -1) : 
                                            cube[kk,ii,jj] = cube[k,i,j]
                                            cube[k,i,j] = -1
                                            break
                                    break
                            if(flag == 0) : 
                                break
                    else : 
                        proff.append(genes[cube[k,i,j]].prof_id)


                if(cube[k,i,j] != -1) : 
                    if(genes[cube[k,i,j]].batch_id in batch) : 
                        for ii in range(cube.shape[1]) : 
                            for jj in range(cube.shape[2]) : 
                                flag = 0
                                for kk in range(cube.shape[0]) : 
                                    if(cube[kk,ii,jj] != -1) : 
                                        if( (genes[cube[kk,ii,jj]].prof_id == genes[cube[k,i,j]].prof_id) or (genes[cube[kk,ii,jj]].batch_id == genes[cube[k,i,j]].batch_id)) : 
                                            flag = 1
                                            break
                                        if(flag == 1) : 
                                            break
                                if(flag == 0) : 
                                    for kk in range(cube.shape[0]) : 
                                        if(cube[kk,ii,jj] == -1) : 
                                            cube[kk,ii,jj] = cube[k,i,j]
                                            cube[k,i,j] = -1
                                            break
                                    break
                            if(flag == 0) : 
                                break
                    else : 
                        batch.append(genes[cube[k,i,j]].batch_id)

best.timetable = cube
print("Final fitnees is : ",best.fitness())

stri = ["EL","EC","CS","ME"]

for s in stri : 
    for i in range(1,7) : 
        sq = []
        for k in range(classesInDay) :
            sq.append([])
            for m in range(days) : 
                sq[k].append("-1")
        
        batch_id = s+str(i)
        for ii in range(cube.shape[1]) : 
            for jj in range(cube.shape[2]) : 
                for kk in range(cube.shape[0]) : 
                    if(cube[kk,ii,jj] != -1) : 
                        if(genes[cube[kk,ii,jj]].batch == batch_id) : 
                            sq[ii][jj] = str(genes[cube[kk,ii,jj]].prof_name) + ' ,' + genes[cube[kk,ii,jj]].subject
                           # print(sq[ii][jj])

        df = pd.DataFrame(data=sq)
        df.to_csv(batch_id+".csv")

#print(cube)
