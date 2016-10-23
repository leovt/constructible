# 
#    Copyright 2016 Leonhard Vogt
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#    
from __future__ import division

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


    if not hasattr(unittest.TestCase, 'assertIsInstance'):
        def assertIsInstance(self, obj, cls, msg=None):
            self.assertTrue(isinstance(obj, cls), msg=msg)
            

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

    def test_expressions_type(self):
        from constructible import sqrt, Constructible
        s = sqrt(2)
        self.assertIsInstance(s, Constructible)
        self.assertIsInstance(2 * s, Constructible)
        self.assertIsInstance(2 - s, Constructible)
        t = 3 - 2 * s
        self.assertIsInstance(t, Constructible)
        u = s - s
        self.assertIsInstance(u, Constructible)
        v = -t
        self.assertIsInstance(v, Constructible)


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

class TestComparison(TestCase):
    def test_rational_comparison(self):
        ''' test comparison operators on constructible 
        instances representing rationals '''
        from constructible import Constructible
        from operator import eq, ne, gt, lt, ge, le

        for op in (eq, ne, gt, lt, ge, le):
            with self.subTest(op=op):
                for a in [0, 1, -1]:
                    for b in [0, 1, -1]:
                        result = op(Constructible(a), Constructible(b))
                        self.assertEqual(result, op(a, b))
                        self.assertIsInstance(result, bool)

    def test_comparison_Qsqrt2(self):
        ''' test comparison operators on instances of Q[sqrt(2)] '''
        from constructible import sqrt
        from operator import eq, ne, gt, lt, ge, le

        s = sqrt(2)
        t = 3 - 2 * s
        u = s - s
        v = -t

        self.assertTrue(s.field == t.field == u.field == v.field, "Precondition")

        # numbers is sorted ascending, so the comarison of numbers and therir indices must be same
        numbers = [v, u, t, s]

        self.assertTrue(s.field == t.field == u.field == v.field, "Precondition")

        for op in (eq, ne, gt, lt, ge, le):
            with self.subTest(op=op):
                for i, a in enumerate(numbers):
                    for j, b in enumerate(numbers):
                        result = op(a, b)
                        self.assertEqual(result, op(i, j))
                        self.assertIsInstance(result, bool)


class TestSqrt(TestCase):
    def test_sqrt_2(self):
        from constructible import sqrt
        r = sqrt(2)
        self.assertEqual(r.a, 0)
        self.assertEqual(r.b, 1)
        self.assertEqual(len(r.field), 2)
        self.assertEqual(r.field[0], 2)
        self.assertEqual(str(r), 'sqrt(2)')
        self.assertTrue(r > 0)

    def test_double_sqrt(self):
        from constructible import sqrt
        r = sqrt(2)
        s = sqrt(r)
        self.assertEqual(str(s), 'sqrt(sqrt(2))')

    def test_sqrt23(self):
        from constructible import sqrt
        r = sqrt(2) + sqrt(3)
        self.assertTrue(r > 0)
        self.assertEqual(r*r*r*r - 10*r*r + 1, 0)

    def test_sqrt236(self):
        from constructible import sqrt
        r = sqrt(2) * sqrt(3)
        self.assertTrue(r > 0)
        self.assertEqual(r, sqrt(6))

    def test_sqrt623(self):
        from constructible import sqrt
        r = sqrt(6) / sqrt(3)
        self.assertTrue(r > 0)
        self.assertEqual(r, sqrt(2))

    def test_sqrt235(self):
        from constructible import sqrt
        r = sqrt(2) + sqrt(3) + sqrt(5)
        r2 = r*r
        r4 = r2*r2
        r6 = r2*r4
        r8 = r2*r6
        self.assertTrue(r > 0)
        self.assertEqual(r8 - 40*r6 + 352*r4 - 960*r2 + 576, 0)

    def test_sqrt_square(self):
        from constructible import sqrt
        r = sqrt(2) + sqrt(3) + sqrt(5)
        self.assertEqual(sqrt(r*r), r)
        

class TestTrySqrt(TestCase):
    def test_sqrt2(self):
        from constructible import sqrt
        r = sqrt(2)
        two = r*r
        self.assertEqual(two, 2)
        s = two._try_sqrt()
        self.assertEqual(r, s)
        
class TestHeptadekagon(TestCase):
    def test_roots(self):
        from constructible import sqrt
        r = sqrt(17)
        u = sqrt(2 * (17 - r))
        v = sqrt(2 * (17 + r))
        cos = (-1 + r + u + 2*sqrt(17 + 3*r - u - 2*v)) / 16
        sin = sqrt(1 - cos*cos)
        
        s_i = 0
        c_i = 1
        
        for i in range(17):
            s = sin * c_i + cos * s_i
            c = cos * c_i - sin * s_i
            self.assertEqual(s*s + c*c, 1, "radius not equal to 1 at i=%d" % i)
            s_i = s
            c_i = c
        
        self.assertEqual(s_i, 0)
        self.assertEqual(c_i, 1)
        

class TestHash(TestCase):
    '''
    Main requirement of the hash is that objects comparing equal 
    must have the same hash. 
    '''
    def test_rational(self):
        '''
        hash of rationals represented as Constructible must be equal to the
        hash of the original value.
        '''
        from constructible import Constructible
        from fractions import Fraction as F
        
        for x in [0,1,-1,F(0.25),F(0,1),F(1,2),F(-1,1)]:
            with self.subTest(x=x):
                y = Constructible(x)
                self.assertEqual(x,y, 'precondition for this test')
                self.assertEqual(hash(x), hash(y), 'hash(%s)' % (x,))
            
    def test_equal(self):
        '''
        hash of multiple representations of the same value must be equal
        '''
        from constructible import sqrt
        from fractions import Fraction as F
        
        for a,b in [(sqrt(2), 2/sqrt(2)),
                    (sqrt(2), 1/sqrt(F(1,2))),
                    (sqrt(2) + sqrt(3), sqrt(3) + sqrt(2))]:
            with self.subTest(a=a, b=b):
                self.assertEqual(a,b, 'precondition for this test')
                self.assertEqual(hash(a), hash(b), '%s == %s, but hash is different' % (a,b))
        

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
