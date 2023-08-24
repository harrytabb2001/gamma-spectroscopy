#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 11:46:45 2022

@author: harrytabb
"""

import numpy as np
import matplotlib.pyplot as plt

coeff1 = 0.810289
coeff2 = -0.847134

background_raw = np.genfromtxt('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Background.txt')

channel = np.arange(0, len(background_raw))
energy = coeff1*channel + coeff2
index_below = np.where(energy < 150)
index_above = np.where(energy > 1500)

indices = np.hstack((index_below, index_above))[0]
energy_new = np.delete(energy, indices)


background_raw_new = np.delete(background_raw, indices)

rock1_raw = np.genfromtxt('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Rock1.txt')
rock1_raw_new = np.delete(rock1_raw, indices)

mud_raw = np.genfromtxt('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Mud.txt')

rock2_raw = np.genfromtxt('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Rock2.txt')
rock2_raw_new = np.delete(rock2_raw, indices)

mud_raw_new = np.delete(mud_raw, indices)

rock1 = np.dstack((rock1_raw_new, energy_new))[0]
mud = np.dstack((mud_raw_new, energy_new))[0]
rock2 = np.dstack((rock2_raw_new, energy_new))[0]

background = np.dstack((background_raw, energy))[0]
background_new = np.dstack((background_raw_new, energy_new))[0]

def diff(sample):
    difference = sample[:,0] - background_new[:,0]
    error = np.sqrt(sample[:,0] + background_new[:,0])
    
    final = np.dstack((difference, energy_new, error))[0]
    return final

# fig1 = plt.figure()
# ax = fig1.add_subplot(111)
# ax.scatter(channel, background[:,0], marker='.', linewidth=0.00000001)
# ax.grid()
# ax.set_xlabel('Energy / KeV')
# ax.set_ylabel('Counts')
# ax.set_title('Background Counts')
# plt.savefig('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Background.png', dpi=1000)
# plt.show()


rock1_final = diff(rock1)
mud_final = diff(mud)
rock2_final = diff(rock2)

# fig2 = plt.figure()
# ax = fig2.add_subplot(111)
# ax.scatter(rock1_final[:,1], rock1_final[:,0], marker='.', linewidth=0.0000000000001)
# ax.set_xlabel('Energy  / KeV')
# ax.set_ylabel('Counts')
# ax.set_title('Rock 1 without Background')
# ax.set_ylim(2)
# plt.savefig('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Rock1.png', dpi=1000)
# plt.show()

fig3 = plt.figure()
ax = fig3.add_subplot(111)
ax.scatter(mud_final[:,1], mud_final[:,0], marker='.', linewidth=0.0000000000001)
ax.set_xlabel('Energy  / KeV')
ax.set_ylabel('Counts')
ax.set_title('Mud without Background')
ax.set_ylim(2)
plt.savefig('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/Mud.png', dpi=1000)
plt.show()

# fig4 = plt.figure()
# ax = fig4.add_subplot(111)
# ax.scatter(rock2_final[:,1], rock2_final[:,0], marker='.', linewidth=0.0000000000001)
# ax.set_xlabel('Energy  / KeV')
# ax.set_ylabel('Counts')
# ax.set_title('Rock 2 without Background')
# ax.set_ylim(2)
# plt.savefig('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/rock2.png', dpi=1000)
# plt.show()









