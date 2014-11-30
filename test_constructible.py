'''
Unit tests for constructible
'''
import unittest


class TestHelperFunctions(unittest.TestCase):


    def test_isqrt(self):
        from constructible import isqrt
        from functools import partial

        self.assertEqual(isqrt(0), (0, 1))
        self.assertEqual(isqrt(1), (1, 1))
        self.assertEqual(isqrt(2), (1, 2))
        self.assertEqual(isqrt(4), (2, 1))
        self.assertEqual(isqrt(120), (2, 30))
        self.assertRaises(ValueError, partial(isqrt, -1))
        self.assertRaises(ValueError, partial(isqrt, -12))
        self.assertEqual(isqrt(16), (4, 1))
        self.assertEqual(isqrt(3 ** 4 * 5 ** 6), (9 * 125, 1))

    def test_fsqrt(self):
        from constructible import fsqrt
        from functools import partial
        from fractions import Fraction

        self.assertEqual(fsqrt(0), (0, 1))
        self.assertEqual(fsqrt(1), (1, 1))
        self.assertEqual(fsqrt(2), (1, 2))
        self.assertEqual(fsqrt(4), (2, 1))
        self.assertEqual(fsqrt(120), (2, 30))
        self.assertRaises(ValueError, partial(fsqrt, -1))
        self.assertRaises(ValueError, partial(fsqrt, -12))
        self.assertEqual(fsqrt(16), (4, 1))
        self.assertEqual(fsqrt(3 ** 4 * 5 ** 6), (9 * 125, 1))

        self.assertEqual(fsqrt(Fraction(3, 4)), (Fraction(1, 2), 3))
        self.assertEqual(fsqrt(Fraction(9, 25)), (Fraction(3, 5), 1))
        self.assertEqual(fsqrt(Fraction(9, 50)), (Fraction(3, 10), 2))
        self.assertEqual(fsqrt(Fraction(9, 75)), (Fraction(1, 5), 3))





if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
