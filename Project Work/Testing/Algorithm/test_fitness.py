from chromo import *
from gene import *
from timetable_generator_V7 import *
from loader import *

import unittest

class Fitness_test(unittest.TestCase) :

    def test_fitness_clash_batch(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Jaydeep",1,"Data structures","X","2nd_year",0)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",0)
        E = Gene(4,"Yash",2,"Data Science","X","2nd_year",0)

        Gene_list = [A,B,C,D,E]
        chrom = Chromosome(Gene_list,1,2,3)
        chrom.timetable = [0,1,2,3,4,-1]

        self.assertEqual(chrom.fitness(), -150.0)

    def test_fitness_clash_prof(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",1)
        C = Gene(2,"Jaydeep",1,"Data structures","X","2nd_year",2)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",0)
        E = Gene(4,"Yash",2,"Data Science","X","2nd_year",2)

        Gene_list = [A,B,C,D,E]
        chrom = Chromosome(Gene_list,1,2,3)
        chrom.timetable = [0,2,1,3,4,-1]

        self.assertEqual(chrom.fitness(), -100.0)

    def test_fitness_load(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",1)
        C = Gene(2,"Nishant",0,"Algorithm","X","2nd_year",2)

        Gene_list = [A,B,C]
        chrom = Chromosome(Gene_list,1,3,3)
        chrom.timetable = [0,1,2,-1,-1,-1,-1,-1,-1]

        self.assertEqual(chrom.fitness(), -1.0)

    def test_fitness_mix_cases(self) : 
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Nishant",0,"Algorithm","X","2nd_year",0)
        D = Gene(3,"Jaydeep",1,"Data structures","X","2nd_year",0)

        Gene_list = [A,B,C,D]
        chrom = Chromosome(Gene_list,1,2,3)
        chrom.timetable = [0,1,2,3,-1,-1]

        self.assertEqual(chrom.fitness(), -151.0)

    def test_fitness_zero(self) : 
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)

        Gene_list = [A,B]
        chrom = Chromosome(Gene_list,2,1,1)
        chrom.timetable = [0,1]

        self.assertEqual(chrom.fitness(), 0.0)

if __name__ == '__main__':
    unittest.main()