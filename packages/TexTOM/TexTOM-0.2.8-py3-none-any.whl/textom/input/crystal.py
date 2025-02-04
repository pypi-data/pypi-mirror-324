import numpy as np
## Define diffraction-related parameters:
# x-ray energy in keV
Ex = 15.2
# q range for fitting
q = np.linspace(24.5, 53, num=50)
# azimutal range for fitting
chi = np.linspace( 0, 2*np.pi, int(2*np.pi/60), endpoint=False) + dchi/2
# path to crystal cif file
cifPath = 'analysis/BaCO3.cif'
# crystal size (repeat unit cell along each axis)
crystalsize = (15,15,15)
# angular sampling
sampling = 'cubochoric' # or 'simple' (legacy)
# angular sampling resolution
dchi = 2*np.pi / 120