from ninatool.internal.structures import branch
from ninatool.internal.elements import J
from ninatool.gui.mainwindow import ninaGUI

B0 = branch([J(1, name = str(i)) for i in range(21)], name = 'B0')

ninaGUI(B0)  