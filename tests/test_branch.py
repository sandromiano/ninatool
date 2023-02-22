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

plt.plot(J1.phi, J0.phi, label = 'J0.ic=' + str(J1.ic))
J1.ic = 2
plt.plot(J1.phi, J0.phi, label = 'J0.ic=' + str(J1.ic))
plt.legend()