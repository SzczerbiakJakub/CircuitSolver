#import unittest,

import pytest, calc

"""class TestCalc(unittest.TestCase):
    
    def test_ad_sth(self):
        result = calc.add_sth(20, 50)
        self.assertEqual(result, 70)

    def test_change_list(self):
        result = calc.change_list([1, 2, 3, 4, 5, 6, 7, 8], 3)
        self.assertEqual(result, [8, 1, 2, 3, 4, 5, 6, 7])"""


def test_answer():
    assert calc.add_sth(10, 5) == 15



