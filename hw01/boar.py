#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import numpy


def calculate_probability(probabilities, shooter_number, count=10 ** 6):
    def calculate_mask(shots):
        result = 0
        for (i, (value, probability)) in enumerate(zip(shots, probabilities)):
            if value >= 1 - probability:
                result |= 1 << i

        return result

    def is_power_of_2(mask):
        return mask != 0 and ((mask & (mask - 1)) == 0)

    masks = [calculate_mask(list(numpy.random.uniform(size=len(probabilities)))) for _ in range(count)]

    def filter_masks(func):
        filtered_masks = list(filter(func, masks))
        return filtered_masks, len(filtered_masks)

    masks, denominator = filter_masks(lambda mask: is_power_of_2(mask))
    masks, numerator = filter_masks(lambda mask: mask == 2 ** shooter_number)

    return numerator / denominator


if __name__ == '__main__':
    print(calculate_probability([0.4, 0.3, 0.2], 1))