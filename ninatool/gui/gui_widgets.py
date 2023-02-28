from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np
pi = np.pi

class updated_signal(QObject):
    
    updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        pass

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
        if self.element.kind =='C':
            parString = '.C'
            elementSpinBox.setValue(self.element.C)
            
        elementLabel = QtWidgets.QLabel(self.element.name + parString)
        
        elementSpinBox.valueChanged.connect(self.update)
        
        Box = QtWidgets.QVBoxLayout()
        Box.addWidget(elementLabel)
        Box.addWidget(elementSpinBox)
        
        if self.element.kind =='J':
            self.isFreeLabel = QtWidgets.QLabel('free')
            Box.addWidget(self.isFreeLabel)
        else: #this is a nasty trick to align non JJ boxes... Fix it!!!
            self.isFreeLabel = QtWidgets.QLabel('')
            self.isFreeLabel.setStyleSheet('font-size: 14px')
            Box.addWidget(self.isFreeLabel)
        
        self.setLayout(Box)
        
    def update(self, value):
        
        if self.element.kind == 'J':    
            self.element.ic = value
        elif self.element.kind == 'L':
            self.element.L0 = value
        elif self.element.kind =='C':
            self.element.C = value
            
        self.signal.updated.emit()
            
    def updateFreeIndicator(self):
        if self.element.kind =='J':
            if self.element.is_free:
                self.isFreeLabel.setStyleSheet('color : green; \
                                               font-weight: bold; \
                                               font-size: 14px')
            else:
                self.isFreeLabel.setStyleSheet('color : lightgray; \
                                               font-weight: bold; \
                                               font-size: 14px')


        
class freePhiWidget(QtWidgets.QWidget):

    def __init__(self):
        
        super().__init__()
        
        self.freePhase = None
        self.LineEdit = QtWidgets.QLineEdit()
        Label = QtWidgets.QLabel('free_element.phi')
        self.signal = updated_signal()
        self.LineEdit.editingFinished.connect(self.update)

        Box = QtWidgets.QVBoxLayout()
        Box.addWidget(Label)
        Box.addWidget(self.LineEdit)
        self.setLayout(Box)
        
    def update(self):
        self.freePhase = eval(self.LineEdit.text())
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