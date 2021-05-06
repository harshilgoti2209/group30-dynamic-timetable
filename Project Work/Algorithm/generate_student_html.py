import numpy as np
import random
from copy import deepcopy
from gene import *

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
