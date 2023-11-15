from ninatool.internal.elements import L, J, NW
from ninatool.internal.structures import loop
from ninatool.gui.mainwindow import ninaGUI
import matplotlib.pyplot as plt

order = 3
### DEFINES ELEMENTS ###
NW0 = NW(0.5, 0.5, order = order, name = 'NW0')
J1 = J(.5, order = order, name = 'J1')
J2 = J(.5, order = order, name = 'J2')
J3 = J(.5, order = order, name = 'J3')

### DEFINES RFSQUID ###
NWSNAIL = loop(
    left_branch = [NW0], 
    right_branch = [J1, J2, J3], 
    name = 'dcsquid', 
    observe_elements=True, 
    stray_inductance = True)#%%

plt.plot(NWSNAIL.flux, NWSNAIL.adm[0], label = 'multivalued = ' + str(NWSNAIL.multivalued))
NW0.delta = 0.9
NW0.tau = 0.75
plt.plot(NWSNAIL.flux, NWSNAIL.adm[0], label = 'multivalued = ' + str(NWSNAIL.multivalued))
plt.legend()
plt.xlabel(r'$\varphi_e$')
plt.ylabel(r'$u_2$')
