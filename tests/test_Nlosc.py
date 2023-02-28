from ninatool.internal.structures import Nlosc, branch
from ninatool.circuits.base_circuits import snail
import matplotlib.pyplot as plt

spa = Nlosc(nlind = snail(), name = 'SPA')
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