from ninatool.internal.elements import L, J
from ninatool.internal.structures import loop

class rfsquid(loop):

    def __init__(self,
                 i0 = 1,
                 L0 = .1,
                 L1 = .5,
                 order = 3,
                 name = 'rfsquid',
                 **kwargs):
        
        _J0 = J(i0, order = order, name = 'J0')
        _L0 = L(L0, order = order, name = 'L0')
        _L1 = L(L1, order = order, name = 'L1')

        left_branch = [_J0, _L0]
        right_branch = [_L1]
        
        super().__init__(left_branch = left_branch,
                         right_branch = right_branch,
                         name = name,
                         **kwargs)
        
class dcsquid(loop):
    
    def __init__(self,
                 i0 = 1,
                 L0 = .1,
                 i1 = .9,
                 L1 = .5,
                 order = 3,
                 name = 'dcsquid',
                 **kwargs):
        
        _J0 = J(i0, order = order, name = 'J0')
        _L0 = L(L0, order = order, name = 'L0')
        _J1 = J(i1, order = order, name = 'J1')
        _L1 = L(L1, order = order, name = 'L1')
 
        left_branch = [_J0, _L0]
        right_branch = [_J1, _L1]
        
        super().__init__(left_branch = left_branch,
                         right_branch = right_branch,
                         name = name,
                         **kwargs)
        
class snail(loop):
    
    def __init__(self,
                 i0 = 1,
                 a = .2,
                 order = 3,
                 name = 'snail',
                 **kwargs):
        
        _J0 = J(a * i0, order = order, name = 'J0')
        _J1 = J(i0, order = order, name = 'J1')
        _J2 = J(i0, order = order, name = 'J2')
        _J3 = J(i0, order = order, name = 'J3')


        left_branch = [_J0]
        right_branch = [_J1, _J2, _J3]
        
        super().__init__(left_branch = left_branch,
                         right_branch = right_branch,
                         name = name,
                         **kwargs)