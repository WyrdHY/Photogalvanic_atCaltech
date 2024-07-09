import numpy as np
import matplotlib.pyplot as plt

a = 5 #for delta
b= 1.0 #for z
switch = False
filepath = f'/Users/ericyan/Desktop/Caltech_Paper/Plot/delta={a} z={b}.png'


if switch ==True :
    # Define the function
    def f(z, delta):
        return (np.sin(delta * z / 2)**2) / delta**2

    # Create the figure and subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

    # Plot 1: f(z, δ) at a specific δ
    # Set a specific value for delta
    delta = a  # You can change this value

    # Create an array of z values
    z = np.linspace(-10, 10, 400)

    # Compute the function values
    F = f(z, delta)

    # Plot the function
    ax1.plot(z, F, label=f'δ = {delta}')
    ax1.set_xlabel('z', fontsize=24)
    ax1.set_ylabel('Intensity(z, δ)', fontsize=24)
    #ax1.set_title(f'I(z, δ = {delta})', fontsize=24)
    ax1.legend(fontsize=24)
    ax1.tick_params(axis='both', which='major', labelsize=24)

    # Plot 2: f(z, δ) at a specific z
    # Set a specific value for z
    z = b # You can change this value

    # Create an array of delta values
    delta = np.linspace(-25, 25, 400)
    # To avoid division by zero at delta = 0, replace 0 with a very small number
    delta[delta == 0] = 1e-10

    # Compute the function values
    F = f(z, delta)

    # Plot the function
    ax2.plot(delta, F, label=f'z = {z}')
    ax2.set_xlabel('δ', fontsize=24)
    ax2.set_ylabel('Intensity(z, δ)', fontsize=24)
    #ax2.set_title(f'I(z = {z}, δ)', fontsize=24)
    ax2.legend(fontsize=24)
    ax2.tick_params(axis='both', which='major', labelsize=24)

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(filepath, dpi=500)
    #plt.show()
else: 
    def f(z, delta):
        return (np.sin(delta * z / 2)**2) / delta**2
        # Set the specific values for delta
    delta_values = [0.1, 0.3, 0.5, 1, 3]

    # Create an array of z values
    z = np.linspace(-15, 15, 400)

    # Create the figure
    plt.figure(figsize=(12, 8))

    # Plot the function for each delta
    for delta in delta_values:
        F = f(z, delta)
        plt.plot(z, F, label=f'δ = {delta}')

    # Add labels and title
    plt.xlabel('z', fontsize=24)
    plt.ylabel('Intensity(z, δ)', fontsize=24)
    #plt.title('Intensity vs. z for different δ values', fontsize=24)
    plt.legend(fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)
    plt.ylim(0,12)

    # Save the plot
    filepath = '/Users/ericyan/Desktop/Caltech_Paper/Plot/Intensity_vs_z_multiple_delta.png'
    plt.tight_layout()
    plt.savefig(filepath, dpi=500)

