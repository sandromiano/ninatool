from ninatool.internal.elements import L, J, NW
from ninatool.internal.structures import branch
from ninatool.gui.mainwindow import ninaGUI
import matplotlib.pyplot as plt


order = 2

### DEFINES ELEMENTS ###
NW0 = NW(delta = 0.8, tau = 0.9, order = order, name = 'NW0')
L0 = L(10, order = order, name = 'L0')
### DEFINES BRANCH B0 ###
B0 = branch(
    elements = [NW0, L0], 
    name = 'branch')

plt.plot(B0.phi, B0.i, label = 'multistable = ' + str(B0.multivalued))
NW0.delta = 0.1
plt.plot(B0.phi, B0.i, label = 'multistable = ' + str(B0.multivalued))
plt.legend()
