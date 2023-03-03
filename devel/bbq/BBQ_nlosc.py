from ninatool.circuits.base_circuits import snail
from ninatool.internal.structures import Nlosc
import numpy as np
from matplotlib import pyplot as plt
from ninatool.gui.mainwindow import ninaGUI
#%%
snail0 = snail()
l = snail0.imp[0]
flux = snail0.flux

c = 1
w = np.linspace(.01,11,1001)

L, W = np.meshgrid(l, w, indexing = 'ij')

YC = 1/(1j * W * c)
YL = 1j * W * L

Y = YC + YL

plt.figure()
plt.pcolormesh(flux, w, Y.imag.transpose())
wr_indx = np.argmin(np.abs(Y.imag), axis = -1)
plt.colorbar()
plt.figure()
plt.plot(flux, w[wr_indx]*2*np.pi)
#%%
SPA = Nlosc(snail0)
ninaGUI(SPA)


