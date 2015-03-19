#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def generate_lambdas(blocks_count=10):
    return stats.uniform.rvs(size=blocks_count)


def generate_variates(variates_count=50000):
    return np.array([stats.expon.rvs(scale=1 / l, size=variates_count) for l in generate_lambdas()])


def get_min_variate(variates):
    return np.min(variates, axis=0)


def plot_histogram(variate):
    sns.distplot(variate, fit=stats.expon)
    plt.show()


if __name__ == '__main__':
    np.random.seed(489345284)
    plot_histogram(get_min_variate(generate_variates()))