from chromo import *
from gene import *
from timetable_generator_V7 import *
from loader import *

import unittest

class Mutation_load_testing(unittest.TestCase) :

    def test_mutate_load_rate0(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Nishant",0,"Algorithm","X","2nd_year",0)

        Gene_list = [A,B,C]
        chrom1 = Chromosome(Gene_list,2,3,1)
        chrom1.timetable = [0,-1,1,-1,2,-1]

        chrom2 = deepcopy(chrom1)        
        chrom1.mutate_load(0)

        self.assertEqual(chrom1.fitness(),chrom2.fitness())

    def test_mutate_load_func(self) :
        A = Gene(0,"Nishant",0,"Algorithm","X","2nd_year",0)
        B = Gene(1,"Nishant",0,"Algorithm","X","2nd_year",0)
        C = Gene(2,"Nishant",0,"Algorithm","X","2nd_year",0)

        Gene_list = [A,B,C]
        chrom1 = Chromosome(Gene_list,2,3,1)
        chrom1.timetable = [0,-1,1,-1,2,-1]

        chrom2 = deepcopy(chrom1)        
        chrom1.mutate_load(1)

        self.assertGreater(chrom1.fitness(),chrom2.fitness())

if __name__ == '__main__':
    unittest.main()