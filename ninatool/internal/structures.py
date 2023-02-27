import logging
import numpy as np
from numpy import pi
from .elements import Nlind, L, J
from .support_functions import check_order

NUM_POINTS = 1001 # number of points for default phase array
NUM_PERIODS = 2 # number of periods for default phase array

default_phase_array = NUM_PERIODS * 2 * pi * np.linspace(-.5, .5, NUM_POINTS)

class branch(Nlind):
    '''
    Series combination of linear inductances and Josephson junctions.
    Can compute current-phase relation, energy-phase relation,
    inductance-phase relation and potential energy expansion coefficients.
    '''
    def __init__(self, 
                 elements = [J(1)],
                 is_free = True, 
                 name = '', 
                 observe_elements = True,
                 manipulate_elements = True):
        '''
        Parameters
        ----------
        elements : LIST of J and L instances.
            Default is [L(1)], just a linear inductance.
        is_free : BOOL, optional
            Defines if the branch has a free JJ in it. Default is TRUE
        name : STR, optional
            Name of the branch instance.
        observe_elements : BOOL, optional
            Defines if the branch has to be updated when any of its elements
            is modified. Default is TRUE.
        manipulate_elements : BOOL, optional
            Defines if the branch is allowed to manipulate its elements. 
            Can be set to false to define a branch which only computes its 
            properties once those of its elements are known. Default is TRUE.
        '''
        order = check_order(elements)
        super().__init__(order = order)

        self._Nlind__kind = 'branch'
        self._Nlind__name = name

        self.__elements = elements
        self.__is_linear = False
        self.__is_free = is_free
        self.__free_element = None
        self.__free_phi = default_phase_array
        self.__multivalued = False
        self.__manipulate_elements = manipulate_elements
        #parses the branch to identify the free JJ and the constrained elements
        self.parse()
        #if required, the branch subscribes to receive update 
        #notifications from its elements.
        if self.__manipulate_elements and observe_elements:
            self.subscribe()
        #solves the branch
        self.solve()
    ### BRANCH SPECIFIC GETTERS ###
    
    @property
    def elements(self):
        return(self.__elements)
    
    @property
    def is_linear(self):
        return(self.__is_linear)
    
    @property
    def is_free(self):
        return(self.__is_free)
    
    @property
    def free_element(self):
        return(self.__free_element)
    
    @property
    def free_phi(self):
        return(self.__free_phi)
    
    @property
    def beta(self):
        return(self.__beta)
    
    @property
    def multivalued(self):
        return(self.__multivalued)
    
    @property
    def JJs(self):
        return(self.__JJs)
    
    @property
    def constrained_elements(self):
        return(self.__constrained_elements)

    @property
    def num_elements(self):
        return(len(self.elements))
    
    @property
    def L0(self):
        return(sum(element.L0 for element in self.elements))

    ### BRANCH-SPECIFIC SETTERS ###
    
    @is_free.setter
    def is_free(self, value):
        self.__is_free = value
        self.parse()
        
    @free_phi.setter
    def free_phi(self, value):
        logging.debug('called free_phi setter of branch ' + str(self.name))
        if self.__manipulate_elements:
            self.__free_phi = value
            if self.is_free:
                self.free_element.phi = self.free_phi
                #if only the free phase is changed, no need to re-parse.
                self.update(parse = False)
            else:
                print(self.name + ' is constrained, free phase cannot be set.')
        else:
            print(self.name + ' is not allowed to manipulate elements.')
    
    @Nlind.i.setter 
    def i(self, i):
        self._Nlind__i = i
        for elem in self.elements:
            elem.i = self.i
    #----------------------------------------------------------------------------------------------------------------------#
    
    def subscribe(self):
        logging.debug('called subscribe method of branch ' + str(self.name))
        
        for element in self.elements:
            self.add_observed(element)
            element.observer = self
            
    def parse(self):
        logging.debug('called parse method of branch ' + str(self.name))
        #zero bias linear inductance of the branch
        #list of all the JJs in the branch
        self.__JJs = [elem for elem in self.elements if elem.kind == 'J']
        #if the branch does not have JJs, it is assumed to be linear.
        #this will have to change when more nonlinear elements will be
        #allowed in the branch class.
        if len(self.JJs) == 0:
            self.__is_linear = True
            self.__constrained_elements = self.elements
            #this is just a nasty trick to not recreate everytime the
            #effective free element for a linear branch.
            if self.__free_element is None:
                self.__free_element = L(self.L0, order = self.order)
            else:
                self.__free_element.L0 = self.L0
                
        else:
            self.__is_linear = False
            #defines critical current of the branch
            self._Nlind__ic = min(JJ.ic for JJ in self.JJs)
            
            if self.__is_free:
                #list of possible free JJs
                free_JJs = [JJ for JJ in self.JJs if JJ.ic == self.ic]
                #if multiple free JJs, only one will be picked
                if len(free_JJs) > 1:
                    logging.info("More than one free JJ present. " + 
                    "Only one of them will be allowed to actually be free.")
                self.__free_element = free_JJs[0]
                self.__free_element.is_free = True
                logging.info(self.free_element.name + ' is free element of ' + 
                             'branch ' + self.name)
            else:
                self.__free_element = None
                self.__free_phi = None
            #list of constrained elements
            self.__constrained_elements = \
                list(set(self.elements) - set([self.free_element]))
            #labels constrained JJs as not free
            for element in self.constrained_elements:
                if element.kind == 'J':
                    element.is_free = False
                    
            if self.__is_free:
                self.check_multivalued()
                #updates the new free element with the previously defined
                #free phase of the branch. Necessary if, after a parameter
                #change, a previously constrained JJ becomes the free JJ.
                
                #free_element.phi is only assigned here if the branch is
                #allowed to manipulate the elements and has already been
                #assigned a free_phi value
                if self.__manipulate_elements and self.free_phi is not None:
                    self.free_element.phi = self.free_phi
            
    def check_multivalued(self):
        logging.debug('called check_multivalued method of branch '
                      + str(self.name))
        
        self.__constrained_L0 = \
            sum(other.L0 for other in self.__constrained_elements)
        
        self.__beta = self.__constrained_L0 / self.free_element.L0
        
        if self.beta < 1 and self.__is_free:
            logging.info('Branch ' + str(self.name) + ' is multivalued.')
            self.__multivalued = True
        else:
            self.__multivalued = False

    def solve(self):
        logging.debug('called solve method of branch ' + str(self.name))
        #the solver assigns current to constrained elements only if is
        #allowed to manipulate elements. Otherwise, it just calculates
        #its own quantities.
        if self.__manipulate_elements:
            self._Nlind__i = self.free_element.i
            for elem in self.constrained_elements:
                elem.i = self._Nlind__i

        self.calc_all()
    
    def update(self, parse = True):
        logging.debug('called update method of branch ' + str(self.name))
        
        if parse:
            self.parse()
        self.solve()
        if self.observer is not None:
            self.observer.update()
                
    def calc_phase(self):
        logging.debug('called calc_phase method of branch '
                      + str(self.name))
        
        self._Nlind__phi = sum([elem.phi for elem in self.elements])

    def calc_potential(self):
        logging.debug('called calc_potential method of branch '
                      + str(self.name))
        
        self._Nlind__U = sum([elem.U for elem in self.elements])

    def calc_inductance(self):
        logging.debug('called calc_inductance method of branch '
                      + str(self.name))
        
        self._Nlind__L = sum([elem.L for elem in self.elements])

    def calc_coeffs(self):
        logging.debug('called calc_coeffs method of branch '
                      + str(self.name))
        
        if self.is_linear:
            self.free_element.L0 = self.L0
            self.adm = self.free_element.adm
        elif not self.is_free:
            self.imp = sum([elem.imp for elem in self.elements])
        elif len(self.constrained_elements) == 0:
            self.adm = self.free_element.adm
        else:             
            #for the constrained elements, the expansion coefficients can
            #be computed with the impedance-like representation and then
            #inverted (the invert_repr map can still be singular if there is
            #a constrained JJ with same critical current as the free JJ)
            constrained_imp = sum([elem.imp for elem in self.constrained_elements])
            constrained_adm = self.invert_repr(constrained_imp)
            #the total branch expansion coefficients are then obtained
            #combining the free JJ admittance-like with the total constrained
            #elements admittance-like coefficients.
            self.adm = self.series_combination(self.free_element.adm, 
                                               constrained_adm)
    
    def calc_all(self):
        
        logging.debug('called calc_all method of branch '
                      + str(self.name))
        
        self.calc_phase()
        self.calc_potential()
        self.calc_inductance()
        self.calc_coeffs()
        
    def interpolate_results(self, phi_grid = default_phase_array):
        
            if self.__multivalued:
                print('Cannot interpolate multivalued results (yet).')
            else:
                for elem in self.elements:
                    elem.phi = np.interp(phi_grid, self.phi, elem.phi)

                self._Nlind__i = self.free_element.i
                self.calc_all()
                
class loop(Nlind):
    
    def __init__(self, 
                 left_branch, 
                 right_branch, 
                 name = '',
                 observe_associated = True):
        
        self.__left_elements = left_branch
        self.__right_elements = right_branch
        
        self.elements = self.left_elements + self.right_elements
        
        self._Nlind__order = check_order(self.elements)
        
        super().__init__(order = self._Nlind__order)
        
        self._Nlind__kind = "loop"
        self._Nlind__name = name
        #the associated branch is responsible for computing the equilibrium
        #points of the loop
        self.__associated_branch = branch(elements = self.elements, 
                                          observe_elements = True,
                                          name = self.name + 
                                          '.associated_branch')
        #left and right branch are responsible for computing the expansion
        #coefficients of each arm of the dipole, after the associated branch
        #has computed the equilibium points. left and right branches CANNOT
        #manipulate the elements.
        #these branches do not have to observe elements, otherwise
        #will overwrite the associated branch as observer.
        #In future, the associated branch will not be used and then these
        #internal branches will have to be updated.
        self.left_branch = branch(elements = self.left_elements,
                                  observe_elements = False,
                                  is_free = self.free_element in self.left_elements,
                                  name = self.name + '.left_branch',
                                  manipulate_elements = False)
        #creates a mask array to invert the sign of odd coefficients for left
        #branch (default choice in the paper). Necessary to correctly compute 
        #the dipole admittance when solving the loop equilibrium points via 
        #the associated branch.
        adm_mask_list = [(-1) ** i for i in range(self.order)]
        #the reshape allows consistent ndarray operations
        self.adm_mask = np.array(adm_mask_list).reshape(self.order, 1)
        
        self.right_branch = branch(elements = self.right_elements,
                                   observe_elements = False,
                                   is_free = self.free_element in self.right_elements,
                                   name = self.name + '.right_branch',
                                   manipulate_elements = False)
        
        if observe_associated:
            self.subscribe()
            
        self.calc_coeffs()

    ### LOOP-SPECIFIC GETTERS ###

    @property
    def associated_branch(self):
        return(self.__associated_branch)
    
    @property
    def flux(self):
        return(self.associated_branch.phi)
    
    @property
    def free_phi(self):
        return(self.associated_branch.free_phi)
    
    @property
    def free_element(self):
        return(self.associated_branch.free_element)
    
    @property
    def multivalued(self):
        return(self.associated_branch.multivalued)
    
    @property
    def left_elements(self):
        return(self.__left_elements)

    @property
    def right_elements(self):
        return(self.__right_elements)

    @property
    def left_adm(self):
        return(self.left_branch.adm * self.adm_mask)
    
    @property
    def right_adm(self):
        return(self.right_branch.adm)
    ### LOOP-SPECIFIC SETTERS ###

    @free_phi.setter
    def free_phi(self, value):
        
        logging.debug('called free_phi setter of loop ' + str(self.name))    
        self.associated_branch.free_phi = value

    ### LOOP-SPECIFIC METHODS ###

    def subscribe(self):
        
        logging.debug('called subscribe method of loop ' + str(self.name))
        
        self.add_observed(self.associated_branch)
        self.associated_branch.observer = self
            
    def calc_coeffs(self):
        
        logging.debug('called calc_coeffs method of loop ' + str(self.name))
        
        self.left_branch.calc_coeffs()
        self.right_branch.calc_coeffs()

        self.adm = self.left_adm + self.right_adm
        
    def update(self):
        
        logging.debug('called update method of loop ' + str(self.name))
        
        self.left_branch.is_free = self.free_element in self.left_elements
        self.right_branch.is_free = self.free_element in self.right_elements

        self.calc_coeffs()
        
    def interpolate_results(self, phi_grid = default_phase_array):
        
        self.associated_branch.interpolate_results(phi_grid = phi_grid)
        self.update()
        
class Nlosc:
    
    def __init__(self, nlind, name = ''):
        
        self.__name = name
        self.__kind = 'Nlosc'
        self.__nlind = nlind
        self.__EC = 1

    @property
    def name(self):
        return(self.__name)
    
    @property
    def kind(self):
        return(self.__kind)
    
    @property
    def nlind(self):
        return(self.__nlind)
    
    @property
    def multivalued(self):
        return(self.nlind.multivalued)
    
    @property
    def EC(self):
        return(self.__EC)
        
    @property
    def phiZPF(self):
        return(1/np.sqrt(2) * (8 * self.EC / self.nlind.adm[0]) ** 0.25)
    
    @property
    def nZPF(self):
        return(1/np.sqrt(2) * (self.nlind.adm[0] / (8 * self.EC)) ** 0.25)
    
    @property
    def omega(self):
        #missing hbar at denominator
        return(np.sqrt(8 * self.EC * self.nlind.adm[0]))
    
    @property
    def gn(self):
        #missing hbar at denominator
        factorial_array = np.array([np.math.factorial(i + 3) 
                                    for i in range(self.nlind.order - 1)])
        
        factorial_array = factorial_array.reshape(self.nlind.order -1, 1)
        
        return(self.phiZPF * self.nlind.adm[1:] / factorial_array)
        
    @EC.setter
    def EC(self, value):
        self.__EC = value
        