from PyQt5 import QtWidgets
from functools import partial
from .gui_utils import load_loop, load_branch, load_nlosc
from .gui_widgets import plotWidget, freePhiWidget, unitsWidget

class mainwindow(QtWidgets.QMainWindow):
    
    def __init__(self, structure):
        
        super().__init__()
        
        self.unitsWidget = unitsWidget()
        self.structure = structure
        self.elementsBox = QtWidgets.QHBoxLayout()
        self.freePhiWidget = freePhiWidget()
        self.plotWidget = plotWidget()
        self.axesDict = {}
        self.create_all()
        self.connect_axes()
        self.update_axes()

    @property
    def elements(self):
        
        if self.structure.kind == 'branch' or self.structure.kind == 'loop':
            return(self.structure.elements)
        elif self.structure.kind == 'nlosc':
            return(self.structure.nlind.elements)
        
    @property
    def xaxisWidget(self):
        return(self.plotWidget.xaxisWidget)
    
    @property
    def yaxisWidget(self):
        return(self.plotWidget.yaxisWidget)
       
    def connect_axes(self):
        
        self.xaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
        self.yaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
        self.unitsWidget.currentUnitsCombo.currentTextChanged.connect(self.update_axes)
    
    def update_axes(self):
        
        self.xdata = self.axesDict[self.xaxisWidget.Combo.currentText()]()
        self.ydata = self.axesDict[self.yaxisWidget.Combo.currentText()]()
        self.update_plot()
        self.updateFreeIndicators()
    
    def load_structure(self):
        
        if self.structure.kind == 'branch':
            load_branch(self, self.structure)
            
        if self.structure.kind == 'loop':
            load_loop(self, self.structure)
                    
        if self.structure.kind == 'nlosc':
            load_nlosc(self, self.structure)

    def create_CentralWidget(self):
        
        box = QtWidgets.QVBoxLayout()
        box.addLayout(self.elementsBox)
        box.addWidget(self.freePhiWidget)
        box.addWidget(self.plotWidget)
        box.addWidget(self.multivaluedLed)
        box.addWidget(self.unitsWidget)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(box)
        self.setCentralWidget(centralWidget)
        
    def create_multivalued_indicator(self):
        
        self.multivaluedLed = QtWidgets.QCheckBox()
        self.multivaluedLed.setText('multivalued')
        
    def create_all(self):

        self.load_structure()
        self.create_multivalued_indicator()
        self.create_CentralWidget()
        
    def update_plot(self):
        
        self.multivaluedLed.setChecked(not self.structure.multivalued)
        self.plotWidget.graphWidget.setLabel('bottom', 
                                             self.xaxisWidget.Combo.currentText())
        self.plotWidget.graphWidget.setLabel('left', 
                                             self.yaxisWidget.Combo.currentText())
        self.plotWidget.plot.setData(self.xdata, self.ydata)
        
    def updateFreeIndicators(self):
        
        elementWidgets = (self.elementsBox.itemAt(i) 
                          for i in range(self.elementsBox.count()))
        
        for elementWidget in elementWidgets:
            elementWidget.widget().updateFreeIndicator()    
