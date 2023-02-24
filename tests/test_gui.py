from ninatool.gui.core import mainwindow
from ninatool.circuits.base_circuits import rfsquid, snail
import sys
from PyQt5 import QtWidgets
loop0 = snail(order = 6)
#%%
app = QtWidgets.QApplication(sys.argv)
window = mainwindow(loop0)
window.show()
app.exec()
del app