from ninatool.circuits.base_circuits import snail
from ninatool.internal.structures import Nlosc
from ninatool.internal.tools import unitsConverter
import numpy as np
from matplotlib import pyplot as plt

### SETS UNITS ###
units = unitsConverter()
units.current_units = 1e-9

### DEFINES A SNAIL AND AN SPA ###
snail0 = snail()
SPA = Nlosc(snail0)
SPA.C = 10
### GENERATES DUMMY NUMERICAL CAPACITIVE ADMITTANCE SAME AS THE SPA ###
c0 = SPA.C
def dummy_admittance():
    c = units.capacitance_units * c0
    w = 2 * np.pi * np.linspace(1.5e8, 1e9, 1001)
    adm = 1/(1j * w * c)
    return(w, adm)

### SNAIL INDUCTANCE AS A FUNCTION OF FLUX IN SI UNITS ###
l = units.inductance_units * snail0.imp[0]
flux = snail0.flux
### IMPORTS THE DUMMY ADMITTANCE ###
w, yenv = dummy_admittance()
### DEFINES MESHGRIDS BEFORE COMPUTING THE TOTAL ADMITTANCE ###
L, W = np.meshgrid(l, w, indexing = 'ij')
### MESHGRID ADMITTANCES ###
YL = 1j * W * L
YENV = np.tile(yenv, (len(l), 1))
Y = YL + YENV
### FINDS THE INDEXES OF ZEROS OF TOTAL ADMITTANCE FOR EVERY VALUE OF FLUX
wr_indx = np.argmin(np.abs(Y.imag), axis = -1)
### FREQUENCY FOUND ###
fr = w[wr_indx]/(2 * np.pi)
### PLOTS ###

plt.figure()
plt.plot(
    SPA.nlind.flux, 
    SPA.omega * units.frequency_units, 
    label = 'FROM LUMPED ELEMENT', 
    color = 'k')

plt.scatter(
    flux, 
    fr, 
    s = .5, 
    label = 'FROM BBQ', 
    zorder = 120)
plt.legend()

# NEXT STEPS:
#     NONLINEAR EXPANSION COEFFICIENTS
#     MULTIMODE (STILL SINGLE PORT)
#     MULTIMODE COUPLINGS
