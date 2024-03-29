from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QApplication
from PyQt5.QtCore import QRectF
from .gui_utils import load_loop, load_branch, load_nlosc, findComboBoxIndex
from .gui_widgets import plotWidget, freePhiWidget, unitsWidget, multivaluedWidget
import sys

padding = 0.1

class mainwindow(QMainWindow):
    
    def __init__(self, structure):
        
        super().__init__()
        self.setWindowTitle('ninaGUI')
        self.unitsWidget = unitsWidget()
        self.structure = structure
        self.elementsBox = QHBoxLayout()
        self.freePhiWidget = freePhiWidget()
        self.plotWidget = plotWidget()
        self.multivaluedWidget = multivaluedWidget()
        self.axesDict = {}
        self.axesUnitsDict = {}
        self.create_all()
        self.set_defaults()
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
       
    @property
    def zoom_rect(self):
        width = self.plotWidget.graphWidget.sceneRect().width() * (1. + padding)
        height = self.plotWidget.graphWidget.sceneRect().height() * (1. + padding)
        center = self.plotWidget.graphWidget.sceneRect().center()
        zoom_rect = QRectF(center.x() - width / 2., center.y() - height / 2., width, height)
        return(zoom_rect)
        
### FOR RESCALING PLOT ###
    def showEvent(self, e) -> None:
        super().showEvent(e)
        self.plotWidget.graphWidget.fitInView(self.zoom_rect)
        
    def resizeEvent(self, e) -> None:
        super().resizeEvent(e)
        self.plotWidget.graphWidget.fitInView(self.zoom_rect)
### FOR RESCALING PLOT ###
    
    
    def connect_axes(self):
        
        self.xaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
        self.yaxisWidget.Combo.currentIndexChanged.connect(self.update_axes)
        self.unitsWidget.currentUnitsSpinBox.valueChanged.connect(self.update_axes)
        self.unitsWidget.plotUnitsCombo.currentIndexChanged.connect(self.update_axes)
    
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
        
        box = QVBoxLayout()
        box.addLayout(self.elementsBox)
        box.addWidget(self.freePhiWidget)
        box.addWidget(self.plotWidget)
        box.addWidget(self.multivaluedWidget)
        box.addWidget(self.unitsWidget)

        centralWidget = QWidget()
        centralWidget.setLayout(box)
        self.setCentralWidget(centralWidget)
        
    def create_all(self):

        self.load_structure()
        self.create_CentralWidget()

    def set_defaults(self):

        #sets default plots
        if self.structure.kind == 'branch':
            defaultX = self.structure.name + '.phi'
            defaultY = self.structure.name + '.i'
        elif self.structure.kind == 'loop':
            defaultX = self.structure.name + '.flux'
            defaultY = self.structure.name + '.u2'
        elif self.structure.kind == 'nlosc':
            if self.structure.nlind.kind == 'branch':
                defaultX = self.structure.nlind.name + '.phi'
                defaultY = self.structure.name + '.w'
            elif self.structure.nlind.kind == 'loop':
                defaultX = self.structure.nlind.name + '.flux'
                defaultY = self.structure.name + '.w'
                
        Xindex = findComboBoxIndex(self.xaxisWidget.Combo, defaultX)
        Yindex = findComboBoxIndex(self.yaxisWidget.Combo, defaultY)
        self.xaxisWidget.Combo.setCurrentIndex(Xindex)
        self.yaxisWidget.Combo.setCurrentIndex(Yindex)
        
        #sets default free-phase
        self.freePhiWidget.LineEdit.insert('linspace(-1.,1.,201) * 2 * pi')
        self.freePhiWidget.update()

    def update_plot(self):
        
        self.multivaluedWidget.Led.setChecked(self.structure.multivalued)
        
        if self.unitsWidget.plotUnitsCombo.currentText() == 'SI UNITS':
            xunits = self.axesUnitsDict[self.XAxisSelection]
            yunits = self.axesUnitsDict[self.YAxisSelection]
        elif self.unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
            xunits = None
            yunits = None
        
        self.plotWidget.XAxisItem.setLabel(
            text = self.XAxisSelection, 
            units = xunits)

        
        self.plotWidget.YAxisItem.setLabel(
            text = self.YAxisSelection, 
            units = yunits)

        self.plotWidget.plot.setData(self.xdata, self.ydata)
        
    def updateFreeIndicators(self):
        
        elementWidgets = (self.elementsBox.itemAt(i) 
                          for i in range(self.elementsBox.count()))
        
        for elementWidget in elementWidgets:
            elementWidget.widget().updateFreeIndicator()    

def ninaGUI(circuit):
    app = QApplication(sys.argv)
    window = mainwindow(circuit)
    window.show()
    app.exec()
    del app