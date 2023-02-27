from PyQt5 import QtWidgets
from functools import partial
from .gui_utils import element_adm, element_i, element_phi, loop_left_adm, \
                       loop_right_adm, load_loop, load_branch, load_nlosc
from .gui_widgets import elementWidget, axisWidget, plotWidget

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
        
        if self.structure.kind == 'branch' or self.structure.kind == 'loop':
            return(self.structure.elements)
        elif self.structure.kind == 'Nlosc':
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
            load_branch(self, self.structure)
            
        if self.structure.kind == 'loop':
            load_loop(self, self.structure)
                    
        if self.structure.kind == 'Nlosc':
            load_nlosc(self, self.structure)

    def create_CentralWidget(self):
        
        box = QtWidgets.QVBoxLayout()
        box.addLayout(self.elementsBox)
        box.addWidget(self.plotWidget)
        box.addWidget(self.led)
        
        centralWidget = QtWidgets.QWidget()
        centralWidget.setLayout(box)
        self.setCentralWidget(centralWidget)
        
    def create_multistable_indicator(self):
        
        self.led = QtWidgets.QCheckBox()
        self.led.setText('multivalued')
        
    def create_all(self):

        self.create_elementsBox()
        self.create_multistable_indicator()
        self.create_CentralWidget()
        
    def update_plot(self):
        
        self.led.setChecked(not self.structure.multivalued)
        self.plotWidget.graphWidget.setLabel('bottom', 
                                             self.xaxisWidget.Combo.currentText())
        self.plotWidget.graphWidget.setLabel('left', 
                                             self.yaxisWidget.Combo.currentText())
        self.plotWidget.plot.setData(self.xdata, self.ydata)
