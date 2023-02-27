from PyQt5 import QtWidgets
import pyqtgraph as pg
from .gui_utils import updated_signal

class elementWidget(QtWidgets.QWidget):
    
    def __init__(self, element):
        
        super().__init__()
        self.element = element
        self.signal = updated_signal()
        self.create_elementBox()
    
    def create_elementBox(self):
        
        elementSpinBox = QtWidgets.QDoubleSpinBox(self)
        elementSpinBox.setMaximumWidth(100)
        elementSpinBox.setMinimum(0.01)
        elementSpinBox.setMaximum(1e3)
        elementSpinBox.setSingleStep(0.01)
        
        if self.element.kind == 'J':    
            parString = '.ic'
            elementSpinBox.setValue(self.element.ic)
        elif self.element.kind == 'L':
            parString = '.L0'
            elementSpinBox.setValue(self.element.L0)
            
        elementLabel = QtWidgets.QLabel(self.element.name + parString)
        
        elementSpinBox.valueChanged.connect(self.update)
        
        Box = QtWidgets.QVBoxLayout()
        Box.addWidget(elementLabel)
        Box.addWidget(elementSpinBox)
        
        self.setLayout(Box)
        
    def update(self, value):
        
        if self.element.kind == 'J':    
            self.element.ic = value
        elif self.element.kind == 'L':
            self.element.L0 = value

        self.signal.updated.emit()
        
class axisWidget(QtWidgets.QWidget):
    
    def __init__(self, label = ''):
        
        super().__init__()
        
        self.Combo = QtWidgets.QComboBox()
        self.Combo.setMaximumWidth(300)
        
        Label = QtWidgets.QLabel()
        Label.setText(label)
        
        Box = QtWidgets.QVBoxLayout()
        
        Box.addWidget(Label)
        Box.addWidget(self.Combo)
        
        self.setLayout(Box)
        
    def addItem(self, item):
        self.Combo.addItem(item)
        
class plotWidget(QtWidgets.QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('k')
        self.graphWidget.showGrid(x = True, y = True)
        
        pen = pg.mkPen(color=(0, 255, 150), width= 2)
        self.plot = self.graphWidget.plot(pen = pen)
        
        self.xaxisWidget = axisWidget(label = 'X axis')
        self.yaxisWidget = axisWidget(label = 'Y axis')
      
        self.axesBox = QtWidgets.QHBoxLayout()
        self.axesBox.addWidget(self.xaxisWidget)
        self.axesBox.addWidget(self.yaxisWidget)  
      
        plotLayout = QtWidgets.QVBoxLayout()
        plotLayout.addLayout(self.axesBox)
        plotLayout.addWidget(self.graphWidget)
        
        self.setLayout(plotLayout)