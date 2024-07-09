

# Interim Report #1 : Photogalvanic Effect: 

For detailed, please visit my github repo for this:
    https://github.com/WyrdHY/Photogalvanic_atCaltech

***All of the reference are included in the old_school and new_school folder. I divided them according to the timeline. Before 2000, they are classified as old school as people are discovering and trying to offer theory explaining photo-galvanic effect. After 2000, they are classified as new school as mature mathematical model has been established and people are trying to, instead of understand it, trying to utilize it.***



Motivation
---
In 1986, people first observed second harmonic generation in glass fiber. This phenomena is not supposed to happen in glass. To explain this phenomena, people have raised many models to explain it. Currently, the most prevailing one is photogalvanic effect. 

Photogalvanic effect can be thought as a function that transforms a material from no chi2 to yes chi2. My surf project aims to generate chi2 in GeO2-SiO2 ring resonators and produces SHG. 

Let's precisely define the situation before getting into technical details. 

## Beginning of the puzzle: What do people observe in 1986 

In 1986, when a glass fiber is pumped by pulse laser at 1064nm, people observed 532nm light inside the fiber along with 1064nm. [_photogalvanic_atCaltech\old_school\1986 - first observe SHG.pdf_] The frequency of the light doubles, which proves the existence of second harmonic generation inside the fiber. The key criteria for SHG to happen is the fiber needs to have non-zero chi2. However, naturally, due to centrosymmetric structure of fiber's material, it does not have chi2 that could support SHG. The existence of 532nm light inside fiber supports that the fiber, after pumped by pulse laser at 1064nm for a long time, has chi2. 

In addition, when imaged by two-photon microscopy, people discovered that not the whole fiber contains chi2. In fact, the chi2 occurs on the fiber like an interference pattern-101010101010. [_photogalvanic_atCaltech\old_school\grating_phasematch_auto.pdf_]. This means that the material property of the fiber(GeO2-SiO2) has been modified spatially and periodically. 


## Photogalvanic Effect:

This is a semi-classical model. We do not quantized the electric field, but treat them as a function f(x,t). The material GeO2-SiO2 is modelled as a two level system between defect state and conduction band. 

     Defect: places inside the crystal where locally does not obey crystal symmetry. This will lead to a local hamiltonian coupled to the global hamiltonian. In addition, if the defect is too much, the local hamiltonian will no longer be treated as local and effects similar to orbit hybridization could happen! 

Another concept important is: 

    Defect State: Defect state is just the eigenstate of the local hamiltonian. 

Now this is just a simple perturbation problem for a two level system: Your lower level is the defect state and your higher level is the conduction band[_photogalvanic_atCaltech\old_school\1991 - OL - Model for second-harmonic generation in glass optical fibers based on asymmetric photoelectron emission from defect sites.pdf_]. 

The perturbation comes from E(w) and E(2w), and the solved transition probability is uneven between defect state to conduction band / band to defect state. 

What's new is that the electrons in the conduction band will then be trapped by another defect state2, instead of going back to the original defect state1. In this case, we have electron donor and electron receiver that could establish charge separation. The charge separation will then establish a local static electric field as long as the defect state2 still traps the electrons. This local E field will, with the material intrinsic chi3, formed a rank-3 tensor that effectively served as chi2. 

Since the uneven transitions rates' mathematical expression looks like $\frac{E(w) + E(2w)}{E(w) - E(2w)}$, and chi2 is proportional to it. The generated chi2 pattern matches with the interference pattern between w and 2w wave. In addition, this also automatically matches the phase-match condition necessary for SHG generation[_photogalvanic_atCaltech\old_school\grating_phasematch_auto.pdf_]

## My Task

- Generate photogalvanic chi2 grating in waveguide(GeO2-SiO2) under 1064nm pulse
- Generate photogalvanic chi2 grating in ring resonator(GeO2-SiO2) under 1064nm CW

I am currently dealing with the first one. Several problems: 
- Absorption peak at 1064nm is quite week for GeO2-SiO2. Therefore, the time it takes to ingrate the grating might be very long.
- The group velocity dispersion(GVD) needs to match for SHG and fundamental wave. This requires a careful design of waveguide. I am running COMSOL simulation to get the GVD and see if they match.
# Current Work  
First, I aims to reproduce a result from the published paper from NIST [_photogalvanic_atCaltech\new_school\2019 - NP - Self-organized nonlinear gratings for ultrafast nanophotonics.pdf_]. 

Here is their simulation result: 

[![NIST](C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech/Miscellounous/NIST.png)]


Here is my simulation result. I use it to compare with NIST's result as a proof of my simulation's validity. 

[![Group Index vs Wavelength](C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech/SHG/Group%20Velocity%20Dispersion%20Python%20Code/result/4x12um/group_index_vs_wavelength.png)]




Secondly, here is my simulation of GVD of my platform: 

[![4x4 Compare 4x12](C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech/SHG/Group%20Velocity%20Dispersion%20Python%20Code/result/4x4um/4x4_compare_4x12.png)]

as you can see, it is very hard to achieve group velocity matching in GeO2-SiO2 waveguide. This is my current difficulty and I am trying to figure out some ways to avoid it. 


In addition, I also helped to measure the Q, build up extra stages to measure Q, get the MZM+YDFA option working, and get the Tsunami laser working. 

[![MZM](C:\Users\Eric\Desktop\Caltech\photogalvanic_atCaltech\Miscellounous\MZM.png)]

I help to update the Q measurement in the lab by replacing the old code with my code. Please visit my repo to see exact description as it is too long and impossible to include in this report. 

    https://github.com/WyrdHY/Q_Measurement








# Miscellaneous

To preview this file in markdown in VScode：
    1. Press Ctrl+Shift+K
    2. Press V

I am trying to make this intuitive and helpful. Maybe sometime in the future someone will repick this project and this might help him. 

Ti Sapphire: 750-850nm

scattering loss 

material absorption

dry etching

anomalous group velocity dispersion 

bright soliton 

Kerr effect

wavelength: 1064, 850, whatever

device: waveguide, spiral, ring resonator 

SHG group velocity match

1.018v = 18.9 uw = minimum 
2.288V = 4.18 mw = max

1.1V AC 

minimum pulse during is 16ns by function generator

Purchase list:
label marker
microscope light source haye
monitor
bnc connector
pd
HDMI to BNC  


Good resource teaching you how to do COMSOL and MATLAB:
    https://www.youtube.com/watch?v=dB6_yqQ-GPA


# Common Variables for `ewfd` Module in COMSOL

## Electric Field Components
- `ewfd.Ex`: x-component of the electric field
- `ewfd.Ey`: y-component of the electric field
- `ewfd.Ez`: z-component of the electric field
- `ewfd.normE`: Norm (magnitude) of the electric field

## Magnetic Field Components
- `ewfd.Hx`: x-component of the magnetic field
- `ewfd.Hy`: y-component of the magnetic field
- `ewfd.Hz`: z-component of the magnetic field
- `ewfd.normH`: Norm (magnitude) of the magnetic field

## Electric Displacement Field Components
- `ewfd.Dx`: x-component of the electric displacement field
- `ewfd.Dy`: y-component of the electric displacement field
- `ewfd.Dz`: z-component of the electric displacement field
- `ewfd.normD`: Norm (magnitude) of the electric displacement field

## Magnetic Flux Density Components
- `ewfd.Bx`: x-component of the magnetic flux density
- `ewfd.By`: y-component of the magnetic flux density
- `ewfd.Bz`: z-component of the magnetic flux density
- `ewfd.normB`: Norm (magnitude) of the magnetic flux density

## Energy Density
- `ewfd.We`: Electric energy density
- `ewfd.Wm`: Magnetic energy density

## Power Flow
- `ewfd.Poav`: Time-averaged power flow

## Effective Mode Index
- `ewfd.neff`: Effective mode index (complex)
- `real(ewfd.neff)`: Real part of the effective mode index
- `imag(ewfd.neff)`: Imaginary part of the effective mode index

## Frequency and Wavelength
- `ewfd.freq`: Eigenfrequency of the mode
- `ewfd.lambda`: Wavelength in the medium
