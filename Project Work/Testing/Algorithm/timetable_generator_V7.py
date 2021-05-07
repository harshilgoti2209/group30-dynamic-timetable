from chromo import Chromosome	
from loader import *
from copy import deepcopy
import numpy as np
import pandas as pd
import sys
import getopt


class GA:

    def __init__(
        self,
        popSize,
        genes,
        num_Batch,
        days,
        classesInDay,
        ):
        self.chroms = [Chromosome(genes, days, classesInDay, num_Batch)
                       for x in range(popSize)]
        self.genes = genes

    def calcFitness(self):
        fitnesses = []
        for c in self.chroms:
            fitnesses.append(c.fitness())
        return np.array(fitnesses)

    def mutate(self, rate):
        for c in self.chroms:
            c.mutate(rate)

    def mutate_load(self, rate):
        for c in self.chroms:
            c.mutate_load(rate)

    def selection(
        self,
        iteration=1,
        mutationRate=0.1,
        group=4,
        parentToChildRatio=.5,
        ):
        fitnesses = self.calcFitness()
        best = self.chroms[0]
        maxFitness = fitnesses[0]
        noParents = int(parentToChildRatio * len(self.chroms))
        noChildren = len(self.chroms) - noParents

        phase_change = 0

        print ('Phase 1 : Satisfying Hard constraints : Clash avoidance')

        for j in range(iteration):

            fitnesses = self.calcFitness()

            if maxFitness == 0:
                break

            argsorted = fitnesses.argsort()

            if fitnesses[argsorted[-1]] > maxFitness:
                maxFitness = fitnesses[argsorted[-1]]
                best = deepcopy(self.chroms[argsorted[-1]])

            print ('Generation: {0}, Fitness: {1} , Total Fitness : {2} '.format(j,maxFitness, sum(fitnesses)))

            newChroms = []

            for i in range(1, noParents + 1):
                newChroms.append(self.chroms[argsorted[-i]])

            for ip in range(noChildren):
                ps = np.random.randint(0, len(self.chroms), group)
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

            if phase_change == 0 and sum(fitnesses) == maxFitness \
                * len(self.chroms):
                assert maxFitness < 500
                phase_change = 1
                print ('Phase 2 : Satisfying Soft constraints : Load Balancing')

            if phase_change == 0:
                self.mutate(mutationRate)
            else:
                self.mutate_load(mutationRate)

        return best

    def bestFit(self):
        fitnesses = self.calcFitness()
        argsorted = fitnesses.argsort()
        return self.chroms[argsorted[-1]]

def timetable(s):
    p = 10
    days = 6
    classesInDay = 4
    num_Batch = 24

    genes = load(s)
    ga = GA(p, genes, num_Batch, days, classesInDay)

    best = ga.selection(iteration=100, mutationRate=0.03, group=4,
                        parentToChildRatio=0.4)

    best.toStudentsTimetableHtml()
    best.toTeacherTimetableHtml()

    print ('Final fitnees is : ', best.fitness())
    cube = best.timetable.reshape((num_Batch, classesInDay, days))
    return (cube, genes)
