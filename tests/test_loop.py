from ninatool.internal.elements import L, J
from ninatool.internal.structures import loop
from ninatool.gui.mainwindow import ninaGUI
import numpy as np
from matplotlib import pyplot as plt

### DEFINES ELEMENTS ###
J0 = J(.1, order = 2)
L0 = L(1, order = 2)
L1 = L(1, order = 2)
### DEFINES RFSQUID ###
rfsquid = loop(left_branch = [J0, L0], right_branch = [L1], name = 'rfsquid')
ninaGUI(rfsquid)
