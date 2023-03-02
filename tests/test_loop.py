from ninatool.internal.elements import L, J
from ninatool.internal.structures import loop
import numpy as np
from matplotlib import pyplot as plt

### DEFINES ELEMENTS ###
J0 = J(.1, order = 2)
L0 = L(1, order = 2)
L1 = L(1, order = 2)
### DEFINES RFSQUID ###
rfsquid = loop(left_branch = [J0, L0], right_branch = [L1], name = 'rfsquid')
### SETS PHASE OF THE FREE ELEMENT IN THE RFSQUID
#%%
from ninatool.gui.mainwindow import mainwindow
import sys
from PyQt5 import QtWidgets
import numpy as np
#%%
app = QtWidgets.QApplication(sys.argv)
window = mainwindow(rfsquid)
window.resize(600,600)
window.show()
app.exec()
del app