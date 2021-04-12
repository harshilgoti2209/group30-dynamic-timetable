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
                print("Generation: {0}, Fitness: {1}".format(j, maxFitness))

            randParents = np.random.randint(
                0, len(self.chroms), (noChildren, group))
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

p=20
genes = load()
days = 6
classesInDay = 5
num_Batch = 24
ga = GA(p, genes, num_Batch, days, classesInDay)
best = ga.selection(iteration=100, mutationRate=0.1, group=4, parentToChildRatio=0.5)
cube = best.timetable.reshape((num_Batch, classesInDay, days))
print(cube)
