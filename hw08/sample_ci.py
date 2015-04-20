#!/usr/bin/env python3
import numpy as np
import scipy.stats

__author__ = "Andrew Kozlov"
__copyright__ = "Copyright 2014, SPbAU"


def calculate_ci(distribution, label, m=1000):
    print(label)
    print('gamma\tn\tlen (np)\tlen (p)\t' +
          'rmse left (np)\trmse right (np)\trmse left (p)\trmse right (p)\tratio (np)\tratio (p)')

    for gamma in [0.95, 0.99]:
        left = (1 - gamma) / 2
        right = (1 + gamma) / 2

        for n in [10 ** power for power in range(1, 5)]:
            def zeros():
                return np.zeros(m)

            np_left = zeros()
            np_right = zeros()

            p_left = zeros()
            p_right = zeros()

            np_ratio = zeros()
            p_ratio = zeros()

            for i in range(m):
                x = distribution.rvs(size=n)

                def not_parametric_and_parametric(p):
                    return np.percentile(x, p * 100.0), scipy.stats.norm.ppf(p, loc=np.mean(x), scale=np.var(x))

                np_left[i], p_left[i] = not_parametric_and_parametric(left)
                np_right[i], p_right[i] = not_parametric_and_parametric(right)

                def ratio(l, r):
                    return len(x[(x >= l) & (x <= r)]) / len(x)

                np_ratio[i] = ratio(np_left[i], np_right[i])
                p_ratio[i] = ratio(p_left[i], p_right[i])

            def rmse(x, p):
                return np.mean((x - distribution.ppf(p)) ** 2)

            print('%.2f\t%5d\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%.5f\t%.3f\t%.3f' % (gamma,
                                                                                 n,
                                                                                 np.mean(np_right - np_left),
                                                                                 np.mean(p_right - p_left),
                                                                                 rmse(np_left, left),
                                                                                 rmse(np_right, right),
                                                                                 rmse(p_left, left),
                                                                                 rmse(p_right, right),
                                                                                 np.mean(np_ratio),
                                                                                 np.mean(p_ratio)))
    print()


if __name__ == '__main__':
    calculate_ci(scipy.stats.norm(loc=0, scale=1), "norm")
    calculate_ci(scipy.stats.t(df=5), "t_5")
    calculate_ci(scipy.stats.t(df=20), "t_{20}")