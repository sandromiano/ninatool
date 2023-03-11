from sympy import symbols, diff
from sympy import cos as sp_cos
from numpy import array, ndarray, sin, cos, arcsin
from .support_functions import invert_representation_partial, \
                               series_combination_partial


def check_real_number(value):
    if isinstance(value, float) or isinstance(value, int):
        return(True)
    else:
        return(False)

class Nlind(object) :
    '''
    Nlind describes an abstract nonlinear inductance. Is the main parent
    class in NINA.
    '''
    def __init__(self, 
                 order,
                 name = ""):
        '''
        Parameters
        ----------
        order : INT
            Maximum order for potential energy expansion coefficients.
        name : STR, optional
            Name of the Nlind instance. Useful for debugging and GUI
        '''

        self.__order = order
        self.__invert_repr = invert_representation_partial(self.order)
        self.__series_combination = series_combination_partial(self.order)
        
        self.__kind = 'Nlind'
        self.__name = name
        
        self.__observer = None
        self.__observed = []
        
        self.__phi = 0
        self.__i = 0
        self.__U = 0
        self.__L = 0
        
        self.__ic = 0
        self.__L0 = 0 

        self.__adm = None
        self.__imp = None

    ### PROPERTIES GETTERS ###

    @property
    def order(self):
        return(self.__order)
    
    @property
    def invert_repr(self):
        '''
        Returns a partial function which converts nlind.adm to nlind.imp
        and viceversa.
        '''
        return(self.__invert_repr)
    
    @property
    def series_combination(self):
        '''
        Returns a partial function which computes the nlind.adm of two elements
        in series.
        '''
        return(self.__series_combination)
    
    @property
    def name(self):
        return(self.__name)
    
    @property
    def kind(self):
        return(self.__kind)
    
    @property
    def observer(self):
        '''
        Returns the observer of the nlind instance. The observer is typically
        notified when the nlind instance is subject to some change, for
        instance, the critical current of a JJ is modified.
        '''
        return(self.__observer)
    
    @property
    def observed(self):
        '''
        Returns a list of nlind instances observed by self. Useful for debug.
        '''
        return(self.__observed)

    @property
    def phi(self):
        '''
        Returns the total phase drop across self, in radiants.
        '''
        return(self.__phi)

    @property
    def i(self):
        '''
        Returns the current flowing through self.
        '''
        return(self.__i)

    @property
    def U(self):
        '''
        Returns the potential energy of self.
        '''
        return(self.__U)
    
    @property
    def L(self):
        '''
        Returns the differential linear inductance of self.
        '''
        return(self.__L)
    
    @property
    def ic(self):
        '''
        Returns the critical current of self.
        '''
        return(self.__ic)
    
    @property
    def L0(self):
        '''
        Returns the zero-bias inductance of self.
        '''
        return(self.__L0)

    @property
    def adm(self):
        '''
        Returns the admittance-like potential energy 
        expansion coefficients of self.
        '''
        return(self.__adm)

    @property
    def imp(self):
        '''
        Returns the impedance-like potential energy 
        expansion coefficients of self.
        '''
        return(self.__imp)

    ### PROPERTIES SETTERS ###

    @observer.setter
    def observer(self, observer):
        self.__observer = observer

    @phi.setter
    def phi(self, phi):
        
        if not isinstance(phi, ndarray):
            if check_real_number(phi):
                phi = array([phi])
            else:
                raise ValueError("Cannot set " + self.name + ".phi. Value " +\
                                 "needs to be either an array or real number.")
        
        self.__phi = phi
        self.calc_current()
        self.calc_potential()
        self.calc_inductance()
        self.calc_coeffs()

    @i.setter
    def i(self, i):
        self.__i = i
        self.calc_phase()
        self.calc_potential()
        self.calc_inductance()
        self.calc_coeffs()

    @ic.setter
    def ic(self, ic):
        self.__ic = ic
        
    @L0.setter
    def L0(self, L0):
        self.__L0 = L0

    @adm.setter
    def adm(self, adm):
        self.__adm = array(adm)
        self.__imp = array(self.invert_repr(adm))
        
    @imp.setter
    def imp(self, imp):
        self.__imp = array(imp)
        self.__adm = array(self.invert_repr(imp))
    
    ### METHODS ###
    
    def add_observed(self, observed):
        self.__observed.append(observed)
        
    ### CHILD-SPECIFIC METHODS, TO BE OVERRIDEN BY THE DERIVED CLASSES

    def calc_phase(self):
        pass

    def calc_current(self):
        pass

    def calc_potential(self):
        pass

    def calc_inductance(self):
        pass
    
    def calc_coeffs(self):
        pass
    
    ### END OF 'Nlind' CLASS ###

class L(Nlind):
    '''
    Class of linear inductance.
    '''
    def __init__(self, 
                 L, 
                 order = 3, 
                 name = ""):
        '''
        Parameters
        ----------
        L : FLOAT
            Linear inductance value in dimensionless NINA inductance units.
        order : INT, optional
            Maximum order for potential energy expansion coefficients.
        name : STR, optional
            Name of L instance.
        '''
        super().__init__(order = order)
        
        self._Nlind__kind = 'L'
        self._Nlind__name = name

        self.L0 = L
        
        self.calc_coeffs()
    
    @property
    def EL(self):
        return(1/self.L0)
    
    ### CLASS-SPECIFIC SETTERS, OVERRIDE Nlind ONES    
    
    @Nlind.ic.setter
    def ic(self, value):
        self._Nlind__ic = value
        self._Nlind__L0 = 1/value
        self.calc_coeffs()
        #updates observer if any
        if self.observer is not None:
            self.observer.update()
        
    @Nlind.L0.setter
    def L0(self, value):
        self._Nlind__L0 = value
        self._Nlind__ic = 1/value
        self.calc_coeffs()
        #updates observer if any
        if self.observer is not None:
            self.observer.update()

    ### CLASS-SPECIFIC METHODS, OVERRIDE Nlind ONES

    def calc_current(self):
        '''
        Computes the current flowing through the L instance as a function of 
        the phase drop across it.
        '''
        self._Nlind__i = self.phi / (self.L0)

    def calc_phase(self):
        '''
        Computes the phase drop across the L instance as a function of the 
        current flowing through it.
        '''
        self._Nlind__phi = self.L0 * self.i

    def calc_potential(self):
        '''
        Computes the potential energy of the L instance as a function of the 
        phase drop across it.
        '''
        self._Nlind__U = pow(self.phi, 2) / (2 * self.L0)
    
    def calc_inductance(self):
        '''
        Computes the differential linear inductance of the L instance, which
        coincides with the zero-bias inductance L0.
        '''
        self._Nlind__L = self.L0
                  
    def calc_coeffs(self):
        #impedance of a linear inductance is nonzero only for first order
        imp_list = [self.L0] + [0.0 for i in range(self.order - 1)]
        #the reshape allows consistent ndarray operations
        self.imp = array(imp_list).reshape(self.order, 1)
    
    ### END OF 'L' CLASS ###

class J(Nlind):
    '''
    Class of Josephson tunnel junction (JJ).
    '''
    def __init__(self, 
                 ic, 
                 order = 3, 
                 name = ""):
        '''
        Parameters
        ----------
        ic : FLOAT
            JJ critical current in dimensionless NINA current units.
        order : TYPE, optional
            Maximum order for potential energy expansion coefficients.
        name : STR, optional
            Name of J instance.
        '''
        super().__init__(order = order)

        self._Nlind__kind = 'J'
        self._Nlind__name = name
        
        self.ic = ic

        self.__is_free = True
        
        self.calc_coeffs()
        
    ### CLASS-SPECIFIC PROPERTIES

    @property
    def is_free(self):
        '''
        Returns bool flag marking if the J instance is a "free JJ".
        '''
        return(self.__is_free)
    
    @property
    def EJ(self):
        return(self.ic)

    ### CLASS-SPECIFIC SETTERS, 'ic' and 'L0' OVERRIDE Nlind ONES

    @Nlind.ic.setter
    def ic(self, value):
        self._Nlind__ic = value
        self._Nlind__L0 = 1/value
        self.calc_coeffs()
        #updates observer if any
        if self.observer is not None:
            self.observer.update()
        
    @Nlind.L0.setter
    def L0(self, value):
        self._Nlind__L0 = value
        self._Nlind__ic = 1/value
        self.calc_coeffs()
        #updates observer if any
        if self.observer is not None:
            self.observer.update()
            
    @is_free.setter
    def is_free(self, value):
        self.__is_free = value

    ### CLASS-SPECIFIC METHODS, OVERRIDE Nlind ONES

    def calc_current(self):
        '''
        Computes the current flowing through the J instance as a function of 
        the phase drop across it. Can be updated to include higher order 
        effects as second harmonic, etc.
        '''
        self._Nlind__i = self.ic * sin(self.phi)

    def calc_phase(self):
        '''
        Computes the phase drop across the J instance as a function of the
        current flowing through it. Implicitly assumes that the JJ is
        constrained.
        '''
        self._Nlind__phi = arcsin(self.i / self.ic)
 
    def calc_potential(self):
        '''
        Computes the potential energy of the J instance as a function of the 
        phase drop across it.
        '''
        self._Nlind__U = self.ic * (1 - cos(self.phi))

    def calc_inductance(self):
        '''
        Computes the differential linear inductance of the J instance as
        a function of the phase drop across it.
        '''
        self._Nlind__L = self.L0 / cos(self.phi)

    def calc_coeffs(self):
        '''
        Computes potential energy expansion coefficients of the J instance
        for all the values of the phase drop across it.
        '''
        phi = symbols('phi', real = True)
        adm_list = [self.ic * sp_cos(phi)]

        for i in range(self.order - 1):
            adm_list.append(diff(adm_list[-1], phi))
        
        keys = {'phi' : self.phi, 'cos' : cos, 'sin' : sin}
        self.adm = [eval(str(adm_list[i]), keys) for i in range(self.order)]

    ### END OF 'J' CLASS ###
    
class C(object):
    
    def __init__(self, name = ''):
        
        self.__kind = 'C'
        self.__name = name
        self.__C = 1
    
    @property
    def kind(self):
        return(self.__kind)
    
    @property
    def name(self):
        return(self.__name)
    
    @property
    def C(self):
        return(self.__C)
    
    @property
    def EC(self):
        return(1/self.C)
    
    @C.setter
    def C(self, value):
        self.__C = value
        
        