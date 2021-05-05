import numpy as np
import random
from copy import deepcopy
from .gene import *


class Chromosome:

    def __init__(self, genes, days, classesInDay, num_Batch):
        self.timetable = (-1) * np.ones((days *
                                         classesInDay * num_Batch), dtype=np.int32)
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
                        if(vis_prof[genes[slot].prof_id] == time_slot):
                            fitness = fitness - 1
                        else:
                            vis_prof[genes[slot].prof_id] = time_slot

                        if(vis_batch[genes[slot].batch_id] == time_slot):
                            fitness = fitness - 1
                        else:
                            vis_batch[genes[slot].batch_id] = time_slot

        fitness *= 50

        for j in range(noDays):

            prof_count = np.zeros(100)

            for i in range(noClassInDay):
                for k in range(num_Batch):
                    slot = timetable[k*noClassInDay*noDays + i*noDays + j]

                    if slot != -1:
                        prof_count[genes[slot].prof_id] += 1

            for k in prof_count:
                if k > 1:
                    fitness -= (k-2)*(k-2)

        return (fitness)

    def mutate(self, rate):
        return self.mutation(rate, self.timetable, self.genes, self.num_Batch, self.classesInDay, self.days)

    def mutate_load(self, rate):
        return self.mutation_load(rate, self.timetable, self.genes, self.num_Batch, self.classesInDay, self.days)

    def mutation(self, rate, timetable, genes, num_Batch, noClassInDay, noDays):

        # Instead of randomly assigning i and j, find the two which are clashing and then swap those two.
        vis_prof = -1 * np.ones(100)
        vis_batch = -1 * np.ones(num_Batch)

        s1 = -1
        s2 = -1

        for i in range(noClassInDay):
            for j in range(noDays):

                if s1 != -1 and s2 != -1:
                    break

                time_slot = i*noDays + j

                for k in range(num_Batch):

                    slot = timetable[k*noClassInDay*noDays + i*noDays + j]

                    if slot != -1:
                        if(vis_prof[genes[slot].prof_id] == time_slot or vis_batch[genes[slot].batch_id] == time_slot):

                            if s1 == -1:
                                s1 = slot
                            elif s2 == -1 and s1 != slot:
                                s2 = slot

                        vis_prof[genes[slot].prof_id] = time_slot
                        vis_batch[genes[slot].batch_id] = time_slot

        if s1 != -1 and s2 != -1 and np.random.uniform(0, 1) < rate:
            self.timetable = self.mut(self.timetable, s1, s2)

    def mutation_load(self, rate, timetable, genes, num_Batch, noClassInDay, noDays):

        s1 = s2 = -1
        # For each prof and batch, we want to know details of their lecture
        prof_slot = -1 * np.ones((100, noDays, noClassInDay), dtype=np.int32)
        batch_slot = -1 * \
            np.ones((num_Batch, noDays, noClassInDay), dtype=np.int32)
        prof_count = np.zeros((100, noDays), dtype=np.int32)

        for i in range(noClassInDay):
            for j in range(noDays):
                for k in range(num_Batch):

                    slot = timetable[k*noClassInDay*noDays + i*noDays + j]

                    if slot != -1:
                        prof_slot[genes[slot].prof_id][j][i] = slot
                        batch_slot[genes[slot].batch_id][j][i] = slot
                        prof_count[genes[slot].prof_id][j] += 1

        # Now we iterate over prof and day , try to rectify the load
        for i in range(100):
            for j in range(noDays):
                if prof_count[i][j] > 2:
                    for kk in range(noClassInDay):

                        if prof_slot[i][j][kk] != -1:
                            if np.random.uniform(0, 1) < rate:

                                id_to_swap = prof_slot[i][j][kk]
                                new_id = -1

                                for k in range(noDays):

                                    if new_id != -1:
                                        break

                                    if prof_count[i][k] < 2:

                                        for l in range(noClassInDay):

                                            # for this slot check if we can swap it with current slot
                                            if prof_slot[i][k][l] == -1:

                                                other_slot = batch_slot[genes[id_to_swap].batch_id][k][l]

                                                if other_slot == -1:
                                                    # We can change the timing of that prof,
                                                    # Because that prof has no lecture in this time
                                                    # The batch also has no lecture in this time

                                                    # Index 1 : find index of id_to_swap in timetabe
                                                    # Index 2 : find index of -1 in timetable for given day and time
                                                    s1 = np.where(
                                                        timetable == id_to_swap)[0]

                                                    for z in range(num_Batch):
                                                        temp = z*noClassInDay*noDays + l*noDays + k

                                                        if timetable[temp] == -1:
                                                            s2 = temp
                                                            break

                                                    self.timetable = self.mut(
                                                        self.timetable, s1, s2)
                                                    new_id = s2

                                                elif prof_slot[genes[other_slot].prof_id][j][kk] == -1:
                                                    # #We can change the timing of that prof,
                                                    # #Because that prof has no lecture in this time
                                                    # #The batch has a lecture, but the prof taking a lecture is comfortable
                                                    # #To swap it with other prof

                                                    # #Index 1 : find index of id_to_swap in timetable
                                                    # #Index 2 : find index of other_slot in timetable
                                                    # s1 =  np.where(timetable==id_to_swap)[0]
                                                    # s2 =  np.where(timetable==other_slot)[0]
                                                    # self.timetable = self.mut(self.timetable, s1, s2)
                                                    # new_id = s2
                                                    xx = 1

    def mut(self, timetable, i, j):
        temp = timetable[i]
        timetable[i] = timetable[j]
        timetable[j] = temp
        return timetable

    def crossover(self, chrom):
        return self.docrossover(chrom, self.genes, self.num_Batch, self.classesInDay, self.days)

    def docrossover(self, chrom, genes, num_Batch, noClassInDay, noDays):

        newTable = (-1) * np.ones((noDays * noClassInDay *
                                   num_Batch), dtype=np.int32)
        selected_slot = np.zeros(
            (noDays * noClassInDay * num_Batch), dtype=np.int32)

        # Selection without creating clash
        vis_prof = -1 * np.ones(100)
        vis_batch = -1 * np.ones(num_Batch)

        for i in range(noClassInDay):
            for j in range(noDays):

                time_slot = i*noDays + j

                for k in range(num_Batch):

                    pos = (k*noClassInDay*noDays) + (i*noDays) + j

                    slot_1 = self.timetable[pos]
                    slot_2 = chrom.timetable[pos]

                    if slot_1 != -1 and vis_prof[genes[slot_1].prof_id] != time_slot and vis_batch[genes[slot_1].batch_id] != time_slot and selected_slot[genes[slot_1].slot_id] == 0:

                        newTable[pos] = genes[slot_1].slot_id
                        selected_slot[genes[slot_1].slot_id] = 1

                        vis_prof[genes[slot_1].prof_id] = time_slot
                        vis_batch[genes[slot_1].batch_id] = time_slot

                    elif slot_2 != -1 and vis_prof[genes[slot_2].prof_id] != time_slot and vis_batch[genes[slot_2].batch_id] != time_slot and selected_slot[genes[slot_2].slot_id] == 0:

                        newTable[pos] = genes[slot_2].slot_id
                        selected_slot[genes[slot_2].slot_id] = 1

                        vis_prof[genes[slot_2].prof_id] = time_slot
                        vis_batch[genes[slot_2].batch_id] = time_slot

        # Find empty slots in current time table & shuffle
        empty_slots = []

        for i in range(noDays * noClassInDay*num_Batch):
            if newTable[i] == -1:
                empty_slots.append(i)

        random.shuffle(empty_slots)

        # Fill the non-selected lectures in these empty slots
        ptr = 0

        for gene in genes:
            if selected_slot[gene.slot_id] == 0:
                newTable[empty_slots[ptr]] = gene.slot_id
                ptr = ptr + 1

        newChrome = deepcopy(self)
        newChrome.timetable = newTable
        return newChrome

    def searchGene(self, id):
        for g in self.genes:
            if g.slot_id == id:
                return g

    def toStudentsTimetableHtml(self):
        flat = self.timetable.reshape(
            (self.num_Batch, self.classesInDay, self.days))
        tables = {}
        for k in range(self.num_Batch):
            for i in range(flat.shape[1]):
                for j in range(flat.shape[2]):
                    geneId = int(flat[k, i, j])
                    if geneId != -1:
                        gene = self.searchGene(geneId)
                        s = gene.toStudentString()
                        if s not in tables.keys():
                            tables[s] = -np.ones((self.classesInDay,
                                                 self.days), dtype=np.int32)
                        if(tables[s][i, j] != -1):
                            print("Error ", i, j, gene.subject, self.searchGene(
                                abs(tables[s][i, j])).subject)
                            tables[s][i, j] = -gene.slot_id
                        else:
                            tables[s][i, j] = gene.slot_id

        t = ""
        for key in tables.keys():
            h = "<h3 class='title'>{0}</h3>".format(key)
            table = tables[key].reshape((self.classesInDay, self.days))
            stable = "<table class='table table-bordered'>"
            for i in range(table.shape[0]):
                tr = "<tr>"
                for j in range(table.shape[1]):
                    geneId = table[i, j]
                    if geneId == -1:
                        td = "<td class='no'>Free Slot</td>"
                    elif geneId < -1:
                        td = "<td class='bg-danger'><span class='course'>{0}</span><hr><span class='teacher'>{1}</span></td>".format(
                            self.genes[-geneId].subject, self.genes[-geneId].prof_name)
                    else:
                        td = "<td><span class='course'>{0}</span><hr><span class='teacher'>{1}</span></td>".format(
                            self.genes[geneId].subject, self.genes[geneId].prof_name)
                    tr += td
                tr += '</tr>'
                stable += tr
            stable += "</table>"
            t += h + stable

        temp = self.template()
        t = temp.replace("{{timetable}}", t)
        file = open("student_schedule.html", mode="w")
        file.write(t)
        file.close()

    def toTeacherTimetableHtml(self):
        flat = self.timetable.reshape(
            (self.num_Batch, self.classesInDay, self.days))
        tables = {}
        for k in range(self.num_Batch):
            for i in range(flat.shape[1]):
                for j in range(flat.shape[2]):
                    geneId = int(flat[k, i, j])
                    if geneId != -1:
                        gene = self.searchGene(geneId)
                        s = gene.prof_name
                        if s not in tables.keys():
                            tables[s] = -np.ones((self.classesInDay,
                                                 self.days), dtype=np.int32)
                        if(tables[s][i, j] != -1):
                            print("Error ", i, j, gene.subject, self.searchGene(
                                abs(tables[s][i, j])).subject)
                            tables[s][i, j] = -gene.slot_id
                        else:
                            tables[s][i, j] = gene.slot_id

        t = ""
        for key in tables.keys():
            h = "<h3 class='title'>{0}</h3>".format(key)
            table = tables[key].reshape((self.classesInDay, self.days))
            stable = "<table class='table table-bordered'>"
            for i in range(table.shape[0]):
                tr = "<tr>"
                for j in range(table.shape[1]):
                    geneId = table[i, j]
                    if geneId == -1:
                        td = "<td class='no'>Free Slot</td>"
                    elif geneId < -1:
                        td = "<td class='bg-danger'><span class='course'>{0}</span><hr><span class='teacher'>{1}</span></td>".format(
                            self.genes[-geneId].subject, self.genes[-geneId].prof_name)
                    else:
                        td = "<td><span class='course'>{0}</span><hr><span class='teacher'>{1}</span></td>".format(
                            self.genes[geneId].subject, self.genes[geneId].prof_name)
                    tr += td
                tr += '</tr>'
                stable += tr
            stable += "</table>"
            t += h + stable

        temp = self.template()
        t = temp.replace("{{timetable}}", t)
        file = open("teacher_schedule.html", mode="w")
        file.write(t)
        file.close()

    def template(self):
        return """
                <html>
                <head>
                    <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
                    <script src="js/bootstrap.min..js"></script>
                    <link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100&display=swap" rel="stylesheet">
                    <link rel="preconnect" href="https://fonts.gstatic.com">
<link href="https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300&display=swap" rel="stylesheet">
                </head>
                <body>
                <style>
                    *{
                        font-family: 'Roboto Slab', serif;
                    }
                    .title, table td{
                        text-align: center;
                    }
                    .title {
                        font-size: 24px;
                        font-family: cursive;
                        color: black;
                    }
                    table td{
                        height: 100px;
                        width: 200px;
                        padding: 30 10 30 10;
                        background-color: #e2eab4;
                    }
                    .teacher, .course{
                        display: block;
                    }
                    .no{
                        color: #965008;
                    }
                    .teacher{
                        font-weight: bold;
                        color: blue;
                    }
                    .course{
                        color: red;
                        font-size: 16px;
                    }
                    tr hr{
                        color: #fefefe;
                        padding-top: 5px;
                        padding-bottom: 5px;
                    }
                </style>
                    <div class = 'container'>{{timetable}}</div>
                </body>
                </html>
            """
