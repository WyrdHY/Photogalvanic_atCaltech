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




def load_comsol_data(file_path):
    # Initialize a dictionary to store the data
    data_dict = {}

    # Define the column names
    column_names = ["Effective_mode_index", "Eigenvalue", "real_ewfd_neff", "Frequency_Hz"]

    # Read the file and process each line
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines[5:]:  # Skip header lines
            # Split the line into parts, handling the complex numbers properly
            parts = line.strip().split(maxsplit=4)  # Split only the first 4 parts to handle complex numbers
            daddy = int(parts[0])
            Effective_mode_index = parts[1]
            Eigenvalue = parts[2]
            real_ewfd_neff = parts[3]
            Frequency_Hz = parts[4]

            # Create a DataFrame row
            row_df = pd.DataFrame([[Effective_mode_index, Eigenvalue, real_ewfd_neff, Frequency_Hz]], columns=column_names)
            
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

    c = Decimal('3e8')
    getcontext().prec = 50

    frequencies_decimal = combined_df['Frequency_Hz'].apply(lambda f: Decimal(str(f)) if not pd.isna(f) else Decimal('NaN'))

    wavelength_nm = frequencies_decimal.apply(lambda f: (c / f) * Decimal('1e9') if f != Decimal('NaN') else Decimal('NaN'))
    wavelength_nm = np.array(wavelength_nm.tolist(), dtype=np.float64)
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


# File paths
file_path1 = r"C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech\SHG\Group Velocity Dispersion Python Code\data\4x12_FHD.dat"
file_path2 = r"C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech\SHG\Group Velocity Dispersion Python Code\data\4x4_FHD.dat"
#file_path3 = r"C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech\SHG\Group Velocity Dispersion Python Code\data\NEW_dispersion_Ge.dat"  # this is 4x12 dimension

# Load data and generate plots
wavelength_nm1, neff1, fine_wavelength_grid1, fine_ng1, ng1 = give_me_ng_neff(file_path1)
wavelength_nm2, neff2, fine_wavelength_grid2, fine_ng2, ng2 = give_me_ng_neff(file_path2)
#wavelength_nm3, neff3, fine_wavelength_grid3, fine_ng3, ng3 = give_me_ng_neff(file_path3)

# Create figure and axes
fig, ax = png_plot(wavelength_nm1, neff1, ng1, fine_wavelength_grid1, fine_ng1, '4x12_FHD')
fig, ax = png_plot(wavelength_nm2, neff2, ng2, fine_wavelength_grid2, fine_ng2, '4x4_FHD', fig, ax)
#fig, ax = png_plot(wavelength_nm3, neff3, ng3, fine_wavelength_grid3, fine_ng3, '4x12', fig, ax)
output_file = r'C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech\SHG\Group Velocity Dispersion Python Code\result\comparison_plot_FHD.png'
fig.set_size_inches(12, 8)

fig.savefig(output_file, dpi=800)  # Set DPI for the saved figure

plt.show()
plt.show()