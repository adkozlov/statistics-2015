#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import numpy


def n_sphere_volume(n, count):
    variables = numpy.random.uniform(size=(count, n - 1))

    new_variables = numpy.array([numpy.append(row, numpy.modf(numpy.sum(row))[0]) for row in variables])
    new_variables -= 0.5

    return numpy.count_nonzero([numpy.linalg.norm(row) <= 0.5 for row in new_variables]) / count


def n_sphere_real_volume(n, radius=1.0):
    from scipy.special._ufuncs import gamma

    arg = n / 2
    return (radius ** n) * (numpy.pi ** arg) / gamma(arg + 1)


def draw_graphic(n, x, y):
    import matplotlib.pyplot as plt

    plt.xlabel('number of points')
    plt.xscale('log')
    plt.ylabel(str(n) + '-sphere volume error')

    real_volume = n_sphere_real_volume(n, 0.5)
    plt.plot(x, y / real_volume, 'g^')
    plt.show()


if __name__ == '__main__':
    def test(n, origin, bound):
        x = [coefficient * 10 ** power for power in range(origin, bound) for coefficient in [2, 4, 8]]
        y = [n_sphere_volume(n, count) for count in x]
        draw_graphic(n, x, y)

    test(3, 3, 6)
    test(5, 4, 7)
    test(10, 4, 7)