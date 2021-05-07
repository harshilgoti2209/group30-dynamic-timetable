from chromo import *
from gene import *
from timetable_generator_V7 import *
from loader import *

import unittest

class Crossover_testing(unittest.TestCase) :

    def test_crossover_valid(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",1)
        C = Gene(2,"Jaydeep",1,"Data structures","X","2nd_year",2)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",0)
        E = Gene(4,"Yash",2,"Data Science","X","2nd_year",2)

        Gene_list = [A,B,C,D,E]
        chrom1 = Chromosome(Gene_list,1,2,3)
        chrom1.timetable = [0,2,1,3,4,-1]

        chrom2 = deepcopy(chrom1)
        chrom2.timetable = [1,2,3,4,0,-1]

        chrom3 = chrom1.crossover(chrom2)

        cover = np.zeros(len(Gene_list))

        for i in (chrom3.timetable) :
            if i != -1 :
                self.assertEqual(cover[i] , 0)
                cover[i] = 1

        for i in range(len(cover)) :
            self.assertEqual(cover[i] , 1)

    def test_crossover_clash(self) : 
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Jaydeep",1,"Algorithm","X","2nd_year",1)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",1)

        Gene_list = [A,B,C,D]
        chrom1 = Chromosome(Gene_list,1,2,2)
        chrom1.timetable = [0,1,2,3]

        chrom2 = Chromosome(Gene_list,1,2,2)
        chrom2.timetable = [0,2,1,3]

        chrom3 = chrom1.crossover(chrom2)

        self.assertLessEqual(chrom3.fitness(),max(chrom1.fitness(),chrom2.fitness())) 

    def test_crossover_noclash(self) : 
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Jaydeep",1,"Algorithm","X","2nd_year",1)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",1)

        Gene_list = [A,B,C,D]
        chrom1 = Chromosome(Gene_list,1,2,2)
        chrom1.timetable = [0,1,2,3] 

        chrom2 = Chromosome(Gene_list,1,2,2)
        chrom2.timetable = [3,2,1,0]

        chrom3 = chrom1.crossover(chrom2)

        self.assertEqual(chrom3.fitness(),0) 

if __name__ == '__main__':
    unittest.main()