from chromo import *
from gene import *
from timetable_generator_V7 import *
from loader import *

import unittest

class Mutation_clash_testing(unittest.TestCase) :

    def test_mutation_rate0(self) : 
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Jaydeep",1,"Algorithm","X","2nd_year",1)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",1)

        Gene_list = [A,B,C,D]
        chrom1 = Chromosome(Gene_list,1,2,2)
        chrom1.timetable = [0,2,1,3]
        chrom2 = deepcopy(chrom1)
        chrom1.mutate(0)

        self.assertEqual(chrom1.timetable , chrom2.timetable)

    def test_mutation_rate1(self) : 
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Jaydeep",1,"Algorithm","X","2nd_year",1)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",1)

        Gene_list = [A,B,C,D]
        chrom1 = Chromosome(Gene_list,1,2,2)
        chrom1.timetable = [0,2,1,3]
        chrom2 = deepcopy(chrom1)
        chrom1.mutate(1)

        self.assertNotEqual(chrom1.timetable , chrom2.timetable)

    def test_mutation_func(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",1)
        C = Gene(2,"Jaydeep",1,"Algorithm","X","2nd_year",0)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",1)

        Gene_list = [A,B,C,D]
        chrom1 = Chromosome(Gene_list,2,1,2)
        chrom1.timetable = [0,1,2,3] 
        chrom2 = deepcopy(chrom1)
        chrom1.mutate(1)

        self.assertGreater(chrom1.fitness(),chrom2.fitness  ())

if __name__ == '__main__':
    unittest.main()