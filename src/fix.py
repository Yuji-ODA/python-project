from functools import partial
from inspect import signature


def y_combinator(f): return lambda x: f(y_combinator(x(x)))


def z(f): return (lambda x: f(lambda y: x(x)(y)))(lambda x: f(lambda y: x(x)(y)))


def fix(f): return f(lambda x: fix(f)(x))


def curried(f): return f if len(signature(f).parameters) == 1 else lambda x: curried(partial(f, x))


if __name__ == '__main__':
    fib_40 = fix(lambda f: curried(lambda a0, a1, n: a0 if n <= 0 else f(a1)(a0+a1)(n-1)))(0)(1)(40)
    print(fib_40)
