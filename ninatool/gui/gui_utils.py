from PyQt5.QtCore import pyqtSignal, QObject
from functools import partial


def loop_left_adm(loop, index):
    return(loop.left_adm[index])

def loop_right_adm(loop, index):
    return(loop.right_adm[index])

def element_adm(element, index):
    return(element.adm[index])

def element_phi(element):
    return(element.phi)

def element_i(element):
    return(element.i)

def nlosc_phiZPF(nlosc):
    return(nlosc.phiZPF)

def nlosc_nZPF(nlosc):
    return(nlosc.nZPF)

def nlosc_omega(nlosc):
    return(nlosc.omega)

def nlosc_gn(nlosc, i):
    return(nlosc.gn[i])

class updated_signal(QObject):
    
    updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        pass

def load_branch(gui, structure):

      axisName = structure.name
      for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
          axisBox.addItem(axisName + '.phi')
          axisBox.addItem(axisName + '.i')
          
          for i in range(structure.order):
              axisBox.addItem(axisName + '.u' + str(i + 2))
          
      gui.axesDict[axisName + '.phi'] = \
          partial(element_phi, structure)
      gui.axesDict[axisName + '.i'] = \
          partial(element_i, structure)
      
      for i in range(gui.structure.order):
          gui.axesDict[axisName + '.u' + str(i + 2)] = \
              partial(element_adm, structure, i)
              
      load_elements(gui, structure)

def load_loop(gui, structure):

      axisName = structure.name
      for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
          axisBox.addItem(axisName + '.flux')
          
          for i in range(structure.order):
              axisBox.addItem(axisName + '.u' + str(i+2))
              ### UNCOMMENT TO SHOW LEFT AND RIGHT LOOP ADMITTANCES ###
              # axisBox.addItem(axisName + '.left_branch.adm' + str(i+2))
              # axisBox.addItem(axisName + '.right_branch.adm' + str(i+2))
      
      gui.axesDict[axisName + '.flux'] = lambda : structure.flux
      
      for i in range(structure.order):
          gui.axesDict[axisName + '.u' + str(i + 2)] = \
              partial(element_adm, structure, i)
              ### UNCOMMENT TO SHOW LEFT AND RIGHT LOOP ADMITTANCES ###
          # gui.axesDict[axisName + '.left_branch.adm' + str(i + 2)] = \
          #     partial(loop_left_adm, structure, i)
          # gui.axesDict[axisName + '.right_branch.adm' + str(i + 2)] = \
          #     partial(loop_right_adm, structure, i)
              
      load_elements(gui, structure)
              
def load_nlosc(gui, structure):
    
    nlind = structure.nlind
    if nlind.kind == 'branch':
        load_branch(gui, nlind)
    elif nlind.kind == 'loop':
        load_loop(gui, nlind)
  
    axisName = structure.name
    
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.phiZPF')
        axisBox.addItem(axisName + '.nZPF')
        axisBox.addItem(axisName + '.w')
        for i in range(structure.nlind.order - 1):
              axisBox.addItem(axisName + '.g' + str(i+3))
              
    gui.axesDict[axisName + '.phiZPF'] = partial(nlosc_phiZPF, structure)
    gui.axesDict[axisName + '.nZPF'] = partial(nlosc_nZPF, structure)
    gui.axesDict[axisName + '.w'] = partial(nlosc_omega, structure)
    for i in range(structure.nlind.order - 1):   
        gui.axesDict[axisName + '.g' + str(i + 3)] = \
            partial(nlosc_gn, structure, i)

def load_elements(gui, structure):
    
    for element in structure.elements:
        axisName = element.name
        for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
            axisBox.addItem(axisName + '.phi')
            axisBox.addItem(axisName + '.i')
            if element.kind != 'L':
                for i in range(structure.order):
                    axisBox.addItem(axisName + '.u' + str(i + 2))
            
        gui.axesDict[axisName + '.phi'] = partial(element_phi, element)
        gui.axesDict[axisName + '.i'] = partial(element_i, element)
        if element.kind != 'L':
            for i in range(structure.order):
                gui.axesDict[axisName + '.u' + str(i + 2)] = \
                    partial(element_adm, element, i)
     