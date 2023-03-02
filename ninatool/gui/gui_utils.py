from functools import partial
from .gui_widgets import elementWidget, NloopsWidget

def loop_left_adm(loop, index, units):
    return(loop.left_adm[index] * units.frequency_units)

def loop_right_adm(loop, index, units):
    return(loop.right_adm[index] * units.frequency_units)

def element_adm(element, index, units):
    return(element.adm[index] * units.frequency_units)

def nlosc_gn(nlosc, index, units):
    return(nlosc.gn[index] * units.frequency_units)

def element_phi(element):
    return(element.phi)

def element_i(element, units):
    return(element.i * units.current_units)

def element_flux(element):
    return(element.flux)

def nlosc_phiZPF(nlosc):
    return(nlosc.phiZPF)

def nlosc_nZPF(nlosc):
    return(nlosc.nZPF)

def nlosc_omega(nlosc, units):
    return(nlosc.omega * units.frequency_units)

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
    units = gui.unitsWidget
    create_elementWidgets(gui, branch.elements)
    axisName = branch.name
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.phi')
        axisBox.addItem(axisName + '.i')
        
        for i in range(branch.order):
            axisBox.addItem(axisName + '.u' + str(i + 2))
    
    gui.axesDict[axisName + '.phi'] = \
        partial(element_phi, branch, units)
    gui.axesUnitsDict[axisName + '.phi'] = 'rad'
    
    gui.axesDict[axisName + '.i'] = \
        partial(element_i, branch, units)
    gui.axesUnitsDict[axisName + '.i'] = 'A'
    
    for i in range(branch.order):
        gui.axesDict[axisName + '.u' + str(i + 2)] = \
            partial(element_adm, branch, i, units)
        gui.axesUnitsDict[axisName + '.u' + str(i + 2)] = 'Hz'
    
    #loaded here to first list branch quantities in axes combo
    load_elements(gui, branch)
    link_freePhiWidget(gui)

def load_loop(gui, loop):
    units = gui.unitsWidget
    axisName = loop.name
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.flux')
        
        for i in range(loop.order):
            axisBox.addItem(axisName + '.u' + str(i + 2))
    
    gui.axesDict[axisName + '.flux'] = partial(element_flux, loop)
    gui.axesUnitsDict[axisName + '.flux'] = 'rad'
    
    for i in range(loop.order):
        gui.axesDict[axisName + '.u' + str(i + 2)] = \
            partial(element_adm, loop, i, units)
        gui.axesUnitsDict[axisName + '.u' + str(i + 2)] = 'Hz'
    
    #loaded here to first list the loop quantities in axes combo
    load_branch(gui, loop.associated_branch)
    if loop.has_Lstray:
        create_elementWidget(gui, loop.Lstray)
    #creates widget to change number of identical loops in series
    create_NloopsWidget(gui, loop)

def load_nlosc(gui, nlosc):
    units = gui.unitsWidget
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
    
    gui.axesDict[axisName + '.w'] = partial(nlosc_omega, nlosc, units)
    gui.axesUnitsDict[axisName + '.w'] = 'Hz'
    
    for i in range(nlosc.nlind.order - 1):   
        gui.axesDict[axisName + '.g' + str(i + 3)] = \
            partial(nlosc_gn, nlosc, i, units)
        gui.axesUnitsDict[axisName + '.g' + str(i + 3)] = 'Hz'
    
    #loaded here to first list the nlosc quantities in axes combo
    nlind = nlosc.nlind
    if nlind.kind == 'branch':
        load_branch(gui, nlind)
    elif nlind.kind == 'loop':
        load_loop(gui, nlind)

def load_elements(gui, structure):
    units = gui.unitsWidget
    for element in structure.elements:
        axisName = element.name
        for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
            axisBox.addItem(axisName + '.phi')
            axisBox.addItem(axisName + '.i')
            #adm of a linear inductance is constant, no reason to plot!
            if element.kind != 'L':
                for i in range(structure.order):
                    axisBox.addItem(axisName + '.u' + str(i + 2), units)

        gui.axesDict[axisName + '.phi'] = partial(element_phi, element, units)
        gui.axesUnitsDict[axisName + '.phi'] = 'rad'
        
        gui.axesDict[axisName + '.i'] = partial(element_i, element, units)
        gui.axesUnitsDict[axisName + '.i'] = 'A' 
        #adm of a linear inductance is constant, no reason to plot!
        if element.kind != 'L':
            for i in range(structure.order):
                gui.axesDict[axisName + '.u' + str(i + 2)] = \
                    partial(element_adm, element, i, units)
                gui.axesUnitsDict[axisName + '.u' + str(i + 2)] = 'Hz'
    