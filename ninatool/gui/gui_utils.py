from functools import partial
from .gui_widgets import elementWidget

def loop_left_adm(loop, index):
    return(loop.left_adm[index])

def loop_right_adm(loop, index):
    return(loop.right_adm[index])

def element_adm(element, index):
    return(element.adm[index])

def nlosc_gn(nlosc, index):
    return(nlosc.gn[index])

def element_phi(element):
    return(element.phi)

def element_i(element):
    return(element.i)

def element_flux(element):
    return(element.flux)

def nlosc_phiZPF(nlosc):
    return(nlosc.phiZPF)

def nlosc_nZPF(nlosc):
    return(nlosc.nZPF)

def nlosc_omega(nlosc):
    return(nlosc.omega)

def update_freePhase(nlind, gui):
    
    nlind.free_phi = gui.freePhiWidget.freePhase
    gui.update_axes()

def link_freePhiWidget(gui):
    
    if gui.structure.kind == 'branch' or gui.structure.kind == 'loop':
        nlind = gui.structure
    elif gui.structure.kind == 'nlosc':
        nlind = gui.structure.nlind
    gui.freePhiWidget.signal.updated.connect(partial(update_freePhase, nlind, gui))
    

def create_elementWidgets(gui, elements):
    
    for element in elements:
        widget = elementWidget(element)
        widget.signal.updated.connect(gui.update_axes)
        gui.elementsBox.addWidget(widget)
    
def load_branch(gui, branch):

    create_elementWidgets(gui, branch.elements)

    axisName = branch.name
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.phi')
        axisBox.addItem(axisName + '.i')
        
        for i in range(branch.order):
            axisBox.addItem(axisName + '.u' + str(i + 2))
        
    gui.axesDict[axisName + '.phi'] = \
        partial(element_phi, branch)
    gui.axesDict[axisName + '.i'] = \
        partial(element_i, branch)
    
    for i in range(branch.order):
        gui.axesDict[axisName + '.u' + str(i + 2)] = \
            partial(element_adm, branch, i)
    
    #loaded here to first list branch quantities in axes combo
    load_elements(gui, branch)
    link_freePhiWidget(gui)

def load_loop(gui, loop):
    
    axisName = loop.name
    for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
        axisBox.addItem(axisName + '.flux')
        
        for i in range(loop.order):
            axisBox.addItem(axisName + '.u' + str(i + 2))
    
    gui.axesDict[axisName + '.flux'] = partial(element_flux, loop)
    
    for i in range(loop.order):
        gui.axesDict[axisName + '.u' + str(i + 2)] = \
            partial(element_adm, loop, i)
    
    #loaded here to first list the loop quantities in axes combo
    load_branch(gui, loop.associated_branch)

def load_nlosc(gui, nlosc):
    
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
    gui.axesDict[axisName + '.nZPF'] = partial(nlosc_nZPF, nlosc)
    gui.axesDict[axisName + '.w'] = partial(nlosc_omega, nlosc)
    for i in range(nlosc.nlind.order - 1):   
        gui.axesDict[axisName + '.g' + str(i + 3)] = \
            partial(nlosc_gn, nlosc, i)
    
    #loaded here to first list the nlosc quantities in axes combo
    nlind = nlosc.nlind
    if nlind.kind == 'branch':
        load_branch(gui, nlind)
    elif nlind.kind == 'loop':
        load_loop(gui, nlind)

def load_elements(gui, structure):
    
    for element in structure.elements:
        axisName = element.name
        for axisBox in [gui.xaxisWidget.Combo, gui.yaxisWidget.Combo]:
            axisBox.addItem(axisName + '.phi')
            axisBox.addItem(axisName + '.i')
            #adm of a linear inductance is constant, no reason to plot!
            if element.kind != 'L':
                for i in range(structure.order):
                    axisBox.addItem(axisName + '.u' + str(i + 2))
            
        gui.axesDict[axisName + '.phi'] = partial(element_phi, element)
        gui.axesDict[axisName + '.i'] = partial(element_i, element)
        #adm of a linear inductance is constant, no reason to plot!
        if element.kind != 'L':
            for i in range(structure.order):
                gui.axesDict[axisName + '.u' + str(i + 2)] = \
                    partial(element_adm, element, i)
     