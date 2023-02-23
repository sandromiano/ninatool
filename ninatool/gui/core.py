from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
import pyqtgraph as pg
from functools import partial

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

class J_widget(QtWidgets.QWidget):
    
    def __init__(self, J_object):
        
        super().__init__()
        
        self.J = J_object
        self.signal = updated_signal()
        self.create_JJbox()
    
    def create_JJbox(self):
        
        sbox = QtWidgets.QDoubleSpinBox(self)
        sbox.setMinimum(0.01)
        sbox.setMaximum(1e3)
        sbox.setSingleStep(0.01)
        sbox.setValue(self.J.ic)
        sbox.valueChanged.connect(self.update_ic)
        
        label = QtWidgets.QLabel(self.J.name + '.ic', self)
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(sbox)
        
        self.setLayout(vbox)
        
    def update_ic(self, value):
        self.J.ic = value
        self.signal.updated.emit()
        
        
class L_widget(QtWidgets.QWidget):
    
    def __init__(self, L_object):
        
        super().__init__()
        
        self.L = L_object
        self.signal = updated_signal()
        self.create_Lbox()
    
    def create_Lbox(self):
        
        sbox = QtWidgets.QDoubleSpinBox(self)
        sbox.setMinimum(0.01)
        sbox.setMaximum(1e3)
        sbox.setSingleStep(0.01)
        sbox.setValue(self.L.L0)
        sbox.valueChanged.connect(self.update_L0)
        
        label = QtWidgets.QLabel(self.L.name + '.L0', self)
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(sbox)
        
        self.setLayout(vbox)
        
    def update_L0(self, value):
        self.L.L0 = value
        self.signal.updated.emit()
        
class mainwindow(QtWidgets.QMainWindow):
    
    def __init__(self, structure):
        
        super().__init__()
        
        self.structure = structure
        self.elements_box = QtWidgets.QHBoxLayout()
        self.axesDict = {}
        self.create_all()
        self.update_axes()

    @property
    def elements(self):
        return(self.structure.elements)
    
    def create_axesBox(self):
        
        self.xaxisBox = QtWidgets.QComboBox()
        self.yaxisBox = QtWidgets.QComboBox()
        
        self.axesBox = QtWidgets.QHBoxLayout()
        
        self.axesBox.addWidget(self.xaxisBox)
        self.axesBox.addWidget(self.yaxisBox)
        
        self.populate_axesBox()
    
        self.xaxisBox.currentIndexChanged.connect(self.update_axes)
        self.yaxisBox.currentIndexChanged.connect(self.update_axes)
    
    def update_axes(self):
        self.xdata = self.axesDict[self.xaxisBox.currentText()]()
        self.ydata = self.axesDict[self.yaxisBox.currentText()]()
        self.update_plot()
        
    def populate_axesBox(self):
        
        if self.structure.kind == 'branch':
            axisName = self.structure.name
            for axisBox in [self.xaxisBox, self.yaxisBox]:
                axisBox.addItem(axisName + '.phi')
                axisBox.addItem(axisName + '.i')
                
                for i in range(self.structure.order):
                    axisBox.addItem(axisName + '.u' + str(i + 2))
                
            self.axesDict[axisName + '.phi'] = partial(element_phi, self.structure)
            self.axesDict[axisName + '.i'] = partial(element_i, self.structure)
            
            for i in range(self.structure.order):
                self.axesDict[axisName + '.u' + str(i + 2)] = partial(element_adm, self.structure, i)
            
            
        if self.structure.kind == 'loop':
            axisName = self.structure.name
            for axisBox in [self.xaxisBox, self.yaxisBox]:
                axisBox.addItem(axisName + '.flux')
                
                for i in range(self.structure.order):
                    axisBox.addItem(axisName + '.u' + str(i+2))
            
            self.axesDict[axisName + '.flux'] = lambda : self.structure.flux
            
            for i in range(self.structure.order):
                self.axesDict[axisName + '.u' + str(i + 2)] = partial(element_adm, self.structure, i)
                
        for element in self.structure.elements:
            axisName = element.name
            for axisBox in [self.xaxisBox, self.yaxisBox]:
                axisBox.addItem(axisName + '.phi')
                axisBox.addItem(axisName + '.i')
                
                for i in range(self.structure.order):
                    axisBox.addItem(axisName + '.u' + str(i + 2))
                
            self.axesDict[axisName + '.phi'] = partial(element_phi, element)
            self.axesDict[axisName + '.i'] = partial(element_i, element)
            for i in range(self.structure.order):
                self.axesDict[axisName + '.u' + str(i + 2)] = partial(element_adm, element, i)
            
    def create_plot(self):
        
        self.graphWidget = pg.PlotWidget()
        pen = pg.mkPen(color=(0, 255, 150), width= 2)
        self.graphWidget.setBackground('k')
        self.graphWidget.showGrid(x = True, y = True)
        self.plot = self.graphWidget.plot(pen = pen)

    
    def create_plotLayout(self):
        
        self.plotlayout = QtWidgets.QVBoxLayout()
        self.plotlayout.addLayout(self.axesBox)
        self.plotlayout.addWidget(self.graphWidget)
    
    def create_elements_box(self):
        
        for element in self.elements:
            if element.kind == 'J':
                widget = J_widget(element)
            if element.kind == 'L':
                widget = L_widget(element)
            
            widget.signal.updated.connect(self.update_axes)
            self.elements_box.addWidget(widget)
        
    def create_CentralWidget(self):
        
        box = QtWidgets.QVBoxLayout()
        box.addLayout(self.elements_box)
        box.addLayout(self.plotlayout)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(box)
        self.setCentralWidget(centralWidget)
        
    def create_all(self):
        
        self.create_axesBox()
        self.create_plot()
        self.create_plotLayout()
        self.create_elements_box()
        self.create_CentralWidget()
        
    def update_plot(self):
        
        self.graphWidget.setLabel('bottom', self.xaxisBox.currentText())
        self.graphWidget.setLabel('left', self.yaxisBox.currentText())
        self.plot.setData(self.xdata, self.ydata)
