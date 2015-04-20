#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import numpy as np
from scipy import integrate, stats
import matplotlib.pyplot as plt


def monte_carlo(integrand, size=10 ** 7, rv=stats.beta, **kwargs):
    variates = rv.rvs(size=size, **kwargs)
    values = integrand(variates) / rv.pdf(variates, **kwargs)

    return np.arange(size) + 1, values


def calculate_integral_and_variance(integrand, rv=stats.beta, low=0.0, high=1.0, **kwargs):
    def calculate_integral(func):
        return integrate.quad(func, low, high)[0]

    integral_value = calculate_integral(integrand)
    return integral_value, calculate_integral(lambda x: integrand(x) ** 2 / rv.pdf(x, **kwargs)) - integral_value ** 2


def cumulative_mean(xs, ys):
    return np.cumsum(ys) / xs


def cumulative_variance(xs, ys):
    return cumulative_mean(xs, ys ** 2) - cumulative_mean(xs, ys) ** 2


def calculate_confidence_interval(xs, ys, variance=None):
    variance = np.zeros(len(ys)) + variance if variance else cumulative_variance(xs, ys)
    return stats.norm.ppf(0.975) / np.sqrt(xs) * np.sqrt(variance)


def plot(points, integral_value, variance_value, label, y_min, y_max, ratio=0.1):
    xs = points[0]
    ys = points[1]

    ci1 = calculate_confidence_interval(xs, ys)
    ci2 = calculate_confidence_interval(xs, ys, variance_value)
    ys = cumulative_mean(xs, ys)

    def drop_first(x):
        origin = int(ratio * len(x))
        return x[origin:]

    xs = drop_first(xs)
    ys = drop_first(ys)
    ci1 = drop_first(ci1)
    ci2 = drop_first(ci2)

    plt.plot(xs, ys, label=label, linestyle='-.')
    plt.axhline(integral_value)

    plt.plot(xs, ys - ci1, linestyle='--', color='r', label='- ci (avg)')
    plt.plot(xs, ys + ci1, linestyle='--', color='r', label='+ ci (avg)')

    plt.plot(xs, ys - ci2, linestyle='-', color='g', label='- ci')
    plt.plot(xs, ys + ci2, linestyle='-', color='g', label='+ ci')

    plt.ylim((y_min, y_max))
    plt.xlabel('n')
    plt.ylabel('cum. avg')
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    function = lambda x: np.sin(x) ** (-3 / 4)
    # integral, variance = calculate_integral_and_variance(function, a=0.25, b=1.0)
    # plot(monte_carlo(function, a=0.25, b=1.0), integral, variance, 'B(1/4, 1)', 4.0582, 4.0588)

    integral, variance = calculate_integral_and_variance(function, a=0.5, b=0.5)
    plot(monte_carlo(function, a=0.5, b=0.5), integral, variance, 'B(1/2, 1/2)', 4.02, 4.08)