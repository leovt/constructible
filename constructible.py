# coding:utf-8
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
import math


'''
Representing constructible numbers

Author: Leonhard Vogt
'''

from fractions import Fraction
from numbers import Rational

# increments of prime divisor candidates after 7, giving 73% skip
_divisor_incs = (4,  2,  4,  2,  4,  6,  2,  6)
#               11, 13, 17, 19, 23, 29, 31, 37 (mod 30)
# here to avoid reevaluation each time `isqrt` is called

def _divisors():
    yield 2
    yield 3
    yield 5
    k = 7
    while True:
        for k_inc in _divisor_incs:
            yield k
            k += k_inc

def isqrt(n):
    ''' given a non-negative integer n, return a pair (a,b) such that n = a * a * b
        where b is a square-free integer.

        If n is a perfect square, then a is its square root and b is one.
    '''
    # TODO: replace with a more efficient implementation

    if n == 0:
        return n, 1
    if n < 0:
        raise ValueError('math domain error')

    precomp = _isqrt_precomputed.get(n)
    if precomp:
        return precomp

    a, b, c = 1, n, 1

    for k in _divisors():
        k_sqr = k * k
        if k_sqr > b:
            break

        while True:
            d, m = divmod(b, k_sqr)
            if m != 0:
                break
            a *= k
            b = d

        d, m = divmod(b, k)
        if m == 0:
            b = d
            c *= k

        precomp = _isqrt_precomputed.get(b)
        if precomp:
            a_, b_ = precomp
            return a * a_, c * b_

    return a, b * c

_isqrt_precomputed = dict() # should be defined before calling `isqrt`
_isqrt_precomputed = {n: isqrt(n) for n in range(1, 1 + 100)}

def fsqrt(q):
    ''' given a non-negative fraction q, return a pair (a,b) such that q = a * a * b
        where b is a square-free integer.

        if q is a perfect square, a is its square root and b is one.
    '''

    if q == 0:
        return q, 1
    if q < 0:
        raise ValueError('math domain error %s' % q)

    a, b = isqrt(q.numerator)
    c, d = isqrt(q.denominator)

    # q == (a/c)**2 * (b/d) == (a/(c*d))**2 * b*d
    return Fraction(a, c * d), b * d


class Constructible(object):
    """This class implements constructible numbers.
    
    It is usually not necessary to construct Constructible numbers explicitly,
    use mathematical expressions with Constructible and Rational numbers or
    use constructible.sqrt .
    """
    # pylint: disable=protected-access
    def __init__(self, a, b=None, field=()):
        """constructs a Constructible instance.
        
        The one-argument form wraps a Rational instance (e.g. an int or a Fraction)
        in a Constructible instance.
        
        The default arguments are for internal use:
        
        If a and b are given they must be Constructible instances in the
        same rational extension K. field must be a tuple (r, K) with 
        r in K. The resulting Constructible represents a + b * sqrt(r) in K[sqrt(r)]
        """
        assert isinstance(field, tuple)
        if field:
            assert len(field) == 2
            assert isinstance(field[0], Constructible)
            assert isinstance(field[1], tuple)
        if b is None:
            if field:
                raise ValueError('can not set field if b is not given')

            if isinstance(a, Constructible):
                # used as a copy constructior
                self.a = a.a
                self.b = a.b
                self.field = a.field
                self.is_zero = a.is_zero

            else:
                # used as a conversion from Fraction, int or float
                self.a = Fraction(a)
                self.b = 0
                self.field = ()
                self.is_zero = (a == 0)

        else:
            # 'private' constructor
            self.a = a
            self.b = b
            self.field = field
            if field:
                self.is_zero = a.is_zero and b.is_zero
            else:
                self.is_zero = (a == b == 0)
            assert not field or a.field == b.field == self.base_field, '%r, %r, %r, %r' % (field, a.field, b.field, self.base_field)


    @property
    def r(self):
        """The square of the extension radix.
        
        The instance ist contained in the quardratic extension field
        base_field[sqrt(r)]
        """
        return self.field[0]


    @property
    def base_field(self):
        """The base field of which the current field is an extension.
        
        The instance ist contained in the quardratic extension field
        base_field[sqrt(r)]
        """
        return self.field[1]


    def __repr__(self):
        """eval-able representation of the instance"""
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self.a, self.b, self.field)


    def __str__(self):
        """readable representation of the instance"""
        if not self.b:
            return str(self.a)
        elif self.b==1:
            if not self.a:
                return 'sqrt(%s)' % (self.r)
            else:
                return '(%s + sqrt(%s))' % (self.a, self.r)
        else:
            if not self.a:
                return '(%s * sqrt(%s))' % (self.b, self.r)
            str_b = str(self.b)
            if str_b == '-1':
                str_b = ' - '
            elif str_b.startswith('-'):
                str_b = '- ' + str_b[1:] + ' *'
            else:
                str_b = '+ ' + str_b + ' *'
            return '(%s %s sqrt(%s))' % (self.a, str_b, self.r)


    # Arithmetical Operator
    # Additive Group Operations + -
    def __pos__(self):
        return self

    def __neg__(self):
        return Constructible(-self.a, -self.b, self.field)

    def __add__(self, other):
        if not isinstance(other, Constructible):
            if isinstance(other, Rational):
                other = Constructible(other)
            else:
                return NotImplemented

        if self.is_zero:
            return other
        if other.is_zero:
            return self

        if self.field == other.field:
            return Constructible(self.a + other.a, self.b + other.b, self.field)

        a, b = self.join(other)
        return a + b

    def __sub__(self, other):
        return self +(-other)

    __radd__ = __add__

    def __rsub__(self, other):
        return other + (-self)

    # Multiplicative Group Operations * /
    def inverse(self):
        """the multiplicative inverse of the instance"""
        if self.field:
            # 1/(a+b√r) = (a-b√r)/((a+b√r)*(a-b√r)) = (a+b√r) / (a*a-b*b*r)
            d = self.a * self.a - self.b * self.b * self.r
            return Constructible(self.a / d, -self.b / d, self.field)
        else:
            # self is a rational
            return Constructible(1 / self.a)

    def __mul__(self, other):
        if not isinstance(other, Constructible):
            if isinstance(other, Rational):
                return Constructible(self.a * other, self.b * other, self.field)
            else:
                return NotImplemented

        if self.is_zero:
            return self
        if other.is_zero:
            return other

        if self.field == other.field:
            if not self.field:
                return Constructible(self.a * other.a)
            # (a+b√r)(c+d√r) = (ac+bdr) + (ad+bc)√r
            return Constructible(self.a * other.a + self.b * other.b * self.r,
                                 self.a * other.b + self.b * other.a,
                                 self.field)

        a, b = self.join(other)
        return a * b

    def __truediv__(self, other):
        if not isinstance(other, Constructible):
            if isinstance(other, Rational):
                return Constructible(self.a / other, self.b / other, self.field)
            else:
                return NotImplemented

        return self * other.inverse()

    __rmul__ = __mul__

    def __rtruediv__(self, other):
        return self.inverse() * other

    # equality and ordering
    def _sign(self):
        """The sign of the instance
        
        x._sign() ==  1  if  x > 0
        x._sign() ==  0  if  x == 0
        x._sign() == -1  if  x < 0 
        """
        
        # pylint: disable=maybe-no-member
        if self.is_zero:
            return 0
        elif not self.field:
            # representing a rational
            if self.a > 0:
                return 1
            elif self.a < 0:
                return -1
            else:
                return 0
        else:
            if self.a.is_zero:
                return self.b._sign()
            if self.b.is_zero:
                return self.a._sign()
            sa = self.a._sign()
            sb = self.b._sign()
            if sa == sb:
                return sa
            else:
                return sa * (self.a * self.a - self.r * self.b * self.b)._sign()

    def __bool__(self):
        return self != 0

    __nonzero__ = __bool__

    def __eq__(self, other):
        if other == 0:
            return self.is_zero

        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() == 0

        return NotImplemented

    def __ne__(self, other):
        if other == 0:
            return not self.is_zero

        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() != 0

        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() < 0

        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() > 0

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() <= 0

        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() >= 0

        return NotImplemented

    # conjugation in the `self.field`
    def _conjugate(self):
        assert self.field, 'should not be called on rationals'
        return Constructible(self.a, -self.b, self.field)

    # minimal polynomial
    # (a0, a1, ...) represents a0 * x**0 + a1 * x**1 + ...
    def minpoly(self):
        """return a minimal polynomial for self.

        The polynomial p is represented as a tuple a of rationals such that
            p(x) := a[0] + a[1] * x + a[2] * x**2 + ... + a[n] * x**n
        and satisfies
            p(self) == 0
        """

        field = self.field
        one = Constructible.lift_rational_field(1, field)
        poly = (-self, one)

        while field:
            field = field[1]
            if all(c.b == 0 for c in poly):
                # `poly` is its own conjugate, so just unlift it
                poly = tuple(c.a for c in poly)
                continue

            # calculate unlifted `poly * conj(poly)`
            conj_poly = tuple(c._conjugate() for c in poly)
            new_poly = []
            deg = len(poly) - 1
            zero = Constructible.lift_rational_field(0, field)

            for m in range(deg * 2 + 1):
                if m % 2 == 0:
                    x = poly[m // 2] * conj_poly[m // 2]
                    assert x.b == 0
                    coef = x.a
                else:
                    coef = zero

                # iterating i such that 0 <= i < m - i <= deg:
                for i in range(max(0, m - deg), (m + 1) // 2):
                    x = poly[i] * conj_poly[m - i]
                    coef += x.a * 2

                new_poly.append(coef)

            poly = new_poly

        return tuple(c.a for c in poly) # a tuple of `Rational`s

    def __hash__(self):
        # rational numbers compare equal to self.a and also need to have the same hash.
        if not self.field:
            return hash(self.a)
        # otherwise we need a hash that is independent of the representation of
        # the constructible number.
        return hash(self.minpoly())

    def __float__(self):
        if self.is_zero:
            return 0.0
        elif self.field:
            return float(self.a) + float(self.b) * math.sqrt(float(self.r))
        else:
            return float(self.a)

    def join(self, other):
        '''Express self and other as members of a common field.
        
        return a tuple (new_self, new_other) such that
        new_self == self, new_other == other, and new_self.field == new_other.field
        '''
        if self.field == other.field:
            return self, other

        _, f1, f2 = Constructible.join_fields(self.field, other.field)
        return f1(self), f2(other)

    @staticmethod
    def join_fields(field1, field2):
        """find an extension field containing both field1 and field2
        
        returns the resulting field containing both field1 and field2 and
        two mappings for representing instances of the original fields in the new field.
        f1: field1 --> field:  f1(x) == x
        f2: field2 --> field:  f2(x) == x

        """
        # pylint: disable=function-redefined
        Q = ()

        if field1 == Q:
            def f1(x):
                assert x.field == field1
                return Constructible.lift_rational_field(x.a, field2)
            def f2(y):
                assert y.field == field2
                return y
            return field2, f1, f2

        if field2 == Q:
            def f1(x):
                assert x.field == field1
                return x
            def f2(y):
                assert y.field == field2
                return Constructible.lift_rational_field(y.a, field1)
            return field1, f1, f2

        r, base2 = field2
        jbase, f1_base, f2_base = Constructible.join_fields(field1, base2)

        s = f2_base(r)._try_sqrt()
        if s is None:
            field = (f2_base(r), jbase)
            def f1(x):
                assert x.field == field1
                return Constructible(f1_base(x), Constructible.lift_rational_field(0, jbase), field)
            def f2(y):
                assert y.field == field2
                return Constructible(f2_base(y.a), f2_base(y.b), field)
            return field, f1, f2
        else:
            def f2(y):
                assert y.field == field2
                return f2_base(y.a) + f2_base(y.b) * s
            return jbase, f1_base, f2

    @staticmethod
    def lift_rational_field(q, field):
        """represent a rational q in the given field
        
        return a Constructible x such that x == q and x.field == field
        """
        if not field:
            return Constructible(q)
        else:
            zero = Constructible.lift_rational_field(0, field[1])
            lift = Constructible.lift_rational_field(q, field[1])
            return Constructible(lift, zero, field)


    # taking square roots
    def _try_sqrt(self):
        ''' try to compute the square root in the field itself.

        if there is no square root in the field return None.
        '''
        if not self.field:
            assert self.b == 0
            root, remainder = fsqrt(self.a)
            if remainder == 1:
                return Constructible(root)
            else:
                return None

        if self._sign() < 0:
            raise ValueError('math domain error %s' % self)

        nn = self.a * self.a - self.b * self.b * self.r
        if nn._sign() < 0:
            return None

        n = nn._try_sqrt()
        if n is None:
            return None

        a = ((self.a + n) * Fraction(1, 2))._try_sqrt()
        if a is not None:
            result = Constructible(a, self.b / a * Fraction(1, 2), self.field)
            assert result.field == self.field
            return result

        b = ((self.a + n) / self.r * Fraction(1, 2))._try_sqrt()
        if b is not None:
            result = Constructible(self.b / b * Fraction(1, 2), b, self.field)
            assert result.field == self.field
            return result

        return None

def sqrt(n):
    '''return the square root of n in an exact representation
    
    If possible the square root is expressed in the field of the 
    argument thus avoiding redundand field extensions such as
    Q[√2][√3][√6]
    '''
    if isinstance(n, Rational):
        n = Constructible(n)
    elif not isinstance(n, Constructible):
        raise ValueError('the square root is not implemented for the type %s' % type(n))

    r = n._try_sqrt()  # pylint: disable=protected-access
    if r is not None:
        return r
    return Constructible(Constructible.lift_rational_field(0, n.field),
                         Constructible.lift_rational_field(1, n.field),
                         (n, n.field))
