import numpy as np
## Define diffraction-related parameters:
# x-ray energy in keV
Ex = 15.2
# angular resolution on detector
dchi = 2*np.pi / 120
# q range for fitting (lower )
q = np.linspace(24.5, 53, num=50)
# path to crystal cif file
cifPath = 'analysis/BaCO3.cif'
# crystal size (repeat unit cell along each axis)
crystalsize = (15,15,15)
# angular sampling
sampling = 'cubochoric' # or 'simple' (legacy)