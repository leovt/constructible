# coding:utf-8
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
        raise ValueError('math domain error')

    a, b = isqrt(q.numerator)
    c, d = isqrt(q.denominator)

    # q == (a/c)**2 * (b/d) == (a/(c*d))**2 * b*d
    return Fraction(a, c * d), b * d


class Constructible(object):
    def __init__(self, a, b=None, field=()):
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
            assert not field or a.field == b.field == self.base_field


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
        # TODO: implement joining fields

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

        n = (self.a * self.a - self.b * self.b * self.r)._try_sqrt()
        if n is None:
            return None

        a = ((self.a + n) * Fraction(1, 2))._try_sqrt()
        if a is not None:
            result = Constructible(a, self.b / a * Fraction(1, 2), self.r)
            assert result.field == self.field

        b = ((self.a + n) / self.r * Fraction(1, 2))._try_sqrt()
        if b is not None:
            result = Constructible(self.a / b * Fraction(1, 2), b, self.r)
            assert result.field == self.field

        return None



