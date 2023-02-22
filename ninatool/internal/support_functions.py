import sympy as sp
import numpy as np
import os

symbolic_maps_dir = os.path.dirname((__file__)) + '/mapping_functions/'

def check_order(elements):
    '''
    Simple function to check that all the "nlind" elements have same order.
    Raises a "ValueError" if orders don't match.
    '''
    checklist = [elem.order == elements[0].order for elem in elements]
        
    if not all(checklist):
        raise ValueError('The elements do not have all the same order.')
    return(elements[0].order)

def f_exprs(order):
    '''
    This function computes symbolic expression of inverse function taylor
    expansion coefficients. 
    
    Assuming "y = f(x)" and "x = g(y)", f and g are inverse of each other.
    
    If the taylor expansion of g(y) 
    
    g(y) = sum(g_n/n!) * y**n
    is known up to a certain "order" = n + 1,
    
    this function computes the coefficients of the taylor expansion of
    f(x) = sum(f_n/n!) * x**n.
    
    It returns a list of string expressions, representing the 
    f_n(g_0, g_1, ... g_n)
    coefficients that can be later evaluated with "eval" method, once
    g_n coefficients are known.
    '''
    
    ### independent variable of g(y)
    y = sp.symbols('y', real = True)
    ### list of g(y) functions
    gs = [sp.Function('g' + str(i))(y) for i in range(order)]
    ### list of f(g(y)) functions
    fs = [1/gs[0]]
    ### list of derivatives of g(y) functions
    dgs = [sp.diff(g, y) for g in gs[:-1]]
    ### list of substitutions for derivatives of g(y) functions
    dgs_sub = gs[1:] 
    ### list of g symbols
    g_syms = [sp.symbols('g[' + str(i) + ']') for i in range(order)]
    ### list of f symbols
    f_syms = [1/g_syms[0]]
    
    def subs_diff(f):
        '''
        Substitutes first derivatives of g functions
        with next order g functions in f(g(y)) expressions.
        '''       
        for dg, dg_sub in zip(dgs, dgs_sub):
            f = f.subs(dg, dg_sub)
        return(f)
    
    def subs_sym(f):
        '''
        Substitutes g functions with g symbols in f expressions.
        '''
        for g, g_sym in zip(gs, g_syms):
            f = f.subs(g, g_sym)
        return(f)

    ### Generates f functions expressed with g symbols ###    
    for i in range(order - 1):
        ### f[n] = 1/g[0] * df[n-1]
        df = 1/gs[0] * sp.diff(fs[-1],y)
        df = subs_diff(df) 
        fs.append(sp.apart(df, fs[0]))    
        f_syms.append(subs_sym(fs[-1]))
    
    f_exprs = [str(f_sym) for f_sym in f_syms]    
    return(f_exprs)

def generate_invert_representation_file(order):
    print('Generating new symbolic map for inverting representation to order ' 
          +  str(order) + '...')
    fs = f_exprs(order)
    filename = 'O' + str(order) + '.txt'
    filepath = symbolic_maps_dir + filename
    
    with open(filepath, 'w') as file:
        for line in fs:
            file.write(line + '\n')
    
def invert_representation_partial(order):   
    filename = 'invert_representation_O30.txt'
    filepath = symbolic_maps_dir + filename
    fs = []
    
    with open(filepath, 'r') as file:
        fs = [file.readline().strip('\n') for i in range(order)]

    def invert_representation(vals):
        
        return(np.array([eval(f, {'g' : vals}) for f in fs]))   
    
    return(invert_representation)

def series_combination_partial(order):

    filename = 'series_combination_O14.txt'
    filepath = symbolic_maps_dir + filename
    fs = []
    
    with open(filepath, 'r') as file:
        fs = [file.readline().strip('\n') for i in range(order)]
    
    def series_combination(a_adm, b_adm):
        
        return(np.array([eval(f, {'a': a_adm, 'b' : b_adm}) for f in fs]))
    
    return(series_combination)

