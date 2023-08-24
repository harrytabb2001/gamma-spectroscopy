#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 16:01:34 2022

@author: harrytabb
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fmin

start_A = 3000
start_n = -2
start_values = (start_A, start_n)


def efficiency_function(data, initial_A, initial_n):
    return initial_A * data**initial_n

def chi_squared_function(A_n_values, energies, efficiency, uncertainty):

    A = A_n_values[0]
    n = A_n_values[1]

    predicted_efficiency = efficiency_function(energies, A, n)

    chi_square_equation = np.sum(((predicted_efficiency - efficiency)
                                  / uncertainty)**2)

    return chi_square_equation


def fit_function(start_A_n, energies, efficiency, uncertainty):

    fit = fmin(chi_squared_function, start_A_n,
               args=(energies, efficiency, uncertainty),
               full_output=True, disp=0)
    A_and_n = fit[0]
    chi_square_minimum = fit[1]
    return A_and_n, chi_square_minimum

def meshing(array):

    mesh = np.empty((0, len(array)))
    for _iterator in enumerate(array):
        mesh = np.vstack((mesh, array))
    return mesh

def final_coefficient_array(value):
    '''
    Makes an array +/- 0.05 around a specified value with 200 samples.

    Parameters
    ----------
    value : float
        value that array is built around

    Returns
    -------
    array : Array
    '''

    array = np.linspace((value - 0.05), (value + 0.05), 200)
    return array

def plot_contour(
        mesh_mass, mesh_width, mesh_chi_square, chi_square_value,
        coefficients_final):
    '''
    Takes an input of mass, width and corresponding chi square values as a
    mesh. These are then used to produce a contour plot of mass and width
    against chi square. The contour lines are at the minimum chi square + 1 and
    then the next 3 confidence regions.
    The points of the minimum and maximum values of mass and width on the chi
    square minimum + 1 ellipse are represented by dots. The difference bewteen
    these points are calculated and divided by 2 to find the uncertainty on the
    coefficients.

    Parameters
    ----------
    mesh_mass : array
        array of masses in mesh format
    mesh_width : array
        array of width in mesh format
    mesh_chi_square : array
        array of chi square in mesh format corresponding to the meshes of mass
        and width
    chi_square_value : float

    Returns
    -------
    contour_plot
    mass_difference : float
    width_difference : float
    '''
    mass_final = coefficients_final[0]
    width_final = coefficients_final[1]
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel(r'$A$ value ', fontsize=15, name='serif')
    ax.set_ylabel(r'$n$ value', fontsize=15, name='serif')
    ax.set_title(r'$\chi^2$ Contour Plot', fontsize=15, name='serif',
                 weight='bold')

    contour_levels = [chi_square_value + 1, chi_square_value + 2.3,
                      chi_square_value + 5.99, chi_square_value + 9.21]
    contour_plot = ax.contour(mesh_mass, mesh_width, mesh_chi_square, levels=contour_levels, cmap='seismic')
    ax.clabel(contour_plot)

    ax.minorticks_on()
    ax.grid(dashes=(2, 5), color='k')

    labels = [r'$\chi^{2}_{min}$ + 1.00', r'$\chi^{2}_{min}$  + 2.30',
              r'$\chi^{2}_{min}$ + 5.99', r'$\chi^{2}_{min}$ + 9.21']

    ax.scatter(mass_final, width_final, label=r'$\chi^{2}_{min}$', marker='x')

    for i in (0,3):
        contour_plot.collections[i].set_label(labels[i])

    mass_min = np.min(contour_plot.allsegs[0][0][:, 0])
    mass_min_index = np.where(contour_plot.allsegs[2][0][:, 0]
                              == mass_min)[0][0]
    width_at_mass_min = contour_plot.allsegs[2][0][:, 1][mass_min_index]

    # mass_max = np.max(contour_plot.allsegs[0][0][:, 0])
    # mass_max_index = np.where(contour_plot.allsegs[0][0][:, 0]
    #                           == mass_max)[0][0]
    # width_at_mass_max = contour_plot.allsegs[0][0][:, 1][mass_max_index]

    # mass_difference = mass_max - mass_min

    # width_min = np.min(contour_plot.allsegs[0][0][:, 1])
    # width_min_index = np.where(contour_plot.allsegs[0][0][:, 1]
    #                             == width_min)[0][0]
    # mass_at_width_min = contour_plot.allsegs[0][0][:, 0][width_min_index]

    # width_max = np.max(contour_plot.allsegs[0][0][:, 1])
    # width_max_index = np.where(contour_plot.allsegs[0][0][:, 1]
    #                             == width_max)[0][0]
    # mass_at_width_max = contour_plot.allsegs[0][0][:, 0][width_max_index]

    # width_difference = width_max - width_min

    # ax.scatter(mass_max, width_at_mass_max, c='orange',
    #             label=r'$m_z$ min / max')
    ax.scatter(mass_min, width_at_mass_min, c='orange')

    # ax.scatter(mass_at_width_min, width_min, c='r',
    #             label=r'$\Gamma_z$ min / max')
    # ax.scatter(mass_at_width_max, width_max, c='r')

    # plt.legend(bbox_to_anchor=(1, 1.03), loc='upper left')

    # plt.savefig('Contour-Plot.png', dpi=300, bbox_inches='tight')

    return contour_plot


time  = 4312.7

counts = np.array([57755, 6312, 12075, 592.4, 723.29, 1011, 732.7, 489.5])
energy = np.array([121.952, 245.35, 344.84, 411.91, 444.95, 779.61, 964.45, 1407.38])

intensities = np.array([28.58, 7.583, 26.50, 2.234, 2.821, 12.942, 14.605, 21.005])

intensities_ratio = intensities / intensities[0]

counts_err = np.sqrt(counts)

count_rate = counts / time

rate_err = count_rate * counts_err / counts

ratio_rates = count_rate / np.max(count_rate)

ratio_rates_err = []

for i in range(len(ratio_rates)):
    ratio_rate_err = ratio_rates[i] * np.sqrt((rate_err[0] / count_rate[0])**2 + (rate_err[i] / count_rate[i])**2)
    ratio_rates_err.append(ratio_rate_err)

eff_ratio = ratio_rates / intensities_ratio
eff_ratio_errs = []

for i in range(len(eff_ratio)):
    eff_ratio_err = eff_ratio[i] * ratio_rates_err[i] / ratio_rates[i]
    eff_ratio_errs.append(eff_ratio_err)

EU_eff = eff_ratio
EU_eff_errs = eff_ratio_errs
EU_energy = energy

Ba_eff = [0.140 + 0.1, 0.193 + 0.1, 0.0969 + 0.1]
Ba_eff_errs = [0.001, 0.001, 0.0005]
Ba_energy = [303.63, 276.28, 356.41]


eff_ratio = np.append(eff_ratio, [0.140 + 0.1, 0.193 + 0.1, 0.0969 + 0.1])
eff_ratio_errs = np.append(eff_ratio_errs, [0.001, 0.001, 0.0005])
energy = np.append(energy, [303.63, 276.28, 356.41])


final_values = fit_function(start_values, energy, eff_ratio, eff_ratio_errs)
final_coefficients = final_values[0]
A_final = 3140
n_final = -1.667
chi_final = final_values[1]

err_A = 104
err_n = 0.006

energy_plot = np.linspace(120, 1500, 200)


# A_array = np.linspace(A_final - 2 , (start_A + 2), 200)
# n_array = np.linspace(n_final - 0.05, (n_final + 0.05), 200)

final_eff_theory = efficiency_function(energy_plot, final_values[0][0], final_values[0][1])

# A_mesh = meshing(A_array)
# n_mesh = meshing(n_array)

# A_mesh_list = A_mesh.flatten()
# n_mesh_list = n_mesh.flatten()

# A_n_list = np.column_stack((A_mesh_list, n_mesh_list))

# chi_square_list = np.empty((0, len(A_n_list)))

# for pair in A_n_list:
#     chi_square = chi_squared_function(pair, energy, eff_ratio, eff_ratio_errs)
#     chi_square_list= np.append(chi_square_list, chi_square)
    
# chi_square_mesh = np.reshape(chi_square_list, (-1, len(A_array)))

# chi_square_plot = plot_contour(A_mesh, n_mesh, chi_square_mesh,
#                                 chi_final, final_coefficients)

# contour_levels = [chi_final + 1, chi_final + 2.3,
#                       chi_final + 5.99, chi_final + 9.21]

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.contour(A_mesh, n_mesh, chi_square_mesh, levels=contour_levels, cmap='seismic')
# plt.show()

plt.figure()
plt.errorbar(EU_energy, EU_eff, yerr= EU_eff_errs, c='orange', fmt='o', ecolor='r' , label='Data points for Europium-152')
plt.errorbar(Ba_energy, Ba_eff, yerr= Ba_eff_errs, c='green', fmt='o', ecolor='r' , label='Data points for Barium-133')
plt.plot(energy_plot, final_eff_theory, label='Fitting Function y=A$x^{n}$')
plt.text(100, -0.25, 'Coefficients:', fontweight='bold')
plt.text(100,-0.4, ' $A$ = {0:.0f}±{1:.0f} \n $n$ = {2:.3f}±{3:.3f}'.format(A_final, err_A, n_final, err_n))
plt.text(800,-0.35, '$\chi^{2}_{red}$ = 147.94')
plt.xlabel('Energy/KeV')
plt.ylabel('Relative Efficiencies ')
plt.title('Relative efficiency as a function of energy')
plt.grid()
plt.legend(loc='best')
plt.savefig('/Users/harrytabb/Desktop/Uni/Uni Year 2/Gamma/EffiencyGraph.png', dpi=600, bbox_inches='tight')
plt.show()




# fig5, axs5 = plt.subplots(1)
# axs5.plot(x, fitting_function, label='Fitting Function: $y=Ax^n$')
# axs5.text(100, -0.25, 'Coefficients:', fontweight='bold')
# axs5.text(100,-0.4, ' $A$ = {0:.0f}±{1:.0f} \n $n$ = {2:.3f}±{3:.3f}'.format(A_final, err_A, n_final, err_n))

# axs5.errorbar(energy, eff_ratio, yerr=eff_ratio_errs, fmt='o', ecolor='r' , label='Data points for Europium')
# axs5.set_xlabel('Energy/KeV')
# axs5.set_ylabel('Relative Efficiencies ')
# axs5.set_title('Relative efficiency as a function of energy')
# axs5.legend(loc='best')
# axs5.grid()
# plt.show()
# plt.savefig('/Users/mpotts/Documents/University/Semester 2/Labs/Gamma ray /relative efficiencies.png', dpi=500, bbox_inches='tight')





