#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import numpy as np
import matplotlib.pyplot as plt


def generate_variates(size=500, high=1.0):
    return np.random.uniform(0.0, high, size)


def percentile(x, percent=25):
    return np.percentile(x, percent) / percent * 100


def rmse(func, size, high, m=1000):
    def mse():
        return np.mean([(func(generate_variates(size, high)) - high) ** 2 for _ in range(m)])

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
    functions = [(lambda x: 2 * np.mean(x), 'mean', '-.'),
                 (lambda x: np.max(x), 'max', '-'),
                 (lambda x: (1 + 1 / len(x)) * np.max(x), 'scaled max', '--'),
                 (lambda x: 2 * np.median(x), 'median', ':'),
                 (lambda x: percentile(x), 'q(0.25)', '-'),
                 (lambda x: percentile(x, 75), 'q(0.75)', '--')]

    ns = range(100, 1000, 100)
    plot(ns, [([rmse(func, n, 5.0) for n in ns], label, line_style) for (func, label, line_style) in functions])