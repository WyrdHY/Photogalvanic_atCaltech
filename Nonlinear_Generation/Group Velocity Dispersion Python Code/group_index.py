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

#This is a function specifically designed for reading the dat type exported from Comsol
#However, depending on the content you select to output in Comsol, the code needs to be adjusted

file_path = r"C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech\SHG\Group Velocity Dispersion Python Code\data\4x12_FHD.dat"
outputname = "4x12_FHD"
folder = "4x12um"
width = 12
#I defined this to run it as my wish.
intersection_enable = 0
gate1 = 0

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


def find_intersections(x):
    y0 = ng_interpolator(500)
    return ng_interpolator(x) - y0
    print(y0)

initial_guesses = [500, 1000]
if intersection_enable:
    intersections = fsolve(find_intersections, initial_guesses)



# Plot the non-interpolated and interpolated ng vs. wavelength
plt.figure(dpi=300)
plt.plot(wavelength_nm, ng, 'o', markersize=0.8)
plt.plot(fine_wavelength_grid, fine_ng, '-', label=f'ng_{outputname}',linewidth=0.5)
if intersection_enable:
    plt.axhline(y=y0, color='r', linestyle='--', label=f'y0 = ng(780 nm) = {y0:.4f}',linewidth=0.5)
plt.plot(wavelength_nm,neff,'o', label=f'neff_{outputname}', markersize=0.8)
if intersection_enable:
    for x in intersections:
        y = ng_interpolator(x)
        plt.plot(x, y, 'ro',markersize=3)
        plt.text(x, y, f'({x:.1f}, {y:.4f})', fontsize=8, ha='center')

plt.xlabel('Wavelength (nm)')
plt.ylabel('ng')
plt.title('Top ng and bottom neff vs. Wavelength')
plt.legend()
relative_path_png = os.path.join(os.path.dirname(__file__), 'result',f'{folder}' ,f'{outputname}.png')
plt.savefig(relative_path_png)
plt.show()



#also save it as an interactive plot for detailed investigation

fig = go.Figure()

# Original ng data
fig.add_trace(go.Scatter(
    x=wavelength_nm,
    y=ng,
    mode='markers',
    name='Original ng',
    marker=dict(size=4)
))

# Interpolated ng data
fig.add_trace(go.Scatter(
    x=fine_wavelength_grid,
    y=fine_ng,
    mode='lines',
    name='Interpolated ng',
    line=dict(width=1)
))

# Horizontal line at y0

if intersection_enable:
    fig.add_trace(go.Scatter(
        x=[min(wavelength_nm), max(wavelength_nm)],
        y=[y0, y0],
        mode='lines',
        name=f'y0 = ng(780 nm) = {y0:.4f}',
        line=dict(dash='dash', color='red', width=1)
    ))

fig.add_trace(go.Scatter(
    x=wavelength_nm,
    y=neff,
    mode='lines',
    name=f'neff',
    line=dict(dash='dash', color='green', width=1)
))

fig.add_trace(go.Scatter(
    x=wavelength_nm,
    y=neff,
    mode='markers',
    name=f'neff dot',
    marker=dict(size=4)
))

# Intersection points
if intersection_enable:
    for x in intersections:
        y = ng_interpolator(x)
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            text=[f'({x:.1f}, {y:.4f})'],
            textposition='top right',
            name=f'Intersection ({x:.1f}, {y:.4f})',
            marker=dict(color='red', size=6)
        ))

# Update layout
fig.update_layout(
    title='Group Index vs. Wavelength',
    xaxis_title='Wavelength (nm)',
    yaxis_title='ng',
    showlegend=True
)

relative_path = os.path.join(os.path.dirname(__file__), 'result',f'{folder}', f'{outputname}.html')


fig.write_html(relative_path)
webbrowser.open_new_tab(relative_path)

wavelengthold = wavelength_nm
neffold = neff
ngold = ng
fineold_nm = fine_wavelength_grid
fineold_ng = fine_ng

if gate1: 
    file_path = r"C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech\SHG\Group Velocity Dispersion Python Code\data\NEW_dispersion_Ge.dat"
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

    y0 = ng_interpolator(500)
    def find_intersections(x):
        return ng_interpolator(x) - y0
    initial_guesses = [500, 1000]
    if intersection_enable:
        intersections = fsolve(find_intersections, initial_guesses)


    print(y0)
    # Plot the non-interpolated and interpolated ng vs. wavelength
    plt.figure(dpi=300)
    plt.plot(wavelength_nm, ng, 'o', label='(4x12)', markersize=0.8,color = 'red')
    plt.plot(fine_wavelength_grid, fine_ng, '-', linewidth=0.5,color = 'red')
    plt.plot(wavelength_nm,neff,'o', markersize=0.8,color = 'red')

    plt.plot(wavelengthold, ngold, 'o', label=f'(4x{width})', markersize=0.8,color = 'green')
    plt.plot(fineold_nm, fineold_ng, '-', linewidth=0.5,color = 'green')
    plt.plot(wavelengthold,neffold,'o', markersize=0.8,color = 'green')




    if intersection_enable:
        plt.axhline(y=y0, color='r', linestyle='--', label=f'y0 = ng(780 nm) = {y0:.4f}',linewidth=0.5)
        for x in intersections:
            y = ng_interpolator(x)
            plt.plot(x, y, 'ro',markersize=3)
            plt.text(x, y, f'({x:.1f}, {y:.4f})', fontsize=8, ha='center')

    plt.xlabel('Wavelength (nm)')
    plt.ylabel('ng')
    plt.title('Group Index vs. Wavelength. Bottom two are neff. Top two are ng')
    plt.legend()
    relative_path_png = os.path.join(os.path.dirname(__file__), 'result',f'{folder}' ,f'{outputname}_compare.png')
    plt.savefig(relative_path_png)
    plt.show()



    #also save it as an interactive plot for detailed investigation

    fig = go.Figure()

    # Original ng data
    fig.add_trace(go.Scatter(
        x=wavelength_nm,
        y=ng,
        mode='markers',
        name = 'ng(4x12)',
        marker=dict(size=4)
    ))

    # Interpolated ng data
    fig.add_trace(go.Scatter(
        x=fine_wavelength_grid,
        y=fine_ng,
        mode='lines',
        #name='Interpolated ng(4x12)',
        line=dict(width=1)
    ))

    # Horizontal line at y0

    if intersection_enable:
        fig.add_trace(go.Scatter(
            x=[min(wavelength_nm), max(wavelength_nm)],
            y=[y0, y0],
            mode='lines',
            name=f'y0 = ng(780 nm) = {y0:.4f}',
            line=dict(dash='dash', color='red', width=1)
        ))

    fig.add_trace(go.Scatter(
        x=wavelength_nm,
        y=neff,
        mode='lines',
        name=f'neff(4x12)',
        line=dict(dash='dash', color='green', width=1)
    ))

    fig.add_trace(go.Scatter(
        x=wavelength_nm,
        y=neff,
        mode='markers',
        name=f'neff dot(4x12)',
        marker=dict(size=4)
    ))

    # Intersection points
    if intersection_enable:
        for x in intersections:
            y = ng_interpolator(x)
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                text=[f'({x:.1f}, {y:.4f})'],
                textposition='top right',
                name=f'Intersection ({x:.1f}, {y:.4f})',
                marker=dict(color='red', size=6)
            ))

    # Update layout
    fig.update_layout(
        title='Group Index vs. Wavelength',
        xaxis_title='Wavelength (nm)',
        yaxis_title='ng',
        showlegend=True
    )

    relative_path = os.path.join(os.path.dirname(__file__), 'result',f'{folder}', f'{outputname}/_compare.html')


    fig.write_html(relative_path)
    webbrowser.open_new_tab(relative_path)
