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

'''
Representing constructible numbers

Author: Leonhard Vogt
'''

from fractions import Fraction
from numbers import Rational

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

    a, b = 1, n
    k = 2
    while k * k <= b:
        d, m = divmod(b, k * k)
        while m == 0:
            a *= k
            b = d
            d, m = divmod(b, k * k)
        k += 1
    return a, b


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
    # pylint: disable=protected-access
    def __init__(self, a, b=None, field=()):
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
            self.is_zero = (a == b == 0)
            assert not field or a.field == b.field == self.base_field, '%r, %r, %r, %r' % (field, a.field, b.field, self.base_field)


    @property
    def r(self):
        return self.field[0]


    @property
    def base_field(self):
        return self.field[1]


    def __repr__(self):
        return '%s(%r, %r, %r)' % (self.__class__.__name__, self.a, self.b, self.field)


    def __str__(self):
        if not self.b:
            return str(self.a)
        return '(%s + %s * sqrt(%s))' % (self.a, self.b, self.r)


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

        if self.field == other.field:
            if not self.field:
                return Constructible(self.a * other.a)
            # (a+b√r)(c+d√r) = (ac+bdr) + (ad+bc)√r
            return Constructible(self.a * other.a + self.b * other.b * self.r,
                                 self.a * other.b + self.b * other.a,
                                 self.field)

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

    def __gt__(self, other):
        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() > 0

    def __le__(self, other):
        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() <= 0

    def __ge__(self, other):
        if isinstance(other, Constructible) or isinstance(other, Rational):
            return (self -other)._sign() >= 0

    def join(self, other):
        '''return a tuple (new_self, new_other) such that
        new_self == self, new_other == other, and new_self.field == new_other.field '''
        if self.field == other.field:
            return self, other

        _, f1, f2 = Constructible.join_fields(self.field, other.field)
        return f1(self), f2(other)

    @staticmethod
    def join_fields(field1, field2):
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
    '''return the square root of n in an exact representation'''
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

