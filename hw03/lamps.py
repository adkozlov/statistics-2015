#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def generate_lambda(k=9.0, theta=1.0):
    return np.random.gamma(k, theta)


def calculate_parameters(real_lambda, tests_number=1000, k=9.0, theta=1.0):
    current = 1.0 / theta

    alphas = [k + i for i in range(tests_number)]
    betas = [current]
    for t in np.random.exponential(1 / real_lambda, tests_number):
        current = current + t
        betas.append(current)

    return zip(alphas, betas)


def plot(parameters, real_lambda):
    x = np.linspace(0, 30, 100)
    for (alpha, beta) in parameters:
        rv = stats.gamma(alpha, 0, 1 / beta)
        plt.plot(x, rv.pdf(x))
    plt.axvline(x=real_lambda, linewidth=1, color='k')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    l = generate_lambda()
    plot(calculate_parameters(l), l)