from PyQt5 import QtWidgets
import pyqtgraph as pg
from functools import partial
from .util import element_adm, element_i, element_phi
from .widgets import JWidget, LWidget, axisWidget


        
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
        
        self.xaxisWidget = axisWidget(label = 'X axis')
        self.yaxisWidget = axisWidget(label = 'Y axis')
        
        self.axesBox = QtWidgets.QHBoxLayout()
        self.axesBox.addWidget(self.xaxisWidget)
        self.axesBox.addWidget(self.yaxisWidget)
        self.populate_axesBox()
        
        self.xaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
        self.yaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
    
    def update_axes(self):
        self.xdata = self.axesDict[self.xaxisWidget.Combo.currentText()]()
        self.ydata = self.axesDict[self.yaxisWidget.Combo.currentText()]()
        self.update_plot()
        
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
                widget = JWidget(element)
            if element.kind == 'L':
                widget = LWidget(element)
            
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
        
        self.graphWidget.setLabel('bottom', self.xaxisWidget.Combo.currentText())
        self.graphWidget.setLabel('left', self.yaxisWidget.Combo.currentText())
        self.plot.setData(self.xdata, self.ydata)
