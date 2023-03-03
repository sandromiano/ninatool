from ninatool.internal.elements import L, J
from ninatool.internal.structures import loop
from ninatool.gui.mainwindow import ninaGUI

order = 3
### DEFINES ELEMENTS ###
J0 = J(.1, order = order, name = 'J0')
L0 = L(1, order = order, name = 'L0')
L1 = L(1, order = order, name = 'L1')
### DEFINES RFSQUID ###
rfsquid = loop(left_branch = [J0, L0], right_branch = [L1], name = 'rfsquid')
ninaGUI(rfsquid)
