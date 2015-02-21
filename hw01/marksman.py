#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import numpy


def count_points_inside(count, edge_length=1.0):
    radius = edge_length / 2
    center = numpy.array([radius, radius])
    points = [numpy.random.uniform(size=2) for _ in range(count)]

    return sum([1 for point in points if numpy.linalg.norm(point - center) <= radius])


if __name__ == '__main__':
    for size in [10 ** i for i in range(10)]:
        print(size, count_points_inside(size) / size)