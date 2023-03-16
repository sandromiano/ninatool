from ninatool.internal.elements import L, J
from ninatool.internal.structures import loop
from ninatool.gui.mainwindow import ninaGUI

order = 3
### DEFINES ELEMENTS ###
J0 = J(1, order = order, name = 'J0')
J1 = J(.1, order = order, name = 'J1')
J2 = J(2, order = order, name = 'J2')
J3 = J(.1, order = order, name = 'J3')

### DEFINES RFSQUID ###
dcsquid = loop(
    left_branch = [J(1, order = order, name = str(i)) for i in range(10)], 
    right_branch = [J1, J2, J3], 
    name = 'dcsquid', 
    observe_elements=True, 
    stray_inductance = True)

ninaGUI(dcsquid)