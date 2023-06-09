from ninatool.internal.structures import Nlosc
from ninatool.circuits.base_circuits import snail
from ninatool.gui.mainwindow import ninaGUI

spa = Nlosc(nlind = snail(order = 5), name = 'SPA')
ninaGUI(spa)