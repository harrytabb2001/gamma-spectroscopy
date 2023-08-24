#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 14:35:44 2022

@author: harrytabb
"""

def chi_square(expected, observed):
    
    expected_new = np.array(expected)
    observed_new = np.array(observed)
    
    return np.sum(((expected_new - observed_new)**2) / expected_new)

import numpy as np
import matplotlib.pyplot as plt

energy = [59.50, 510.90, 661.70, 1173.20, 1274.50, 1332.50]
channel = [74.21, 630.90, 815.23, 1446.44, 1570.51, 1642.11]

grad = 0.811917
const = -0.809862

x = np.linspace(74.21, 1642, 1000)
y = grad*x + const

channel_EU = [151.25, 303.22, 425.81]
energy_EU = [121.9926, 245.3796, 344.9125]

obs = energy_EU
exp = [121.7817, 244.6975, 344.2785]


plt.figure()
plt.plot(channel, energy, 'ro', label='Energy Calibration')
plt.plot(x, y)
plt.plot(channel_EU, exp, 'go', label='Europium')
plt.legend()
plt.xlabel('Channel')
plt.ylabel('Energy / KeV')
plt.title('Energy Calibration Curve')
plt.grid()
plt.savefig('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Calibration2.png')
plt.show()

chi = chi_square(exp, obs)

def function(channel):
    return (0.81192 * channel) - 0.80986

