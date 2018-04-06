# coding=utf-8

from random import randint
from time import sleep

import matplotlib.pyplot as plt
import numpy as np
from numpy.random import randint

from unit.ikrlib import rand_gauss, plot2dfun, gellipse, train_gauss, train_gmm, logpdf_gmm, \
    logistic_sigmoid


class GaussianMixtureModelDetector(object):
    def run(self, x1=None):

        # Generate random data for classes X1 and X2. The data for each class are
        # generated from two gaussian distributions. Hopefully, we will be able to
        # learn these distributions from data using EM algorithm implemented in
        # 'train_gmm' function.
        x1 = x1 # or np.r_[rand_gauss(400, np.array([50, 40]), np.array([[100, 70], [70, 100]])),
                #         rand_gauss(200, np.array([55, 75]), np.array([[25, 0], [0, 25]]))]

        mu1, cov1 = train_gauss(x1)
        p1 = 0.5

        # Plot the data
        plt.plot(x1[:, 0], x1[:, 1], 'r.')
        gellipse(mu1, cov1, 100, 'r')
        ax = plt.axis()
        plt.draw()

        # Train and test with GMM models with full covariance matrices
        # Decide for number of gaussian mixture components used for the model
        m1 = 20

        # Initialize mean vectors to randomly selected data points from corresponding class
        mus1 = x1[randint(1, len(x1), m1)]

        # Initialize all covariance matrices to the same covariance matrices computed using
        # all the data from the given class
        covs1 = [cov1] * m1

        # Use uniform distribution as initial guess for the weights
        ws1 = np.ones(m1) / m1

        # fig = plt.figure()
        # ims = []

        # Run 30 iterations of EM algorithm to train the two GMM models
        axes = plt.gca()
        xdata = []
        ydata = []
        line, = axes.plot(xdata, ydata, 'b.')

        for i in range(300):
            line.set_xdata(x1[:, 0])
            line.set_ydata(x1[:, 1])

            # plt.plot(x1[:, 0], x1[:, 1], 'r.')

            for w, m, c in zip(ws1, mus1, covs1):
                gellipse(m, c, 100, 'r', lw=round(w * 10))
            ws1, mus1, covs1, ttl1 = train_gmm(x1, ws1, mus1, covs1)
            print('Total log-likelihood: %s for class X1;' % (ttl1,))
            plt.draw()
            plt.pause(1e-17)
            sleep(.1)
            plt.clf()

        hard_decision = lambda x: logpdf_gmm(x, ws1, mus1, covs1) + np.log(
            p1) > 0  # logpdf_gmm(x, ws2, mus2, covs2) + np.log(p2)
        plot2dfun(hard_decision, ax, 500)
        plt.plot(x1[:, 0], x1[:, 1], 'r.')
        for w, m, c in zip(ws1, mus1, covs1):
            gellipse(m, c, 100, 'r', lw=round(w * 10))
        # for w, m, c in zip(ws2, mus2, covs2):
        #     gellipse(m, c, 100, 'b', lw=round(w * 10))

        plt.figure()
        x1_posterior = lambda x: logistic_sigmoid(
            logpdf_gmm(x, ws1, mus1, covs1) + np.log(p1)
            # - logpdf_gmm(x, ws2, mus2, covs2) - np.log(p2)
        )
        plot2dfun(x1_posterior, ax, 500)
        plt.plot(x1[:, 0], x1[:, 1], 'r.')
        for w, m, c in zip(ws1, mus1, covs1):
            gellipse(m, c, 100, 'r', lw=round(w * 10))
        # for w, m, c in zip(ws2, mus2, covs2): gellipse(m, c, 100, 'b', lw=round(w * 10))
        plt.show()
