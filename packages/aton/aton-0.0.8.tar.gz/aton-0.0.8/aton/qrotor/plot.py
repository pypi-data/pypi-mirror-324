"""
# Description

This module provides straightforward functions to plot QRotor data.


# Index

| | |
| --- | --- |
| `reduced_energies()` | Reduced energies E/B as a function of the reduced potential V/B |
| `potential()`        | Potential values as a function of the angle |
| `energy()`           | Calculated eigenvalues |
| `energies_DEV()`     | NOT IMPLEMENTED |
| `convergence_DEV()`  | NOT IMPLEMENTED |
| `eigenvectors_DEV()` | NOT IMPLEMENTED |

---
"""


from .classes import *
import matplotlib.pyplot as plt
from copy import deepcopy


def reduced_energies(data:QExp):
    """Plots the reduced energy of the system, E/B, vs the reduced potential energy, V/B"""
    number_of_levels = data.systems[0].E_levels
    x = []
    for system in data.systems:
        x.append(system.potential_max_B)
    for i in range(number_of_levels):
        y = []
        for system in data.systems:
            y.append(system.eigenvalues_B[i])
        plt.plot(x, y, marker='', linestyle='-')
    plt.xlabel('V$_{B}$ / B')
    plt.ylabel('E / B')
    plt.title(data.comment)
    plt.show()


def potential(data):
    """Plot the potential values of the system.

    Input `data` can be a `QSys` or `QExp` object.
    """
    dataset = deepcopy(data)
    if isinstance(dataset, QSys):
        dataset = QExp(systems=[dataset], comment=data.comment)
    if not isinstance(dataset, QExp):
        raise TypeError(f'Requires a QExp or QSys object as input')
    for system in dataset.systems:
        plt.plot(system.grid, system.potential_values, marker='', linestyle='-')
    plt.xlabel('Angle / rad')
    plt.ylabel('Potential energy / meV')
    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
    plt.title(dataset.comment)
    plt.show()


def energy(data:QExp):
    """Plot the potential values of the QExp `data`."""
    dataset = deepcopy(data)
    V_colors = ['C0'] #...
    E_colors = ['red', 'purple', 'grey']  # To extend...
    E_linestyles = ['--', ':', '-.']
    edgecolors = ['tomato', 'purple', 'grey']

    V_linestyle = '-'

    title = dataset.comment
    ylabel_text = f'Energy / meV'
    xlabel_text = 'Angle / radians'

    plt.figure(figsize=(10, 6))
    plt.xlabel(xlabel_text)
    plt.ylabel(ylabel_text)

    plt.title(title)
    if not dataset.comment and dataset.systems[0].comment:
        plt.title(f'{dataset.systems[0].comment}')

    plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])

    unique_potentials = []
    unique_groups = []
    for i, system in enumerate(dataset.systems):
        V_color = V_colors[i % len(V_colors)]
        E_color = E_colors[i % len(E_colors)]
        E_linestyle = E_linestyles[i % len(E_linestyles)]
        edgecolor = edgecolors[i % len(edgecolors)]

        # Plot potential energy if it is unique
        if not any(np.array_equal(system.potential_values, value) for value in unique_potentials):
            unique_potentials.append(system.potential_values)
            plt.plot(system.grid, system.potential_values, color=V_color, linestyle=V_linestyle)

        # Plot eigenvalues
        if system.eigenvalues is not None:
            text_offset = 3 * len(unique_groups)
            if system.group not in unique_groups:
                unique_groups.append(system.group)
            for j, energy in enumerate(system.eigenvalues):
                plt.axhline(y=energy, color=E_color, linestyle=E_linestyle)
                plt.text(j%3*0.9 + text_offset, energy, f'$E_{{{j}}}$ = {round(energy,4):.04f}', va='top', bbox=dict(edgecolor=edgecolor, boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
            if len(dataset.get_groups()) > 1:
                plt.plot([], [], color=E_color, label=f'{system.group} Energies')  # Add to legend

    if len(dataset.get_groups()) > 1:
        plt.subplots_adjust(right=0.85)
        plt.legend(bbox_to_anchor=(1.1, 0.5), loc='center', fontsize='small')

    plt.show()


def energies_DEV(data, separate_plots:bool=False):
    """Plot the potential values of the system. NOT YET IMPLEMENTED

    Input `data` can be a `QSys` or `QExp` object.
    Separate plots with `separate_plots = True`.
    """
    dataset = deepcopy(data)
    if isinstance(dataset, QSys):
        dataset = QExp(systems=[dataset], comment=data.comment)
    if not isinstance(dataset, QExp):
        raise TypeError(f'Requires a QExp or QSys object as input')
    if separate_plots:
        for system in dataset.systems:
            new_data = QExp()
            new_data.comment = system.comment
            new_data.systems = [system]
            energy(new_data)
    else:  # Group data with the same potential_values and different element
        grouped_data = dataset.group_by_potential_values()
        print(f'energies plot: len = {len(dataset.systems)}')
        print(f'grouped: {len(grouped_data[0].systems)}')  # BUG: old systems are not overwritten
        for new_data in grouped_data:
            print('new_data')
            energy(new_data)


def convergence_DEV(data:QExp):
    '''Plots the energy convergence of the system. NOT YET IMPLEMENTED'''
    fig, ax1 = plt.subplots(figsize=(10, 6))

    E_color = 'C0'
    runtime_color = 'C3'
    yaxes_color = E_color

    converged_color_line = 'lightgrey'

    units = data.variables[0].units
    E_units = 'meV'
    if 'meV' in units or 'mev' in units:
        E_units = 'meV'
    elif 'eV' in units or 'ev' in units:
        E_units = 'eV'

    title = data.comment
    ylabel_text = f'Energy / {E_units}'
    xlabel_text = 'Grid Size'
    runtime_text = 'Runtime / s'

    legend_title = data.legend_title
    legend_title_position = data.legend_title_position
    check_E_threshold = data.check_E_threshold
    check_E_diff = data.check_E_diff
    check_E_level = data.check_E_level
    ideal_E = data.ideal_E
    if check_E_level is None:
        data.check_E_level = len(data.solutions[0].eigenvalues) - 1
        check_E_level = data.check_E_level
        ideal_E = data.get_ideal_E()


    textbox = dict(boxstyle='round', facecolor='white', edgecolor='lightgrey', alpha=0.5)
    textstr = ''

    textstr_position_x = 0.88
    textstr_position_y = 0.15
    textstr_alignment_h = 'right'
    textstr_alignment_v = 'bottom'

    if legend_title_position and isinstance(legend_title_position, list):
        textstr_position_x = data.legend_title_position[0]
        textstr_position_y = data.legend_title_position[1]
        textstr_alignment_h = data.legend_title_position[2]
        textstr_alignment_v = data.legend_title_position[3]

    energies = data.energies()
    energies_transposed = np.transpose(energies)
    plotted_energies = energies_transposed[check_E_level]
    gridsizes = data.gridsizes()
    runtimes = data.runtimes()

    if check_E_diff:
        plotted_energies = np.abs(plotted_energies - ideal_E)
        ylabel_text = 'Energy offset / |meV|'
        textstr_position_x = 0.5
        textstr_position_y = 0.85
        textstr_alignment_v = 'top'
        textstr_alignment_h = 'center'
    
    if not any(runtimes):
        yaxes_color = 'black'

    ax1.plot(gridsizes, plotted_energies, marker='o', linestyle='-', color=E_color)
    ax1.set_xlabel(xlabel_text)
    ax1.set_ylabel(ylabel_text, color=yaxes_color)
    ax1.tick_params(axis='y', labelcolor=yaxes_color)

    if ideal_E is not None:
        if check_E_diff:
            ax1.axhline(y=0, color='grey', linestyle='--')
        else:
            ax1.axhline(y=ideal_E, color='grey', linestyle='--')
            textstr += f'Ideal  E={ideal_E:.4f}\n'
    
    if check_E_threshold and (ideal_E is not None):
        if check_E_diff:
            abs_energies = energy
        else:
            abs_energies = np.abs(plotted_energies - ideal_E)
        for i, energy in enumerate(abs_energies):
            if energy < check_E_threshold:
                #ax1.plot(gridsizes[i], plotted_energies[i], marker=converged_marker, color=E_converged_color)
                ax1.axvline(x=gridsizes[i], color=converged_color_line, linestyle='--')
                textstr += f'Convergence threshold:  {check_E_threshold}\n'
                lower_limit, _ = ax1.get_ylim()
                ax1.text(gridsizes[i], lower_limit, str(gridsizes[i]), fontsize=10, verticalalignment='bottom', horizontalalignment='center')
                break

    if any(runtimes):
        ax2 = ax1.twinx()  # instantiate a second y-axis that shares the same x-axis
        ax2.set_ylabel(runtime_text, color=runtime_color)  # we already handled the x-label with ax1
        ax2.plot(gridsizes, runtimes, marker='o', linestyle='-', color=runtime_color)
        ax2.tick_params(axis='y', labelcolor=runtime_color)
        for i, energy in enumerate(plotted_energies):
            textstr += f'N={gridsizes[i]}   E={round(energy,4):.04f}   t={round(runtimes[i],2):.02f}'
            if i < len(plotted_energies) - 1:
                textstr += '\n'

    else:
        for i, energy in enumerate(plotted_energies):
            textstr += f'N={gridsizes[i]}   E={round(energy,4):.04f}\n'

    if legend_title is not False:
        if isinstance(legend_title, str):
            textstr = legend_title + '\n' + textstr
        fig.text(textstr_position_x, textstr_position_y, textstr, fontsize=10, verticalalignment=textstr_alignment_v, horizontalalignment=textstr_alignment_h, bbox=textbox)

    plt.title(title)
    plt.show()









def eigenvectors_DEV(data:QExp, levels=None, squared=False, scaling_factor=1):

    xlabel = 'Angle / radians'
    ylabel = 'Energy / meV'
    title = data.title
    V_color = 'lightblue'
    V_label = 'Potential'

    #energy_color = 'red'
    energy_edgecolor = 'lightgrey'
    energy_linestyle = ':'
    energy_label = 'E'

    eigenvector_linestyle = '--'

    # To square the eigenvectors
    if squared:
        eigenvector_label = 'Eigenvect$^2$ '
        square = 2
    else:
        eigenvector_label = 'Eigenvect '
        square = 1
    
    for i, potential in enumerate(data.set_of_potentials):

        # Transpose the 2D array so that each inner array represents a different eigenvector
        eigenvectors_transposed = np.transpose(data.set_of_eigenvectors[i])

        # Plot potential energy
        plt.figure(figsize=(10, 6))
        plt.plot(data.x, potential, color=V_color, label=V_label)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(f'{title} (#' + str(i+1) + ')' )
        if len(data.set_of_potentials) == 1:
            plt.title(f'{title}')
        plt.xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi],
                   ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
        for j, energy in enumerate(data.set_of_energies[i]):
            if levels is not None and j not in levels:
                continue

            color = 'C' + str(j)

            E_label = energy_label + str(j)
            plt.axhline(y=energy, linestyle=energy_linestyle, color=color, label=E_label)
            plt.text(j%3*0.9, energy, f'E$_{j}$ = {energy:.4f}', va='top', bbox=dict(edgecolor=energy_edgecolor, boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

            eigenvect_label = eigenvector_label + str(j)
            eigenvector = scaling_factor*eigenvectors_transposed[j]**square
            plt.plot(data.x, eigenvector, linestyle=eigenvector_linestyle, label=eigenvect_label, color=color)

        plt.subplots_adjust(right=0.85)
        plt.legend(bbox_to_anchor=(1.1, 0.5), loc='center', fontsize='small')
        plt.text(1.03, 0.9, f'Eigenvects\nscaled x{scaling_factor}', transform=plt.gca().transAxes)
        plt.show()



