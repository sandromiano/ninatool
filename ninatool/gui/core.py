from PyQt5 import QtWidgets
import pyqtgraph as pg
from functools import partial
from .util import element_adm, element_i, element_phi
from .widgets import elementWidget, axisWidget, plotWidget

class mainwindow(QtWidgets.QMainWindow):
    
    def __init__(self, structure):
        
        super().__init__()
        
        self.structure = structure
        self.elementsBox = QtWidgets.QHBoxLayout()
        self.plotWidget = plotWidget()
        self.axesDict = {}
        self.create_all()
        self.populate_axesBox()
        self.connect_axes()
        self.update_axes()

    @property
    def elements(self):
        return(self.structure.elements)
    
    @property
    def xaxisWidget(self):
        return(self.plotWidget.xaxisWidget)
    
    @property
    def yaxisWidget(self):
        return(self.plotWidget.yaxisWidget)
       
    def connect_axes(self):
        
        self.xaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
        self.yaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
    
    def update_axes(self):
        self.xdata = self.axesDict[self.xaxisWidget.Combo.currentText()]()
        self.ydata = self.axesDict[self.yaxisWidget.Combo.currentText()]()
        self.update_plot()
        
    def create_elementsBox(self):
        
        for element in self.elements:
            if element.kind == 'J':
                widget = elementWidget(element)
            if element.kind == 'L':
                widget = elementWidget(element)
            
            widget.signal.updated.connect(self.update_axes)
            self.elementsBox.addWidget(widget)
        
    def populate_axesBox(self):
        
        if self.structure.kind == 'branch':
            axisName = self.structure.name
            for axisBox in [self.xaxisWidget.Combo, self.yaxisWidget.Combo]:
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
            for axisBox in [self.xaxisWidget.Combo, self.yaxisWidget.Combo]:
                axisBox.addItem(axisName + '.flux')
                
                for i in range(self.structure.order):
                    axisBox.addItem(axisName + '.u' + str(i+2))
            
            self.axesDict[axisName + '.flux'] = lambda : self.structure.flux
            
            for i in range(self.structure.order):
                self.axesDict[axisName + '.u' + str(i + 2)] = partial(element_adm, self.structure, i)
                
        for element in self.structure.elements:
            axisName = element.name
            for axisBox in [self.xaxisWidget.Combo, self.yaxisWidget.Combo]:
                axisBox.addItem(axisName + '.phi')
                axisBox.addItem(axisName + '.i')
                
                for i in range(self.structure.order):
                    axisBox.addItem(axisName + '.u' + str(i + 2))
                
            self.axesDict[axisName + '.phi'] = partial(element_phi, element)
            self.axesDict[axisName + '.i'] = partial(element_i, element)
            for i in range(self.structure.order):
                self.axesDict[axisName + '.u' + str(i + 2)] = partial(element_adm, element, i)
        
    def create_CentralWidget(self):
        
        box = QtWidgets.QVBoxLayout()
        box.addLayout(self.elementsBox)
        box.addWidget(self.plotWidget)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(box)
        self.setCentralWidget(centralWidget)
        
    def create_all(self):

        self.create_elementsBox()
        self.create_CentralWidget()
        
    def update_plot(self):
        
        self.plotWidget.graphWidget.setLabel('bottom', self.xaxisWidget.Combo.currentText())
        self.plotWidget.graphWidget.setLabel('left', self.yaxisWidget.Combo.currentText())
        self.plotWidget.plot.setData(self.xdata, self.ydata)
