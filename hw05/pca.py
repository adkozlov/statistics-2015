#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import sys

import numpy as np
import matplotlib.pyplot as plt


def read_data(filename):
    return np.genfromtxt(filename, delimiter=',')[:, :-1]


def transform(matrix):
    def transformation_matrix():
        eig_value, eig_vector = np.linalg.eig(np.cov(np.transpose(matrix)))
        zipped = list(zip(np.abs(eig_value), eig_vector))

        zipped.sort(reverse=True)
        _, result = zip(*zipped)

        return np.transpose(result)

    return matrix.dot(transformation_matrix())


def plot(matrix):
    n = matrix.shape[1]
    _, axes = plt.subplots(ncols=n, nrows=n)
    for i in range(n):
        for j in range(n):
            axes[i][j].scatter(matrix[:, i], matrix[:, j])
    plt.show()


if __name__ == '__main__':
    data = read_data(sys.argv[1])
    plot(data)
    plot(transform(data))