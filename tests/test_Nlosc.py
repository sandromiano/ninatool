from ninatool.internal.structures import Nlosc
from ninatool.circuits.base_circuits import snail
import matplotlib.pyplot as plt

spa = Nlosc(nlind = snail(order = 4), name = 'SPA')

plt.plot(spa.nlind.flux, spa.omega)
spa.EC = 2
plt.plot(spa.nlind.flux, spa.omega)

#%%
from ninatool.gui.mainwindow import mainwindow
import sys
from PyQt5 import QtWidgets
import numpy as np
#%%
app = QtWidgets.QApplication(sys.argv)
window = mainwindow(spa)
window.resize(600,600)
window.show()
app.exec()
del app