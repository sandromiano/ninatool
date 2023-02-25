from ninatool.gui.core import mainwindow
from ninatool.circuits.base_circuits import rfsquid, snail
import sys
from PyQt5 import QtWidgets
import numpy as np

loop0 = snail(order = 5)
loop0.free_phi = np.linspace(-1,1,1001) * 2 * np.pi
#%%
app = QtWidgets.QApplication(sys.argv)
window = mainwindow(loop0)
window.show()
app.exec()
del app