# NINA IMPORTS
from ninatool.internal.structures import loop, Nlosc
from ninatool.internal.elements import L, J

# EXTERNAL IMPORTS
import matplotlib.pyplot as plt
import numpy as np
plt.style.use('paper_1col')
#%%
#NONLINEAR ORDER OF EXPANSION; 1 is LINEAR
order = 5
#LEFT BRANCH ELEMENTS
L0 = L(L = .1, order = order, name = 'L0')
J0 = J(ic = .1, order = order, name = 'J0')
left_elements = [L0, J0]

#RIGHT BRANCH ELEMENTS
L1 = L(L = .1, order = order, name = 'L1')
J1 = J(ic = 1, order = order, name = 'J1')
J2 = J(ic = 1, order = order, name = 'J2')
J3 = J(ic = 1, order = order, name = 'J3')
right_elements = [L1, J1, J2, J3]

#DEFINES THE SNAIL AS A LOOP INSTANCE
snail = loop(left_branch = left_elements, 
             right_branch = right_elements, 
             stray_inductance = True,
             name = 'SNAIL')
#%%
#DEFINES PLOT FUNCTION
def plot_un(order):
    #THE "0" INDEX CORRESPONDS TO SECOND ORDER EXPANSION OF POTENTIAL ENERGY
    plt.plot(snail.flux/2/np.pi, snail.adm[order - 2])
    plt.xlabel(r'$\bar{\varphi}_\mathrm{e}/2\pi$')
    plt.ylabel(r'$u_' + str(order) + '$', rotation = 0, labelpad = 10)
#%%
plot_un(order = 2)
#%%
J1.ic = .5
L0.L0 = 2
plot_un(2)
#%%
#DEFINES A SNAIL PARAMETRIC AMPLIFIER BY SHUNTING THE SNAIL WITH A CAPACITOR
spa = Nlosc(snail, name = 'SPA')
#%%
plt.plot(spa.nlind.flux/2/np.pi, spa.omega)
plt.xlabel(r'$\bar{\varphi}_\mathrm{e}/2\pi$')
plt.ylabel(r'$\omega$', rotation = 0, labelpad = 10)
#%%
# IMPORTS THE NINA GUI
from ninatool.gui.mainwindow import ninaGUI
#%%
#RUNS THE SPA SIMULATION IN THE NINA GUI
ninaGUI(spa)
