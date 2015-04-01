#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import scipy.stats
import numpy as np
import matplotlib.pyplot as plt


def generate_variates(size, loc=0.0):
    return np.sort(scipy.stats.cauchy.rvs(loc=loc, size=size))


def rmse(func, size, loc, m=500):
    def mse():
        return np.mean([(func(generate_variates(size, loc)) - loc) ** 2 for _ in range(m)])

    return np.sqrt(mse())


def plot(x, ys):
    for (y, label, line_style) in ys:
        plt.plot(x, y, label=label, linestyle=line_style)

    plt.xscale('log')
    plt.xlabel('n')
    plt.yscale('log')
    plt.ylabel('RMSE')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    functions = [(lambda x: np.median(x), 'median', '-.'),
                 (lambda x: np.mean(x[1:-1]), 'trim min-max', '-'),
                 (lambda x: np.mean(scipy.stats.trimboth(x, 0.05)), 'trim 5%', '--')]

    powers = [10 ** power for power in range(2, 6)]
    plot(powers, [([rmse(func, n, 5.0) for n in powers], label, line_style) for (func, label, line_style) in functions])