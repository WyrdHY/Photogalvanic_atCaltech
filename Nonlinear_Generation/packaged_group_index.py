import re
import os
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal, getcontext
from scipy.interpolate import interp1d
import plotly.graph_objects as go
import plotly.io as pio
from scipy.optimize import fsolve
import pandas as pd
import webbrowser
import itertools
from scipy.constants import c,pi #speed of light #Pi

#This code is used to plot:
#delta beta(w) = beta(w)-beta(830) - (w-830)/vg(830)
#vg = c/ng(830)



def load_comsol_data(file_path):
    # Initialize a dictionary to store the data
    data_dict = {}

    # Define the column names
    column_names = ["Effective_mode_index", "real_ewfd_neff", "Wavelength_in_free_space", "Propagation_constant"]

    # Read the file and process each line
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[5:]:  # Skip header lines
            # Split the line into parts, handling the complex numbers properly
            parts = line.strip().split(maxsplit=4)  # Split only the first 4 parts to handle complex numbers
            daddy = int(parts[0])
            Effective_mode_index = parts[1]
            real_ewfd_neff = parts[2]
            Wavelength_in_free_space = parts[3]
            Propagation_constant = parts[4]

            # Create a DataFrame row
            row_df = pd.DataFrame([[Effective_mode_index, real_ewfd_neff, Wavelength_in_free_space, Propagation_constant]], columns=column_names)
            
            # Add to the dictionary
            if daddy not in data_dict:
                data_dict[daddy] = row_df
            else:
                data_dict[daddy] = pd.concat([data_dict[daddy], row_df], ignore_index=True)
    return data_dict
def give_me_ng_neff(file_path):
    comsol_data = load_comsol_data(file_path)
    keep_only_max = {}
    for a in comsol_data.keys():
        df = comsol_data[a]
        df['real_ewfd_neff'] = pd.to_numeric(df['real_ewfd_neff'], errors='coerce')
        max_index = df['real_ewfd_neff'].idxmax()
        max_row = df.loc[[max_index]]
        keep_only_max[a] = max_row

        
    combined_df = pd.concat(keep_only_max.values(), ignore_index=True)
    combined_df['Frequency_Hz'] = pd.to_numeric(combined_df['Frequency_Hz'], errors='coerce')
    combined_df['real_ewfd_neff'] = pd.to_numeric(combined_df['real_ewfd_neff'], errors='coerce')

    
    wavelength_nm = combined_df['Wavelength_in_free_space']
    neff = combined_df['real_ewfd_neff'].to_numpy()
    dndlambda = np.gradient(neff, wavelength_nm)
    ng = neff - wavelength_nm*dndlambda
    print(np.min(wavelength_nm), np.max(wavelength_nm))

    #Interpolate ng(w)
    fine_wavelength_grid = np.linspace(np.min(wavelength_nm), np.max(wavelength_nm), 8000)
    ng_interpolator = interp1d(wavelength_nm, ng, kind='cubic')
    fine_ng = ng_interpolator(fine_wavelength_grid)
    return wavelength_nm,neff,fine_wavelength_grid,fine_ng,ng
def png_plot(wavelength_nm, neff, ng, fine_wavelength_grid, fine_ng, name, fig=None, ax=None, color=None):
    if fig is None or ax is None:
        fig, ax = plt.subplots()

    if color is None:
        color = next(ax._get_lines.prop_cycler)['color']

    # Plot ng data points and interpolated ng line with the same color
    ax.plot(wavelength_nm, ng, 'o', markersize=0.8, color=color)
    ax.plot(fine_wavelength_grid, fine_ng, '-', color=color, linewidth=0.5)

    # Plot neff data points and line connecting them
    ax.plot(wavelength_nm, neff, 'o-', markersize=.8, color=color, label=f'{name}', linewidth=0.5)

    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('ng')
    ax.set_title('n_group(Up) Or n_eff(down) vs. Wavelength')
    ax.legend()
    
    return fig, ax
def key(file_path):
    comsol_data = load_comsol_data(file_path)
    keep_only_max = {}
    for a in comsol_data.keys():
        df = comsol_data[a]
        df['real_ewfd_neff'] = pd.to_numeric(df['real_ewfd_neff'], errors='coerce')
        max_index = df['real_ewfd_neff'].idxmax()
        max_row = df.loc[[max_index]]
        keep_only_max[a] = max_row
    combined_df = pd.concat(keep_only_max.values(), ignore_index=True)

    combined_df['real_ewfd_neff'] = pd.to_numeric(combined_df['real_ewfd_neff'], errors='coerce')
    combined_df['Propagation_constant'] = pd.to_numeric(combined_df['Propagation_constant'], errors='coerce')
    combined_df['Wavelength_in_free_space'] = pd.to_numeric(combined_df['Wavelength_in_free_space'], errors='coerce')

    wavelength_nm = combined_df['Wavelength_in_free_space'].to_numpy()
    neff = combined_df['real_ewfd_neff'].to_numpy()
    beta = combined_df['Propagation_constant'].to_numpy()
    return wavelength_nm,neff,beta
def inter_ng(wavelength_nm,neff,omega=0):
    dndlambda = np.gradient(neff, wavelength_nm)
    ng = neff - wavelength_nm*dndlambda
    # Interpolate it
    #print(f"max and min = {np.min(wavelength_nm)} ,,, {np.max(wavelength_nm)}")
    fine_wavelength_grid = np.linspace(np.min(wavelength_nm), np.max(wavelength_nm), 18000)
    ng_interpolator = interp1d(wavelength_nm, ng, kind='cubic')
    fine_ng = ng_interpolator(fine_wavelength_grid)

    if omega==0:
        return fine_wavelength_grid,fine_ng
    else:
        return ng_interpolator(omega)
def inter_beta(wavelength_nm,beta,omega=0):
    # Interpolate it
    #print(f"max and min wavelength are {np.min(wavelength_nm)}, {np.max(wavelength_nm)}")
    fine_wavelength_grid = np.linspace(np.min(wavelength_nm), np.max(wavelength_nm), 8000)
    beta_interpolator = interp1d(wavelength_nm, beta, kind='cubic')
    fine_beta = beta_interpolator(fine_wavelength_grid)
    if omega==0:
        return fine_wavelength_grid,fine_beta
    else:
        return beta_interpolator(omega)
def process_file(filepath, label):
    temp = key(filepath)
    vg830 = c / inter_ng(temp[0], temp[1], 830)
    beta830 = inter_beta(temp[0], temp[2], 830)
    w_base, beta_base = inter_beta(temp[0], temp[2])
    delta_beta = beta_base - beta830 - 2 * np.pi * (c / w_base - c / 830) / vg830 * 1e9

    zero_crossings = np.where(np.diff(np.sign(delta_beta)))[0]
    w_zero_crossings = []
    delta_beta_zero_crossings = []
    for i in zero_crossings:
        w1 = w_base[i]
        w2 = w_base[i + 1]
        beta1 = delta_beta[i]
        beta2 = delta_beta[i + 1]
        w_zero_crossing = w1 - beta1 * (w2 - w1) / (beta2 - beta1)
        w_zero_crossings.append(w_zero_crossing)
        delta_beta_zero_crossings.append(0)  # Zero crossing is at delta_beta = 0

    return w_base, delta_beta, w_zero_crossings, delta_beta_zero_crossings, label
###############################################################################################################################
# Below is specifically for large_simulation 
def load_large(file_path):
    # Initialize a dictionary to store the data
    data_dict = {}
    
    # Define the column names
    column_names = ["Effective_mode_index", "real_ewfd_neff", "Wavelength_in_free_space", "Propagation_constant"]

    # Read the file and process each line
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[5:]:  # Skip header lines
            # Split the line into parts, handling the complex numbers properly
            parts = line.strip().split(maxsplit=7)  # Split only the first 4 parts to handle complex numbers
            daddy = int(parts[3])
            Effective_mode_index = parts[4]
            real_ewfd_neff = parts[5]
            Wavelength_in_free_space = parts[6]
            Propagation_constant = parts[7]

            # Create a DataFrame row
            row_df = pd.DataFrame([[Effective_mode_index, real_ewfd_neff, Wavelength_in_free_space, Propagation_constant]], columns=column_names)
            
            # Add to the dictionary
            if daddy not in data_dict:
                data_dict[daddy] = row_df
            else:
                data_dict[daddy] = pd.concat([data_dict[daddy], row_df], ignore_index=True)
    return data_dict
def key_large(file_path):
    comsol_data = load_large(file_path)
    keep_only_max = {}
    for a in comsol_data.keys():
        df = comsol_data[a]
        df['real_ewfd_neff'] = pd.to_numeric(df['real_ewfd_neff'], errors='coerce')
        max_index = df['real_ewfd_neff'].idxmax()
        max_row = df.loc[[max_index]]
        keep_only_max[a] = max_row
    combined_df = pd.concat(keep_only_max.values(), ignore_index=True)

    combined_df['real_ewfd_neff'] = pd.to_numeric(combined_df['real_ewfd_neff'], errors='coerce')
    combined_df['Propagation_constant'] = pd.to_numeric(combined_df['Propagation_constant'], errors='coerce')
    combined_df['Wavelength_in_free_space'] = pd.to_numeric(combined_df['Wavelength_in_free_space'], errors='coerce')

    wavelength_nm = combined_df['Wavelength_in_free_space'].to_numpy()
    neff = combined_df['real_ewfd_neff'].to_numpy()
    beta = combined_df['Propagation_constant'].to_numpy()
    return wavelength_nm,neff,beta
def process_large_file(filepath, label):
    temp = key_large(filepath)
    vg830 = c / inter_ng(temp[0], temp[1], 830)
    beta830 = inter_beta(temp[0], temp[2], 830)
    w_base, beta_base = inter_beta(temp[0], temp[2])
    delta_beta = beta_base - beta830 - 2 * np.pi * (c / w_base - c / 830) / vg830 * 1e9

    zero_crossings = np.where(np.diff(np.sign(delta_beta)))[0]
    w_zero_crossings = []
    delta_beta_zero_crossings = []
    for i in zero_crossings:
        w1 = w_base[i]
        w2 = w_base[i + 1]
        beta1 = delta_beta[i]
        beta2 = delta_beta[i + 1]
        w_zero_crossing = w1 - beta1 * (w2 - w1) / (beta2 - beta1)
        w_zero_crossings.append(w_zero_crossing)
        delta_beta_zero_crossings.append(0)  # Zero crossing is at delta_beta = 0

    return w_base, delta_beta, w_zero_crossings, delta_beta_zero_crossings, label
###############################################################################################################################    
single = 0
multiple = 0
plotly = 0
large = 1


if single:
    filepath = r"D:\Caltech\photogalvanic_atCaltech\Nonlinear_Generation\Raw data from Comsol\For_Real\6000_2000.dat"
    temp = key(filepath)
    print("you are here 137")
    vg830 = c/inter_ng(temp[0],temp[1],830)
    beta830 = inter_beta(temp[0],temp[2],830)
    w_base,beta_base = inter_beta(temp[0],temp[2])
    print(f'asdkjlfhasdf {w_base}')
    print(f"vg830 is {vg830}")
    print(f"beta830 is {beta830}")
    delta_beta = beta_base- beta830 - 2*pi*(c/w_base  - c/830)/vg830*1e9

    print(max(delta_beta))
    zero_crossings = np.where(np.diff(np.sign(delta_beta)))[0]
    w_zero_crossings = []
    w_zero_crossings = []
    delta_beta_zero_crossings = []
    for i in zero_crossings:
        w1 = w_base[i]
        w2 = w_base[i + 1]
        beta1 = delta_beta[i]
        beta2 = delta_beta[i + 1]
        w_zero_crossing = w1 - beta1 * (w2 - w1) / (beta2 - beta1)
        w_zero_crossings.append(w_zero_crossing)
        delta_beta_zero_crossings.append(0)  # Zero crossing is at delta_beta = 0

    plt.figure(dpi=300)

    for xc, yc in zip(w_zero_crossings[0:2], delta_beta_zero_crossings[0:2]):
        plt.plot(xc, yc, 'kx', markersize=10)  # Cross marker at zero crossings
        plt.text(xc, yc, f'({xc:.2f}, {yc:.1f})', rotation=0, verticalalignment='bottom', horizontalalignment='right', fontsize=8, color='black')


    plt.plot(w_base, delta_beta/100,label='6000_2000')
    plt.axhline(y=0, color='r', linestyle='--')  # Add horizontal line at y=0
    plt.title(r'$\Delta \beta$')  # LaTeX formatted title
    plt.ylim(-65, 2550)
    plt.xlabel(r'Wavelength (nm)', fontsize=12)  # LaTeX formatted x-axis label
    plt.ylabel(r'$\Delta \beta$ (mm$^{-1}$)', fontsize=12)  # LaTeX formatted y-axis label
    plt.legend()
    plt.show()

    if plotly: 
            # Create the plot using Plotly
        fig = go.Figure()

        # Add the zero crossings as cross markers
        fig.add_trace(go.Scatter(
            x=w_zero_crossings,
            y=delta_beta_zero_crossings,
            mode='markers+text',
            marker=dict(color='black', size=10, symbol='x'),
            text=[f'({xc:.2f}, {yc:.1f})' for xc, yc in zip(w_zero_crossings, delta_beta_zero_crossings)],
            textposition="bottom right",
            name='Zero Crossings'
        ))

        # Add the delta_beta curve
        fig.add_trace(go.Scatter(
            x=w_base,
            y=-delta_beta / 100,
            mode='lines',
            name='1700nm * 500nm',
            line=dict(color='blue')
        ))

        # Add horizontal line at y=0
        fig.add_shape(type="line",
                    x0=min(w_base), y0=0, x1=max(w_base), y1=0,
                    line=dict(color="red", width=2, dash="dash"))

        # Update layout with LaTeX formatted title and labels
        fig.update_layout(
            title=r'$\Delta \beta$',
            xaxis_title=r'Wavelength (nm)',
            yaxis_title=r'$\Delta \beta$ (mm$^{-1}$)',
            legend=dict(x=0.01, y=0.99),
            template="plotly_white"
        )

        # Show the plot
        fig.show()

        # Optionally, save the plot as an HTML file
        fig.write_html('delta_beta_plot.html')

        webbrowser.open('delta_beta_plot.html')

if multiple: 
    # Process the first file
    filepath1 = r"D:\Caltech\photogalvanic_atCaltech\Nonlinear_Generation\Raw data from Comsol\For_Real\2000_2000.dat"
    w_base1, delta_beta1, w_zero_crossings1, delta_beta_zero_crossings1, label1 = process_file(filepath1, '2000 x 2000 nm')

    # Process the second file
    filepath2 = r"D:\Caltech\photogalvanic_atCaltech\Nonlinear_Generation\Raw data from Comsol\For_Real\4000_2000.dat"
    w_base2, delta_beta2, w_zero_crossings2, delta_beta_zero_crossings2, label2 = process_file(filepath2, '4000 x 2000 nm')

    # Process the third file
    filepath3 = r"D:\Caltech\photogalvanic_atCaltech\Nonlinear_Generation\Raw data from Comsol\For_Real\6000_2000.dat"
    w_base3, delta_beta3, w_zero_crossings3, delta_beta_zero_crossings3, label3 = process_file(filepath3, '6000 x 2000 nm')

    # Plot the results
    plt.figure(dpi=300)

    # Plot the first dataset
    plt.plot(w_base1, delta_beta1 / 100, label=label1)
    if False:
        for xc, yc in zip(w_zero_crossings1[0:1], delta_beta_zero_crossings1[0:1]):
            plt.plot(xc, yc, 'kx', markersize=6)  # Cross marker at zero crossings
            plt.text(xc, yc, f'({xc:.2f}, {yc:.2f})', rotation=0, verticalalignment='top', horizontalalignment='right', fontsize=8, color='black')

    # Plot the second dataset
    plt.plot(w_base2, delta_beta2 / 100, label=label2)
    if False:
        for xc, yc in zip(w_zero_crossings2[0:2], delta_beta_zero_crossings2[0:2]):
            plt.plot(xc, yc, 'kx', markersize=6)  # Cross marker at zero crossings
            plt.text(xc, yc, f'({xc:.2f}, {yc:.2f})', rotation=0, verticalalignment='bottom', horizontalalignment='right', fontsize=8, color='black')
    plt.plot(w_base3, delta_beta3 / 100, label=label3)

    plt.axhline(y=0, color='r', linestyle='--')  # Add horizontal line at y=0
    plt.title(r'$\Delta \beta$, THOX(Extended to 300nm), base substrate is 450nm')  # LaTeX formatted title
    plt.ylim(-65, 750)
    plt.xlabel(r'Wavelength (nm)', fontsize=12)  # LaTeX formatted x-axis label
    plt.ylabel(r'$\Delta \beta$ (mm$^{-1}$)', fontsize=12)  # LaTeX formatted y-axis label
    plt.legend()
    
    plt.show()

if large: 
    for sub in [250,500,750,1000]:
        for height in [500,1000,1500]:

            target = [1,2,4,6]
            
            plt.figure(dpi=300)
            for i in target:
                filepath = f"D:\\Caltech\\photogalvanic_atCaltech\\Nonlinear_Generation\\Raw data from Comsol\\For_Real\\Large Simulation\\sub_{sub}_h_{height}\\rate={i}.dat"
                w_base1, delta_beta1, w_zero_crossings1, delta_beta_zero_crossings1, label1 = process_large_file(filepath, f'{height*i} x {height}, ')
                w_zero_crossings_array1 = np.array(w_zero_crossings1)
                w_zero_crossings_array1.sort()
                if len(w_zero_crossings_array1)==0:
                    name = 'DNE'
                else:
                    name = f'{w_zero_crossings_array1[0]:.2f}'
                plt.plot(w_base1, delta_beta1 / 100, label=label1 + f' {name} nm')
            plt.axhline(y=0, color='black', linestyle='--')  # Add horizontal line at y=0
            plt.gcf()
            plt.title((r'$\Delta \beta$'+ f' base substrate: {sub}nm'))  # LaTeX formatted title
            plt.legend(loc='upper right')
            plt.ylim(-765,650)
            plt.xlim(300,1000)
            plt.xlabel(r'Wavelength (nm)', fontsize=12)  # LaTeX formatted x-axis label
            plt.ylabel(r'$\Delta \beta$ (mm$^{-1}$)', fontsize=12)  # LaTeX formatted y-axis label
            save_address = f'D:\\Caltech\\photogalvanic_atCaltech\\Nonlinear_Generation\\Result\\German_SiO2\\test_save\\sub_{sub}_height_{height}.png'
            plt.savefig(save_address, bbox_inches='tight', pad_inches=0, dpi=400)
            #plt.show()
print('Finished')
