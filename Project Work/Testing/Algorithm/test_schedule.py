from chromo import *
from gene import *
from timetable_generator_V7 import *
from loader import *

import unittest

class Schedule_testing(unittest.TestCase) :

    def test_schedule(self) :

        cube,genes = timetable('DTT_Dataset_Final.csv')
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