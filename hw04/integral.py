#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import scipy.stats
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt


def monte_carlo(n, integrand, distribution, rv, **kwargs):
    variates = distribution(size=n, **kwargs)
    return np.mean(integrand(variates) / rv.pdf(variates))


def rmse(ns, integral_value, m=100, **kwargs):
    def mse(n):
        return np.mean([(monte_carlo(n, **kwargs) - integral_value) ** 2 for _ in range(m)])

    return [np.sqrt(mse(n)) for n in ns]


def plot(x, ys):
    for y in ys:
        plt.plot(x, y[0], label=y[1], linestyle=y[2])

    plt.xscale('log')
    plt.xlabel('n')
    plt.yscale('log')
    plt.ylabel('RMSE')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    function = lambda x: np.cos(x) * np.exp(-(x ** 2))
    integral = integrate.quad(function, -np.infty, np.infty)[0]

    powers = [10 ** power for power in range(1, 7)]
    results = [(rmse(powers, integral, integrand=function,
                     distribution=np.random.normal, rv=scipy.stats.norm), 'normal', '-'),
               (rmse(powers, integral, integrand=function,
                     distribution=np.random.normal, rv=scipy.stats.norm(scale=1 / np.sqrt(2)), scale=1 / np.sqrt(2)),
                'scaled normal', '-.'),
               (rmse(powers, integral, integrand=function,
                     distribution=np.random.standard_cauchy, rv=scipy.stats.cauchy), 'cauchy', '--'),
               (rmse(powers, integral, integrand=function,
                     distribution=np.random.laplace, rv=scipy.stats.laplace), 'laplace', ':')]
    plot(powers, results)