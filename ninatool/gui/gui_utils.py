from functools import partial
from .gui_widgets import elementWidget, NloopsWidget

def findComboBoxIndex(ComboBox, text):
    indx = ComboBox.findText(text)
    return(indx)

def loop_left_adm(loop, index, unitsWidget):
    #checks plot units selection
    if unitsWidget.plotUnitsCombo.currentText() == 'SI':
        scale_factor = unitsWidget.frequency_units
    elif unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
        scale_factor = 1
    return(loop.left_adm[index] * scale_factor)

def loop_right_adm(loop, index, unitsWidget):
    #checks plot units selection
    if unitsWidget.plotUnitsCombo.currentText() == 'SI':
        scale_factor = unitsWidget.frequency_units
    elif unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
        scale_factor = 1
    return(loop.right_adm[index] * scale_factor)

def loop_left_phi(loop):
    #checks plot units selection
    return(loop.left_phi)

def loop_right_phi(loop):
    #checks plot units selection
    return(loop.right_phi)

def loop_phi(loop):
    #checks plot units selection
    return(loop.phi)

def element_adm(element, index, unitsWidget):
    #checks plot units selection
    if unitsWidget.plotUnitsCombo.currentText() == 'SI':
        scale_factor = unitsWidget.frequency_units
    elif unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
        scale_factor = 1
    return(element.adm[index] * scale_factor)

def nlosc_gn(nlosc, index, unitsWidget):
    #checks plot units selection
    if unitsWidget.plotUnitsCombo.currentText() == 'SI':
        scale_factor = unitsWidget.frequency_units
    elif unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
        scale_factor = 1
    return(nlosc.gn[index] * scale_factor)

def element_phi(element):
    return(element.phi)

def element_i(element, unitsWidget):
    #checks plot units selection
    if unitsWidget.plotUnitsCombo.currentText() == 'SI':
        scale_factor = unitsWidget.current_units
    elif unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
        scale_factor = 1
    return(element.i * scale_factor)

def element_U(element, unitsWidget):
    #checks plot units selection
    if unitsWidget.plotUnitsCombo.currentText() == 'SI':
        scale_factor = unitsWidget.frequency_units
    elif unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
        scale_factor = 1
    return(element.U * scale_factor)

def element_flux(element):
    return(element.flux)

def nlosc_phiZPF(nlosc):
    return(nlosc.phiZPF)

def nlosc_nZPF(nlosc):
    return(nlosc.nZPF)

def nlosc_omega(nlosc, unitsWidget):
    #checks plot units selection
    if unitsWidget.plotUnitsCombo.currentText() == 'SI':
        scale_factor = unitsWidget.frequency_units
    elif unitsWidget.plotUnitsCombo.currentText() == 'NINA UNITS':
        scale_factor = 1
    return(nlosc.omega * scale_factor)

def update_freePhase(nlind, gui):
    
    nlind.free_phi = gui.freePhiWidget.freePhase
    gui.update_axes()

def link_freePhiWidget(gui):
    
    if gui.structure.kind == 'branch' or gui.structure.kind == 'loop':
        nlind = gui.structure
    elif gui.structure.kind == 'nlosc':
        nlind = gui.structure.nlind
    gui.freePhiWidget.signal.updated.connect(partial(update_freePhase, nlind, gui))

def create_elementWidget(gui, element):
    widget = elementWidget(element)
    widget.signal.updated.connect(gui.update_axes)
    gui.elementsBox.addWidget(widget)
    
def create_elementWidgets(gui, elements):
    for element in elements:
        create_elementWidget(gui, element)
        
def create_NloopsWidget(gui, loop):
    widget = NloopsWidget(loop)
    widget.signal.updated.connect(gui.update_axes)
    gui.elementsBox.addWidget(widget)
    
def load_branch(gui, branch):
    unitsWidget = gui.unitsWidget
    create_elementWidgets(gui, branch.elements)
    axisName = branch.name
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.phi')
        axisBox.addItem(axisName + '.i')
        axisBox.addItem(axisName + '.U')
        
        for i in range(branch.order):
            axisBox.addItem(axisName + '.u' + str(i + 2))
    
    gui.axesDict[axisName + '.phi'] = \
        partial(element_phi, branch)
    gui.axesUnitsDict[axisName + '.phi'] = 'rad'
    
    gui.axesDict[axisName + '.i'] = \
        partial(element_i, branch, unitsWidget)
    gui.axesUnitsDict[axisName + '.i'] = 'A'
    
    gui.axesDict[axisName + '.U'] = \
        partial(element_U, branch, unitsWidget)
    gui.axesUnitsDict[axisName + '.U'] = 'Hz'
    
    for i in range(branch.order):
        gui.axesDict[axisName + '.u' + str(i + 2)] = \
            partial(element_adm, branch, i, unitsWidget)
        gui.axesUnitsDict[axisName + '.u' + str(i + 2)] = 'Hz'
    
    #loaded here to first list branch quantities in axes combo
    load_elements(gui, branch)
    link_freePhiWidget(gui)

def load_loop(gui, loop):
    unitsWidget = gui.unitsWidget
    axisName = loop.name
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.flux')
        axisBox.addItem(axisName + '.left_phi')
        axisBox.addItem(axisName + '.right_phi')
        axisBox.addItem(axisName + '.phi')
        
        for i in range(loop.order):
            axisBox.addItem(axisName + '.u' + str(i + 2))
    
    gui.axesDict[axisName + '.flux'] = partial(element_flux, loop)
    gui.axesUnitsDict[axisName + '.flux'] = 'rad'
    
    gui.axesDict[axisName + '.left_phi'] = partial(loop_left_phi, loop)
    gui.axesUnitsDict[axisName + '.left_phi'] = 'rad'
    
    gui.axesDict[axisName + '.right_phi'] = partial(loop_right_phi, loop)
    gui.axesUnitsDict[axisName + '.right_phi'] = 'rad'
    
    gui.axesDict[axisName + '.phi'] = partial(loop_phi, loop)
    gui.axesUnitsDict[axisName + '.phi'] = 'rad'
    
    for i in range(loop.order):
        gui.axesDict[axisName + '.u' + str(i + 2)] = \
            partial(element_adm, loop, i, unitsWidget)
        gui.axesUnitsDict[axisName + '.u' + str(i + 2)] = 'Hz'
        
        gui.axesDict[axisName + '.left_branch.u' + str(i + 2)] = \
            partial(loop_left_adm, loop, i, unitsWidget)
        gui.axesUnitsDict[axisName + '.left_branch.u' + str(i + 2)] = 'Hz'
        
        gui.axesDict[axisName + '.right_branch.u' + str(i + 2)] = \
            partial(loop_right_adm, loop, i, unitsWidget)
        gui.axesUnitsDict[axisName + '.right_branch.u' + str(i + 2)] = 'Hz'
    
    #loaded here to first list the loop quantities in axes combo
    load_branch(gui, loop.associated_branch)
    if loop.has_Lstray:
        create_elementWidget(gui, loop.Lstray)
    #creates widget to change number of identical loops in series
    create_NloopsWidget(gui, loop)

def load_nlosc(gui, nlosc):
    unitsWidget = gui.unitsWidget
    #creates elementWidget for the nlosc capacitor
    create_elementWidgets(gui, [nlosc.cElem])
  
    axisName = nlosc.name
    
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.phiZPF')
        axisBox.addItem(axisName + '.nZPF')
        axisBox.addItem(axisName + '.w')
        for i in range(nlosc.nlind.order - 1):
              axisBox.addItem(axisName + '.g' + str(i + 3))
    
    gui.axesDict[axisName + '.phiZPF'] = partial(nlosc_phiZPF, nlosc)
    gui.axesUnitsDict[axisName + '.phiZPF'] = 'rad'
    
    gui.axesDict[axisName + '.nZPF'] = partial(nlosc_nZPF, nlosc)
    gui.axesUnitsDict[axisName + '.nZPF'] = ''
    
    gui.axesDict[axisName + '.w'] = partial(nlosc_omega, nlosc, unitsWidget)
    gui.axesUnitsDict[axisName + '.w'] = 'Hz'
    
    for i in range(nlosc.nlind.order - 1):   
        gui.axesDict[axisName + '.g' + str(i + 3)] = \
            partial(nlosc_gn, nlosc, i, unitsWidget)
        gui.axesUnitsDict[axisName + '.g' + str(i + 3)] = 'Hz'
    
    #loaded here to first list the nlosc quantities in axes combo
    nlind = nlosc.nlind
    if nlind.kind == 'branch':
        load_branch(gui, nlind)
    elif nlind.kind == 'loop':
        load_loop(gui, nlind)

def load_elements(gui, structure):
    unitsWidget = gui.unitsWidget
    for element in structure.elements:
        axisName = element.name
        for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
            axisBox.addItem(axisName + '.phi')
            axisBox.addItem(axisName + '.i')
            axisBox.addItem(axisName + '.U')
            #adm of a linear inductance is constant, no reason to plot!
            if element.kind != 'L':
                for i in range(structure.order):
                    axisBox.addItem(axisName + '.u' + str(i + 2), unitsWidget)

        gui.axesDict[axisName + '.phi'] = \
            partial(element_phi, element)
        gui.axesUnitsDict[axisName + '.phi'] = 'rad'
        
        gui.axesDict[axisName + '.i'] = \
            partial(element_i, element, unitsWidget)
        gui.axesUnitsDict[axisName + '.i'] = 'A'
        
        gui.axesDict[axisName + '.U'] = \
            partial(element_U, element, unitsWidget)
        gui.axesUnitsDict[axisName + '.U'] = 'Hz'
        #adm of a linear inductance is constant, no reason to plot!
        if element.kind != 'L':
            for i in range(structure.order):
                gui.axesDict[axisName + '.u' + str(i + 2)] = \
                    partial(element_adm, element, i, unitsWidget)
                gui.axesUnitsDict[axisName + '.u' + str(i + 2)] = 'Hz'
    