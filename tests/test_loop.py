from ninatool.internal.elements import L, J
from ninatool.internal.structures import loop
import numpy as np
from matplotlib import pyplot as plt

### DEFINES ELEMENTS ###
J0 = J(.1, order = 2)
L0 = L(1, order = 2)
L1 = L(1, order = 2)
### DEFINES RFSQUID ###
rfsquid = loop(left_branch = [J0, L0], right_branch = [L1], name = 'rfsquid')
### SETS PHASE OF THE FREE ELEMENT IN THE RFSQUID
rfsquid.free_phi = np.linspace(-1,1,101) * 2 * np.pi

plt.plot(rfsquid.flux, rfsquid.adm[0])

rfsquid.interpolate_results(np.linspace(-1,1,101) * 2 * np.pi)

plt.scatter(rfsquid.flux, rfsquid.adm[0])
for flux in rfsquid.flux:
    plt.axvline(flux)
