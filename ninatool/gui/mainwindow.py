from PyQt5 import QtWidgets
from .gui_utils import load_loop, load_branch, load_nlosc
from .gui_widgets import plotWidget, freePhiWidget, unitsWidget, multivaluedWidget

class mainwindow(QtWidgets.QMainWindow):
    
    def __init__(self, structure):
        
        super().__init__()
        
        self.unitsWidget = unitsWidget()
        self.structure = structure
        self.elementsBox = QtWidgets.QHBoxLayout()
        self.freePhiWidget = freePhiWidget()
        self.plotWidget = plotWidget()
        self.multivaluedWidget = multivaluedWidget()
        self.axesDict = {}
        self.axesUnitsDict = {}
        self.create_all()
        self.connect_axes()
        self.update_axes()

    @property
    def XAxisSelection(self):
        return(self.xaxisWidget.Combo.currentText())
    
    @property
    def YAxisSelection(self):
        return(self.yaxisWidget.Combo.currentText())
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
        self.unitsWidget.currentUnitsSpinBox.valueChanged.connect(self.update_axes)
    
    def update_axes(self):
        
        self.xdata = self.axesDict[self.XAxisSelection]()
        self.ydata = self.axesDict[self.YAxisSelection]()
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
        box.addWidget(self.multivaluedWidget)
        box.addWidget(self.unitsWidget)

        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(box)
        self.setCentralWidget(centralWidget)
        
    def create_all(self):

        self.load_structure()
        self.create_CentralWidget()
        
    def update_plot(self):
        
        self.multivaluedWidget.Led.setChecked(not self.structure.multivalued)
        
        self.plotWidget.XAxisItem.setLabel(
            text = self.XAxisSelection, 
            units = self.axesUnitsDict[self.XAxisSelection])
        
        self.plotWidget.YAxisItem.setLabel(
            text = self.YAxisSelection, 
            units = self.axesUnitsDict[self.YAxisSelection])

        self.plotWidget.plot.setData(self.xdata, self.ydata)
        
    def updateFreeIndicators(self):
        
        elementWidgets = (self.elementsBox.itemAt(i) 
                          for i in range(self.elementsBox.count()))
        
        for elementWidget in elementWidgets:
            elementWidget.widget().updateFreeIndicator()    
