from chromo import *
from gene import *
from timetable_generator_V6 import *

import unittest

class Algo_testing(unittest.TestCase) :

    def test_fitness_clash_batch(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Jaydeep",1,"Data structures","X","2nd_year",0)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",0)
        E = Gene(4,"Yash",2,"Data Science","X","2nd_year",0)

        Gene_list = [A,B,C,D,E]
        chrom = Chromosome(Gene_list,1,2,3)

        self.assertEqual(chrom.calcFitness([0,1,2,3,4,-1],Gene_list,3,2,1), -150.0)

    def test_fitness_clash_prof(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",1)
        C = Gene(2,"Jaydeep",1,"Data structures","X","2nd_year",2)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",0)
        E = Gene(4,"Yash",2,"Data Science","X","2nd_year",2)

        Gene_list = [A,B,C,D,E]
        chrom = Chromosome(Gene_list,1,2,3)

        self.assertEqual(chrom.calcFitness([0,2,1,3,4,-1],Gene_list,3,2,1), -100.0)

    def test_fitness_load(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",1)
        C = Gene(2,"Nishant",0,"Algorithm","X","2nd_year",2)

        Gene_list = [A,B,C]
        chrom = Chromosome(Gene_list,1,3,3)
        self.assertEqual(chrom.calcFitness([0,1,2,-1,-1,-1,-1,-1,-1],Gene_list,3,3,1), -1.0)

    def test_schedule(self) :

        cube,genes = timetable('DTT_Dataset_V2.csv')
        cover = np.zeros(len(genes))

        for i in cube:
            for j in i:
                for k in j:
                    if k != -1:
                        self.assertEqual(cover[k],0)
                        cover[k] = 1

        for i in cover:
            self.assertFalse(i == 0)

if __name__ == '__main__':
    unittest.main()
