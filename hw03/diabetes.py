#!/usr/bin/env python3

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"

import sys

import numpy as np


def calculate_error_rate(diabetes_probability=0.01, tests_number=100000,
                         mu_ill=3.0, sigma_ill=2.0,
                         mu_not_ill=1.0, sigma_not_ill=0.35):
    def generate_normal_variates(mu, sigma, size):
        return np.random.normal(mu, sigma, int(size))

    def generate_normal_variates_ill():
        return generate_normal_variates(mu_ill, sigma_ill, diabetes_probability * tests_number)

    def generate_normal_variates_not_ill():
        return generate_normal_variates(mu_not_ill, sigma_not_ill, (1.0 - diabetes_probability) * tests_number)

    def calculate_probability(x, mu, sigma):
        return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))

    def iterate_variates(variates, is_really_ill, delta_bound, decision_bound):
        result = 0
        for x in variates:
            probability_ill = calculate_probability(x, mu_ill, sigma_ill)
            probability_not_ill = calculate_probability(x, mu_not_ill, sigma_not_ill)

            bayes_factor_minus_one = probability_ill * diabetes_probability / (
                probability_not_ill * (1.0 - diabetes_probability)) - 1.0
            is_ill = bayes_factor_minus_one > 0
            if (is_ill and not is_really_ill) or (not is_ill and is_really_ill):
                result += 1

            bayes_factor_minus_one = abs(bayes_factor_minus_one)
            if bayes_factor_minus_one < delta_bound:
                delta_bound = bayes_factor_minus_one
                decision_bound = x

        return result, delta_bound, decision_bound

    result_ill = iterate_variates(generate_normal_variates_ill(), True, sys.float_info.max, None)
    result_not_ill = iterate_variates(generate_normal_variates_not_ill(), False, result_ill[0], result_ill[1])

    return (result_ill[0] + result_not_ill[0]) / tests_number, result_not_ill[2]


if __name__ == '__main__':
    print('error rate = %f\ndecision bound = %f' % calculate_error_rate())