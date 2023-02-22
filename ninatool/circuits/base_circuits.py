from ninatool.internal.elements import L, J
from ninatool.internal.structures import loop

class rfsquid(loop):

    def __init__(self,
                 i0 = 1,
                 L0 = .1,
                 L1 = .5,
                 order = 3,
                 name = 'rfsquid'):
        
        self.J0 = J(i0, order = order, name = 'J0')
        self.L0 = L(L0, order = order, name = 'L0')
        self.L1 = L(L0, order = order, name = 'L1')

        left_branch = [self.J0, self.L0]
        right_branch = [self.L1]
        
        super().__init__(left_branch = left_branch,
                         right_branch = right_branch,
                         name = name)
        
class dcsquid(loop):
    
    def __init__(self,
                 i0 = 1,
                 L0 = .1,
                 i1 = .9,
                 L1 = .5,
                 order = 3,
                 name = 'dcsquid'):
        
        self.J0 = J(i0, order = order, name = 'J0')
        self.L0 = L(L0, order = order, name = 'L0')
        self.J1 = J(i1, order = order, name = 'J1')
        self.L1 = L(L1, order = order, name = 'L1')


        left_branch = [self.J0, self.L0]
        right_branch = [self.J1, self.L1]
        
        super().__init__(left_branch = left_branch,
                         right_branch = right_branch,
                         name = name)
        
class snail(loop):
    
    def __init__(self,
                 a = .2,
                 order = 3,
                 name = 'snail'):
        
        self.J0 = J(a, order = order, name = 'J0')
        self.J1 = J(1, order = order, name = 'J1')
        self.J2 = J(1, order = order, name = 'J2')
        self.J3 = J(1, order = order, name = 'J3')


        left_branch = [self.J0]
        right_branch = [self.J1, self.J2, self.J3]
        
        super().__init__(left_branch = left_branch,
                         right_branch = right_branch,
                         name = name)