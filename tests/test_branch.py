from ninatool.internal.elements import L, J
from ninatool.internal.structures import branch
import numpy as np
from matplotlib import pyplot as plt

order = 2

### DEFINES ELEMENTS ###
J0 = J(1, order = order, name = 'J0')
J1 = J(.1, order = order, name = 'J1')
L0 = L(1, order = order, name = 'L0')
L1 = L(1, order = order, name = 'L1')
### DEFINES BRANCH B0 ###
B0 = branch(elements = [J0, J1, L0, L1], name = 'B0')
### SETS PHASE OF FREE ELEMENT IN B0
#%%
from ninatool.gui.mainwindow import mainwindow
import sys
from PyQt5 import QtWidgets
import numpy as np
#%%
app = QtWidgets.QApplication(sys.argv)
window = mainwindow(B0)
window.resize(600,600)
window.show()
app.exec()
del app