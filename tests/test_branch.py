from ninatool.internal.elements import L, J
from ninatool.internal.structures import branch
import numpy as np
from matplotlib import pyplot as plt

### DEFINES ELEMENTS ###
J0 = J(1, order = 2, name = 'J0')
J1 = J(.1, order = 2, name = 'J1')
L0 = L(1, order = 2, name = 'L0')
L1 = L(1, order = 2, name = 'L1')
### DEFINES BRANCH B0 ###
B0 = branch(elements = [J0, J1, L0, L1], name = 'B0')
### SETS PHASE OF FREE ELEMENT IN B0
B0.free_phi = np.linspace(-1,1,101) * 2 * np.pi

#plt.scatter(B0.free_element.phi, B0.phi, s = 5, color = 'k')

for phi in B0.free_element.phi:
    plt.axvline(phi, color = 'k')

B0.interpolate_results(np.linspace(-1,1,101) * 2 * np.pi)

for phi in B0.phi:
    plt.axvline(phi, color = 'g')

plt.scatter(B0.phi, B0.adm[0], s = 5, color = 'g')