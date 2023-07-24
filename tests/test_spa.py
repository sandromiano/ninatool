from ninatool.internal.structures import Nlosc
from ninatool.circuits.base_circuits import snail
from ninatool.gui.mainwindow import ninaGUI
from ninatool.internal.tools import unitsConverter
import matplotlib.pyplot as plt
import numpy as np

cmap = plt.get_cmap('tab10')

plt.style.use('paper_1col')

spa = Nlosc(nlind = snail(a = .06, stray_inductance=True), name = 'SPA')

unitsHandler = unitsConverter()
unitsHandler.current_units = 6e-9

f = spa.omega * unitsHandler.frequency_units
g3 = spa.gn[0] * unitsHandler.frequency_units
g4 = spa.gn[1] * unitsHandler.frequency_units
flux = spa.nlind.flux

fig, ax = plt.subplots(1,3, figsize = (5.5,2), sharex = True)

ax[0].plot(flux/2/np.pi,f/1e9, color = cmap(0))
ax[1].plot(flux/2/np.pi,g3/1e6, color = cmap(1))
ax[2].plot(flux/2/np.pi,g4/1e6, color = cmap(2))

ax[0].set_xlabel(r'$\bar{\varphi}_\mathrm{e}/2\pi$', fontsize = 14)
ax[1].set_xlabel(r'$\bar{\varphi}_\mathrm{e}/2\pi$', fontsize = 14)
ax[2].set_xlabel(r'$\bar{\varphi}_\mathrm{e}/2\pi$', fontsize = 14)

ax[0].set_ylabel(r'$\omega/2\pi$ (GHz)', labelpad = 2, fontsize = 14)
ax[1].set_ylabel(r'$g_3/2\pi$ (MHz)', labelpad = 2, fontsize = 14)
ax[2].set_ylabel(r'$g_4/2\pi$ (MHz)', labelpad = 2, fontsize = 14)

ax[0].set_xlim(-1,1)
ax[0].set_ylim(4.2,5.4)
ax[1].set_ylim(-120,120)
ax[2].set_ylim(-60,30)

ax[0].set_yticks([4.2,4.8,5.4])
ax[1].set_yticks([-120,-60,0,60,120])
ax[2].set_yticks([-60,-30,0,30])

plt.tight_layout()


