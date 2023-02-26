from PyQt5.QtCore import pyqtSignal, QObject


def loop_left_adm(loop, index):
    return(loop.left_adm[index])

def loop_right_adm(loop, index):
    return(loop.right_adm[index])

def element_adm(element, index):
    return (element.adm[index])

def element_phi(element):
    return (element.phi)

def element_i(element):
    return (element.i)

class updated_signal(QObject):
    
    updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        pass