from ninatool.gui.mainwindow import mainwindow
from ninatool.circuits.base_circuits import rfsquid, snail
import sys
from PyQt5 import QtWidgets
import numpy as np

loop0 = rfsquid(order = 5)
loop0.free_phi = np.linspace(-1,1,1001) * 2 * np.pi
#%%
app = QtWidgets.QApplication(sys.argv)
window = mainwindow(loop0)
window.resize(600,600)
window.show()
app.exec()
del app