'''
Unit tests for constructible
'''
import unittest

class TestCase(unittest.TestCase):
    ''' TestCase subclass with dummy subTest method 
    
    for Python version before 3.4
    '''
    if not hasattr(unittest.TestCase, 'subTest'):
        def subTest(self, **dummy):
            class subTest(object):
                def __enter__(self): pass
                def __exit__(self, *dummy): pass
            return subTest()


class TestHelperFunctions(TestCase):
    def test_isqrt(self):
        ''' test the isqrt function '''
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
        ''' test the fsqrt function '''
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


class TestArithmeticOperators(TestCase):
    def test_rational_binop(self):
        ''' test binary operators on constructible 
        instances representing rationals '''
        from constructible import Constructible
        from fractions import Fraction as F
        from operator import add, mul, sub, truediv

        for op in (add, mul, sub, truediv):
            with self.subTest(op=op):
                for a, b in [(F(1, 2), F(5, 7)),
                             (F(-1, 2), F(12, 25)),
                             (F(4, 3), 7),
                             (17, F(7, 16))]:
                    result = op(Constructible(a), Constructible(b))
                    self.assertEqual(result.a, op(a, b))
                    self.assertFalse(result.b)
                    self.assertFalse(result.field)

    def test_rational_unop(self):
        ''' test unary operators on constructible instances 
        representing rationals '''
        from constructible import Constructible
        from fractions import Fraction as F
        from operator import pos, neg

        for op in (pos, neg):
            with self.subTest(op=op):
                for a in [F(1, 2), F(-1, 2), F(12, 25), F(4, 3), 7, 0, -10, F(0)]:
                    result = op(Constructible(a))
                    self.assertEqual(result.a, op(a))
                    self.assertFalse(result.b)
                    self.assertFalse(result.field)

    def test_mix_rational_binop(self):
        ''' test binary operators between constructible instances 
        representing rationals and Fraction instances'''
        from constructible import Constructible
        from fractions import Fraction as F
        from operator import add, mul, sub, truediv

        for op in (add, mul, sub, truediv):
            with self.subTest(op=op):
                for a, b in [(F(1, 2), F(5, 7)),
                             (F(-1, 2), F(12, 25)),
                             (F(4, 3), 7),
                             (17, F(7, 16))]:
                    result = op(Constructible(a), b)
                    self.assertEqual(result.a, op(a, b))
                    self.assertFalse(result.b)
                    self.assertFalse(result.field)

    def test_mix_rational_rbinop(self):
        ''' test binary operators between Fraction instances and 
        constructible instances representing rationals'''
        from constructible import Constructible
        from fractions import Fraction as F
        from operator import add, mul, sub, truediv

        for op in (add, mul, sub, truediv):
            with self.subTest(op=op):
                for a, b in [(F(1, 2), F(5, 7)),
                             (F(-1, 2), F(12, 25)),
                             (F(4, 3), 7),
                             (17, F(7, 16))]:
                    result = op(a, Constructible(b))
                    self.assertEqual(result.a, op(a, b))
                    self.assertFalse(result.b)
                    self.assertFalse(result.field)

class TestStrRepr(TestCase):
    def test_repr(self):
        from constructible import Constructible
        self.assertEqual(repr(Constructible(2)), 'Constructible(Fraction(2, 1), 0, ())')
        self.assertEqual(repr(Constructible(Constructible(2), Constructible(3), (Constructible(5), ()))),
                         'Constructible('
                         'Constructible(Fraction(2, 1), 0, ()), '
                         'Constructible(Fraction(3, 1), 0, ()), '
                         '(Constructible(Fraction(5, 1), 0, ()), ())'
                         ')')

    def test_str(self):
        from constructible import Constructible
        self.assertEqual(str(Constructible(2)), '2')
        self.assertEqual(str(Constructible(Constructible(2), Constructible(3), (Constructible(5), ()))),
                         '(2 + 3 * sqrt(5))')



if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()