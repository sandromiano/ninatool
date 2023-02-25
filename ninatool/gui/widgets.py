from PyQt5 import QtWidgets
from .util import updated_signal

class JWidget(QtWidgets.QWidget):
    
    def __init__(self, J_object):
        
        super().__init__()
        
        self.J = J_object
        self.signal = updated_signal()
        self.create_jBox()
    
    def create_jBox(self):
        
        jSpinBox = QtWidgets.QDoubleSpinBox(self)
        jSpinBox.setMinimum(0.01)
        jSpinBox.setMaximum(1e3)
        jSpinBox.setSingleStep(0.01)
        jSpinBox.setValue(self.J.ic)
        jSpinBox.valueChanged.connect(self.update_ic)
        
        jLabel = QtWidgets.QLabel(self.J.name + '.ic', self)
        
        jBox = QtWidgets.QVBoxLayout()
        jBox.addWidget(jLabel)
        jBox.addWidget(jSpinBox)
        
        self.setLayout(jBox)
        
    def update_ic(self, value):
        self.J.ic = value
        self.signal.updated.emit()
        
class LWidget(QtWidgets.QWidget):
    
    def __init__(self, L_object):
        
        super().__init__()
        
        self.L = L_object
        self.signal = updated_signal()
        self.create_lBox()
    
    def create_lBox(self):
        
        lSpinBox = QtWidgets.QDoubleSpinBox(self)
        lSpinBox.setMinimum(0.01)
        lSpinBox.setMaximum(1e3)
        lSpinBox.setSingleStep(0.01)
        lSpinBox.setValue(self.L.L0)
        lSpinBox.valueChanged.connect(self.update_L0)
        
        lLabel = QtWidgets.QLabel(self.L.name + '.L0', self)
        
        lBox = QtWidgets.QVBoxLayout()
        lBox.addWidget(lLabel)
        lBox.addWidget(lSpinBox)
        
        self.setLayout(lBox)
        
    def update_L0(self, value):
        self.L.L0 = value
        self.signal.updated.emit()
        
class axisWidget(QtWidgets.QWidget):
    
    def __init__(self, label = ''):
        
        super().__init__()
        
        self.Combo = QtWidgets.QComboBox()
        
        Label = QtWidgets.QLabel()
        Label.setText(label)
        
        Box = QtWidgets.QVBoxLayout()
        
        Box.addWidget(Label)
        Box.addWidget(self.Combo)
        
        self.setLayout(Box)
        
    def addItem(self, item):
        self.Combo.addItem(item)