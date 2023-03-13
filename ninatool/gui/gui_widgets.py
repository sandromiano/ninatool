from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDoubleSpinBox, QLabel, QLineEdit, QWidget, QHBoxLayout, QVBoxLayout, QComboBox, QSpinBox
import pyqtgraph as pg
###
#THIS IMPORT IS USED TO ALLOW eval() ON 
#THE FREE_PHI WIDGET TO READ NP, LINSPACE, ARRAY
from numpy import inf, array, linspace, pi
###
from ninatool.internal.tools import unitsConverter
from .scientific_spinbox import ScienDSpinBox as ScientificDoubleSpinBox
from .led_indicator import LedIndicator

#Format string for SI units
format_string = '{:.3g}'

ENABLE_SECTORS = False

class updated_signal(QObject):
    
    updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        pass

class elementWidget(QWidget):
    
    def __init__(self, element):
        
        super().__init__()
        self.element = element
        self.signal = updated_signal()
        self.create_elementBox()
    
    def create_elementBox(self):
        
        elementSpinBox = QDoubleSpinBox(self)
        elementSpinBox.setMaximumWidth(100)
        elementSpinBox.setMinimum(0.01)
        elementSpinBox.setMaximum(inf)
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
            
        elementLabel = QLabel(self.element.name + parString)
        
        elementSpinBox.valueChanged.connect(self.updateValue)
        
        Box = QVBoxLayout()
        Box.addWidget(elementLabel)
        Box.addWidget(elementSpinBox)

        
        if self.element.kind =='J':
            self.isFreeLabel = QLabel('free')
            self.isFreeLabel.setStyleSheet('font-size: 12px')
            
            self.sectorSpinBox = QSpinBox()
            self.sectorSpinBox.setMaximumWidth(100)
            self.sectorSpinBox.setMinimum(-1)
            self.sectorSpinBox.setMaximum(1)
            self.sectorSpinBox.setValue(0)
            
            self.sectorSpinBox.valueChanged.connect(self.updateSector)
            
            Box.addWidget(self.isFreeLabel)
            Box.addWidget(self.sectorSpinBox)
        else: #this is a nasty trick to align non JJ boxes... Fix it!!!
            self.isFreeLabel = QLabel('')
            self.isFreeLabel.setStyleSheet('font-size: 12px')

            self.sectorSpinBox = QSpinBox()
        
            Box.addWidget(self.isFreeLabel)
            Box.addWidget(self.sectorSpinBox)
            
            self.sectorSpinBox.hide()
            
        
        self.setLayout(Box)
        
    def updateValue(self, value):
        
        if self.element.kind == 'J':    
            self.element.ic = value
        elif self.element.kind == 'L':
            self.element.L0 = value
        elif self.element.kind =='C':
            self.element.C = value
            
        self.signal.updated.emit()
        
    def updateSector(self, value):
        if ENABLE_SECTORS:
            self.element.sector = value
                
            self.signal.updated.emit()
        else:
            pass

            
    def updateFreeIndicator(self):
        if self.element.kind =='J':
            if self.element.is_free:
                self.isFreeLabel.setStyleSheet('color : green; \
                                               font-weight: bold; \
                                               font-size: 12px')
                self.sectorSpinBox.hide()
            else:
                self.isFreeLabel.setStyleSheet('color : lightgray; \
                                               font-weight: bold; \
                                               font-size: 12px')
                                               
                if ENABLE_SECTORS:
                    self.sectorSpinBox.show()
                else:
                    self.sectorSpinBox.hide()

class freePhiWidget(QWidget):

    def __init__(self):
        
        super().__init__()
        
        self.freePhase = None
        self.LineEdit = QLineEdit()
        self.LineEdit.setMaximumWidth(300)
        Label = QLabel('free_element.phi')
        self.signal = updated_signal()
        self.LineEdit.editingFinished.connect(self.update)

        Box = QVBoxLayout()
        Box.addWidget(Label)
        Box.addWidget(self.LineEdit)
        self.setLayout(Box)
        
    def update(self):
        self.freePhase = eval(self.LineEdit.text())
        self.signal.updated.emit()
        
class multivaluedWidget(QWidget):

    def __init__(self):
        
        super().__init__()

        self.Led = LedIndicator()
        label = QLabel('multivalued')

        box = QHBoxLayout()
        box.addWidget(self.Led)
        box.addWidget(label)
        box.addStretch()
        box.setSpacing(10)
        
        self.setLayout(box)
        
class axisWidget(QWidget):
    
    def __init__(self, label = ''):
        
        super().__init__()
        
        self.Combo = QComboBox()
        self.Combo.setMaximumWidth(300)
        
        Label = QLabel()
        Label.setText(label)
        
        Box = QVBoxLayout()
        
        Box.addWidget(Label)
        Box.addWidget(self.Combo)
        
        self.setLayout(Box)
        
    def addItem(self, item):
        self.Combo.addItem(item)
        
class plotWidget(QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.graphWidget = pg.PlotWidget()
        self.plotItem = self.graphWidget.plotItem
        self.graphWidget.setBackground('k')

        pen = pg.mkPen(color=(0, 255, 150), width= 2)
        self.plot = self.graphWidget.plot(pen = pen)
        l = pg.GraphicsLayout()
        l.layout.setContentsMargins(0, 0, 0, 0)

        
        self.xaxisWidget = axisWidget(label = 'X axis')
        self.yaxisWidget = axisWidget(label = 'Y axis')
      
        self.axesBox = QHBoxLayout()
        self.axesBox.addWidget(self.xaxisWidget)
        self.axesBox.addWidget(self.yaxisWidget)  
      
        plotLayout = QVBoxLayout()
        plotLayout.addLayout(self.axesBox)
        plotLayout.addWidget(self.graphWidget)
        
        self.XAxisItem = pg.AxisItem('bottom')
        self.XAxisItem.setGrid(255)
        self.YAxisItem = pg.AxisItem('left')
        self.YAxisItem.setGrid(255)
        
        self.XFrameAxisItem = pg.AxisItem('top', showValues = False, maxTickLength = 0)
        self.YFrameAxisItem = pg.AxisItem('right', showValues = False, maxTickLength = 0)


        self.graphWidget.setAxisItems(
            axisItems = {'bottom' : self.XAxisItem, 'left' : self.YAxisItem,
                         'top' : self.XFrameAxisItem, 'right' : self.YFrameAxisItem})
        
        self.setLayout(plotLayout)

class unitsWidget(QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.unitsHandler = unitsConverter()
        self.createLayout()
        self.currentUnitsSpinBox.setValue(1e-8)
        
    @property
    def current_units(self):
        return(self.unitsHandler.current_units)
    
    @property
    def inductance_units(self):
        return(self.unitsHandler.inductance_units)
    
    @property
    def energy_units(self):
        return(self.unitsHandler.energy_units)
    
    @property
    def capacitance_units(self):
        return(self.unitsHandler.capacitance_units)
    
    @property
    def frequency_units(self):
        return(self.unitsHandler.frequency_units)
    
    def updateCurrentUnits(self, units):
        self.unitsHandler.current_units = units
        self.updateInductanceUnits()
        self.updateCapacitanceUnits()
        self.updateEnergyUnits()
        self.updateFrequencyUnits()
    
    def createCurrentUnitsBox(self):
        currentUnitsLabel = QLabel('Current')
        self.currentUnitsSpinBox = ScientificDoubleSpinBox()
        self.currentUnitsSpinBox.setMaximumWidth(120)
        self.currentUnitsSpinBox.setSuffix('A')
        self.currentUnitsSpinBox.setDecimals(1)
        self.currentUnitsSpinBox.valueChanged.connect(self.updateCurrentUnits)
        currentUnitsBox = QVBoxLayout()
        currentUnitsBox.addWidget(currentUnitsLabel)
        currentUnitsBox.addWidget(self.currentUnitsSpinBox)
        return(currentUnitsBox)
    
    def createInductanceUnitsBox(self):
        UnitsLabel = QLabel('Inductance')
        self.inductanceUnitsDisplay = QLabel()
        self.inductanceUnitsDisplay.setMaximumWidth(100)
        self.updateInductanceUnits()
        UnitsBox = QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.inductanceUnitsDisplay)
        return(UnitsBox)
    
    def createCapacitanceUnitsBox(self):
        UnitsLabel = QLabel('Capacitance')
        self.capacitanceUnitsDisplay = QLabel()
        self.capacitanceUnitsDisplay.setMaximumWidth(100)
        self.updateCapacitanceUnits()
        UnitsBox = QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.capacitanceUnitsDisplay)
        return(UnitsBox)
    
    def createEnergyUnitsBox(self):
        UnitsLabel = QLabel('Energy')
        self.energyUnitsDisplay = QLabel()
        self.energyUnitsDisplay.setMaximumWidth(100)
        self.updateEnergyUnits()
        UnitsBox = QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.energyUnitsDisplay)
        return(UnitsBox)
    
    def createFrequencyUnitsBox(self):
        UnitsLabel = QLabel('Frequency')
        self.frequencyUnitsDisplay = QLabel()
        self.frequencyUnitsDisplay.setMaximumWidth(100)
        self.updateFrequencyUnits()
        UnitsBox = QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.frequencyUnitsDisplay)
        return(UnitsBox)
    
    def createPlotUnitsBox(self):
        label = QLabel('Plot units')
        self.plotUnitsCombo = QComboBox()
        self.plotUnitsCombo.setMaximumWidth(130)
        self.plotUnitsCombo.addItems(['SI', 'NINA UNITS'])
        PlotUnitsBox = QVBoxLayout()
        PlotUnitsBox.addWidget(label)
        PlotUnitsBox.addWidget(self.plotUnitsCombo)
        return(PlotUnitsBox)
        
    def createLayout(self):
        unitsBoxHeader = QLabel('Units')
        unitsBoxHeader.setStyleSheet('font-size : 12pt')
        allUnitsBox = QHBoxLayout()
        allUnitsBox.addLayout(self.createCurrentUnitsBox())
        allUnitsBox.addLayout(self.createInductanceUnitsBox())
        allUnitsBox.addLayout(self.createCapacitanceUnitsBox())
        allUnitsBox.addLayout(self.createEnergyUnitsBox())
        allUnitsBox.addLayout(self.createFrequencyUnitsBox())
        allUnitsBox.addLayout(self.createPlotUnitsBox())
        
        unitsBox = QVBoxLayout()
        unitsBox.addWidget(unitsBoxHeader)
        unitsBox.addLayout(allUnitsBox)
        self.setLayout(unitsBox)
    
    def updateInductanceUnits(self):
        self.inductanceUnitsDisplay.setText(
            format_string.format(self.inductance_units) + ' H')
        
    def updateCapacitanceUnits(self):
        self.capacitanceUnitsDisplay.setText(
            format_string.format(self.capacitance_units) + ' F')
        
    def updateEnergyUnits(self):
        self.energyUnitsDisplay.setText(
            format_string.format(self.energy_units) + ' J')
        
    def updateFrequencyUnits(self):
        self.frequencyUnitsDisplay.setText(
            format_string.format(self.frequency_units) + ' Hz')
        
class NloopsWidget(QWidget):
    
    def __init__(self, loop):
        
        super().__init__()
        
        self.loop = loop
        self.signal = updated_signal()
        
        label = QLabel(loop.name + '.Nloops')
        
        self.SpinBox = QSpinBox()
        self.SpinBox.setMaximumWidth(100)
        self.SpinBox.setMinimum(1)
        self.SpinBox.setMaximum(int(1e3))
        self.SpinBox.setValue(1)
        self.SpinBox.valueChanged.connect(self.update)
        
        #this is a nasty trick to align non JJ boxes... Fix it!!!
        self.isFreeLabel = QLabel('')
        self.isFreeLabel.setStyleSheet('font-size: 12px')

        box = QVBoxLayout()
        box.addWidget(label)
        box.addWidget(self.SpinBox)
        box.addWidget(self.isFreeLabel)
        
        self.setLayout(box)
        
    def update(self, value):
        self.loop.Nloops = value
        self.signal.updated.emit()
        
    def updateFreeIndicator(self):
        #only necessary to make this widget be accepted in the elementsBox.
        pass

### THIS IS FOR RESCALING PLOT VIEW



    