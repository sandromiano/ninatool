from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5 import QtWidgets
import pyqtgraph as pg
from numpy import linspace, array, inf
from scipy.constants import pi, h, elementary_charge
from .scientific_spinbox import ScienDSpinBox as ScientificDoubleSpinBox
from .led_indicator import LedIndicator

Phi0 = h / (2 * elementary_charge)
format_string = '{:.3g}'

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
            self.isFreeLabel.setStyleSheet('font-size: 12px')
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
                                               font-size: 12px')
            else:
                self.isFreeLabel.setStyleSheet('color : lightgray; \
                                               font-weight: bold; \
                                               font-size: 12px')

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
        
class multivaluedWidget(QtWidgets.QWidget):

    def __init__(self):
        
        super().__init__()

        self.Led = LedIndicator()
        label = QtWidgets.QLabel('multivalued')

        box = QtWidgets.QHBoxLayout()
        box.addWidget(self.Led)
        box.addWidget(label)
        box.addStretch()
        box.setSpacing(10)
        
        self.setLayout(box)
        
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
        
        self.XAxisItem = pg.AxisItem('bottom')
        self.XAxisItem.setGrid(255)
        self.YAxisItem = pg.AxisItem('left')
        self.YAxisItem.setGrid(255)

        self.graphWidget.setAxisItems(
            axisItems = {'bottom' : self.XAxisItem, 'left' : self.YAxisItem})
        
        self.setLayout(plotLayout)

class unitsWidget(QtWidgets.QWidget):
    
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
        self.unitsHandler.set_current_units(units = units)
        self.updateInductanceUnits()
        self.updateCapacitanceUnits()
        self.updateEnergyUnits()
        self.updateFrequencyUnits()
    
    def createCurrentUnitsBox(self):
        currentUnitsLabel = QtWidgets.QLabel('Current')
        self.currentUnitsSpinBox = ScientificDoubleSpinBox()
        self.currentUnitsSpinBox.setMaximumWidth(80)
        self.currentUnitsSpinBox.setSuffix('A')
        self.currentUnitsSpinBox.setDecimals(1)
        self.currentUnitsSpinBox.valueChanged.connect(self.updateCurrentUnits)
        currentUnitsBox = QtWidgets.QVBoxLayout()
        currentUnitsBox.addWidget(currentUnitsLabel)
        currentUnitsBox.addWidget(self.currentUnitsSpinBox)
        return(currentUnitsBox)
    
    def createInductanceUnitsBox(self):
        UnitsLabel = QtWidgets.QLabel('Inductance')
        self.inductanceUnitsDisplay = QtWidgets.QLabel()
        self.inductanceUnitsDisplay.setMaximumWidth(100)
        self.updateInductanceUnits()
        UnitsBox = QtWidgets.QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.inductanceUnitsDisplay)
        return(UnitsBox)
    
    def createCapacitanceUnitsBox(self):
        UnitsLabel = QtWidgets.QLabel('Capacitance')
        self.capacitanceUnitsDisplay = QtWidgets.QLabel()
        self.capacitanceUnitsDisplay.setMaximumWidth(100)
        self.updateCapacitanceUnits()
        UnitsBox = QtWidgets.QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.capacitanceUnitsDisplay)
        return(UnitsBox)
    
    def createEnergyUnitsBox(self):
        UnitsLabel = QtWidgets.QLabel('Energy')
        self.energyUnitsDisplay = QtWidgets.QLabel()
        self.energyUnitsDisplay.setMaximumWidth(100)
        self.updateEnergyUnits()
        UnitsBox = QtWidgets.QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.energyUnitsDisplay)
        return(UnitsBox)
    
    def createFrequencyUnitsBox(self):
        UnitsLabel = QtWidgets.QLabel('Frequency')
        self.frequencyUnitsDisplay = QtWidgets.QLabel()
        self.frequencyUnitsDisplay.setMaximumWidth(100)
        self.updateFrequencyUnits()
        UnitsBox = QtWidgets.QVBoxLayout()
        UnitsBox.addWidget(UnitsLabel)
        UnitsBox.addWidget(self.frequencyUnitsDisplay)
        return(UnitsBox)
        
    def createLayout(self):
        unitsBoxHeader = QtWidgets.QLabel('Units')
        unitsBoxHeader.setStyleSheet('font-size : 12pt')
        allUnitsBox = QtWidgets.QHBoxLayout()
        allUnitsBox.addLayout(self.createCurrentUnitsBox())
        allUnitsBox.addLayout(self.createInductanceUnitsBox())
        allUnitsBox.addLayout(self.createCapacitanceUnitsBox())
        allUnitsBox.addLayout(self.createEnergyUnitsBox())
        allUnitsBox.addLayout(self.createFrequencyUnitsBox())
        
        unitsBox = QtWidgets.QVBoxLayout()
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
        self.frequencyUnitsDisplay.setText(format_string.format(self.frequency_units) + ' Hz')

class NloopsWidget(QtWidgets.QWidget):
    
    def __init__(self, loop):
        
        super().__init__()
        
        self.loop = loop
        self.signal = updated_signal()
        
        label = QtWidgets.QLabel(loop.name + '.Nloops')
        
        self.SpinBox = QtWidgets.QSpinBox()
        self.SpinBox.setMinimum(1)
        self.SpinBox.setMaximum(int(1e3))
        self.SpinBox.setValue(1)
        self.SpinBox.valueChanged.connect(self.update)
        
        #this is a nasty trick to align non JJ boxes... Fix it!!!
        self.isFreeLabel = QtWidgets.QLabel('')
        self.isFreeLabel.setStyleSheet('font-size: 12px')

        box = QtWidgets.QVBoxLayout()
        box.addWidget(label)
        box.addWidget(self.SpinBox)
        box.addWidget(self.isFreeLabel)
        
        self.setLayout(box)
        
    def update(self, value):
        self.loop.Nloops = value
        self.signal.updated.emit()
        
    def updateFreeIndicator(self):
        pass
        
class unitsConverter(object):
    
    def __init__(self):
        
        self.__current_units = 1e-6    
    
    @property
    def current_units(self):
        return(self.__current_units)
    
    @property
    def inductance_units(self):
        return(Phi0 / (2 * pi * self.current_units))
    
    @property
    def energy_units(self):
        return(Phi0  * self.current_units / (2 * pi))
    
    @property
    def capacitance_units(self):
        return(pi * elementary_charge ** 2 / (Phi0 * self.current_units))
    
    @property
    def frequency_units(self):
        return(self.energy_units / h)
        
    def set_current_units(self, units):
        self.__current_units = units

    