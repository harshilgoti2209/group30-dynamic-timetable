import numpy as np
import random
from copy import deepcopy
from gene import *
import math

def calcFitness_With_Load(self, timetable, genes, num_Batch, noClassInDay, noDays):
    fitness = 0
    vis_prof = -1 * np.ones(100)
    vis_batch = -1 * np.ones(num_Batch)

    prof_load = 0
    mx_prof = 100
    prof_sch = np.zeros((mx_prof, noDays))

    student_load = 0
    mx_students = 100
    student_sch = np.zeros((mx_prof, noDays))

    for i in range(noClassInDay):
        for j in range(noDays):

            time_slot = i*noDays + j

            for k in range(num_Batch):

                slot = timetable[k*noClassInDay*noDays + i*noDays + j]

                if slot != -1:

                    prof_sch[genes[slot].prof_id][j] += 1

                    student_sch[genes[slot].batch_id][j] += 1

                    if(vis_prof[genes[slot].prof_id] == time_slot):
                        fitness = fitness - 1
                    else:
                        vis_prof[genes[slot].prof_id] = time_slot

                    if(vis_batch[genes[slot].batch_id] == time_slot):
                        fitness = fitness - 1
                    else:
                        vis_batch[genes[slot].batch_id] = time_slot

    for i in range(mx_prof):
        total = 0
        for j in range(noDays):
            total += prof_sch[i][j]
        l_val = math.floor(total / noDays)
        r_val = math.ceil(total / noDays)
        for j in range(noDays):
            if(prof_sch[i][j] < l_val):
                prof_load += l_val - prof_sch[i][j]
            elif (prof_sch[i][j] > r_val):
                prof_load += prof_sch[i][j] - r_val

    for i in range(mx_students):
        total = 0
        for j in range(noDays):
            total += student_sch[i][j]

        l_val = math.floor(total / noDays)
        r_val = math.ceil(total / noDays)
        for j in range(noDays):
            if(student_sch[i][j] < l_val):
                student_load += l_val - student_sch[i][j]
            elif (student_sch[i][j] > r_val):
                student_load += student_sch[i][j] - r_val

    c1 = 1
    c2 = 1
    new_fitness = (fitness * 2 * noDays * noClassInDay *
                   num_Batch) - (c1 * prof_load) - (c2 * student_load)
    return (new_fitness)
