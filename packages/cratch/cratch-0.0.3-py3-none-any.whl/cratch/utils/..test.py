#coding:UTF-8

import ctypes
#import ctypes.util
import numpy as np
import time

def convert_pointer(arr):
    if len(arr.shape) == 1:
        #print('1d array')
        c_double_p = ctypes.POINTER(ctypes.c_double)
        pnt = arr.ctypes.data_as(c_double_p)
    elif len(arr.shape) == 2:
        #print('2d array')
        pnt = (arr.__array_interface__['data'][0]\
              + np.arange(arr.shape[0])*arr.strides[0]).astype(np.uintp)
    else:
        print('arr dimensional error.')
        exit()
    return pnt

def test_lowertrig_solver(lib):
    print('lowertrig')
    #>> ctypes settings
    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    n = 4
    A = np.zeros((n, n), dtype=float)
    b = np.zeros(n, dtype=float)
    x = np.zeros(n, dtype=float)
    lower = True

    A[0][0] = 3.0; A[0][1] = 0.0; A[0][2] = 0.0; A[0][3] = 0.0;
    A[1][0] = 2.0; A[1][1] = 1.0; A[1][2] = 0.0; A[1][3] = 0.0;
    A[2][0] = 1.0; A[2][1] = 0.0; A[2][2] = 1.0; A[2][3] = 0.0;
    A[3][0] = 1.0; A[3][1] = 1.0; A[3][2] = 1.0; A[3][3] = 1.0;
    b[0] = 4.0
    b[1] = 2.0
    b[2] = 4.0
    b[3] = 2.0
    A = convert_pointer(A)
    b = convert_pointer(b)
    x = convert_pointer(x)
    n = c_int(n)
    lower = c_int(lower)

    #''' #default
    lib.solve_triangular.argtypes\
        = [c_int, c_double_pp, c_double_p, c_double_p, c_int]
    lib.solve_triangular.restype = None
    lib.solve_triangular(n, A, b, x, lower)
    #'''

    # OpenMP version
    '''
    p = 2
    p = c_int(p)
    lib.solve_triangular_omp.argtypes\
        = [c_int, c_int, c_double_pp, c_double_p, c_double_p, c_int]
    lib.solve_triangular_omp.restype = None
    lib.solve_triangular_omp(n, p, A, b, x, lower)
    '''


def test_gausselem_triupper(lib):
    #>> ctypes settings
    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    lower = False
    #>> Make test matrix
    n = 50
    epsilon = 1e-4
    maxit = 2*n*n
    numit = 0
    residual = 0.0
    p = 1 # number of threads

    A = np.zeros((n, n), dtype=float)
    b = np.zeros(n, dtype=float)
    x = np.zeros(n, dtype=float)

    for i in range(n):
        b[i] = 2.0*n
        for j in range(n):
            A[i][j] = 1.0
        A[i][i] = n + 1.0

    n = c_int(n)
    lower = c_int(lower)
    A = convert_pointer(A)
    b = convert_pointer(b)
    x = convert_pointer(x)

    '''
    p = 1
    p = c_int(p)
    solver = lib.solve_omptest
    solver.argtypes\
        = [c_int, c_int, c_double_pp, c_double_p, c_double_p, c_int]
    solver.restype = None
    sttime = time.time()
    solver(n, p, A, b, x, lower)
    edtime = time.time()
    print('Time : %lf' % (edtime - sttime))
    exit()
    '''


    #>> Gaussian Elimination
    gelem = lib.GaussianElimination
    gelem.argtypes = [c_int, c_double_pp, c_double_p]
    gelem.restype = None
    gelem(n, A, b)

    ''' default
    lib.solve_triangular.argtypes\
        = [c_int, c_double_pp, c_double_p, c_double_p, c_int]
    lib.solve_triangular.restype = None
    sttime = time.time()
    lib.solve_triangular(n, A, b, x, lower)
    edtime = time.time()
    print('Time : %lf' % (edtime - sttime))
    exit()
    #'''
    #'''
    p = 2
    p = c_int(p)
    solver = lib.solve_triangular_omp
    solver.argtypes\
        = [c_int, c_int, c_double_pp, c_double_p, c_double_p, c_int]
    solver.restype = None
    sttime = time.time()
    solver(n, p, A, b, x, lower)
    edtime = time.time()
    print('Time : %lf' % (edtime - sttime))
    #'''

def test_lu_solver(lib):
    #>> ctypes settings
    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    #>> Make test matrix
    n = 5
    epsilon = 1e-4
    maxit = 2*n*n
    numit = 0
    residual = 0.0
    p = 1 # number of threads

    A = np.zeros((n, n), dtype=float)
    b = np.zeros(n, dtype=float)
    x = np.zeros(n, dtype=float)

    for i in range(n):
        b[i] = 2.0*n
        for j in range(n):
            A[i][j] = 1.0
        A[i][i] = n + 1.0

    #>> Convert valiables to pointers
    n = c_int(n)
    p = c_int(p)
    A_pt = convert_pointer(A)
    b_pt = convert_pointer(b)
    x_pt = convert_pointer(x)
    epsilon = c_double(epsilon)
    maxit = c_int(maxit)
    numit_pt = ctypes.pointer(c_int(numit))
    #'''
    #>> Solver setting
    solver = lib.lu_solver
    solver.argtypes = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    solver(n, A_pt, x_pt, b_pt)
    exit()
    

def test_gauss_seidel(lib):
    #>> ctypes settings
    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    #>> Make test matrix
    n = 10
    epsilon = 1e-4
    maxit = 2*n*n
    numit = 0
    residual = 0.0
    p = 2 # number of threads

    A = np.zeros((n, n), dtype=float)
    b = np.zeros(n, dtype=float)
    x = np.zeros(n, dtype=float)

    for i in range(n):
        b[i] = 2.0*n
        for j in range(n):
            A[i][j] = 1.0
        A[i][i] = n + 1.0

    #>> Convert valiables to pointers
    n = c_int(n)
    p = c_int(p)
    A_pt = convert_pointer(A)
    b_pt = convert_pointer(b)
    x_pt = convert_pointer(x)
    epsilon = c_double(epsilon)
    maxit = c_int(maxit)
    numit_pt = ctypes.pointer(c_int(numit))

    '''
    #>> Solver setting
    solver = lib.jacobi_solver
    #solver = lib.gs_solver
    #solver = lib.sor_solver
    solver.argtypes\
        = [c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    sttime = time.time()
    solver(n, A_pt, x_pt, b_pt)
    edtime = time.time()
    print('Time : %lf' % (edtime - sttime))
    #'''

    #'''
    #>> Solver setting
    solver = lib.gs_solver_omp
    solver.argtypes\
        = [c_int, c_int, c_double_pp, c_double_p, c_double_p]
    solver.restype = None
    sttime = time.time()
    solver(n, p, A_pt, x_pt, b_pt)#, epsilon, maxit, numit_pt)
    edtime = time.time()
    print('Time : %lf' % (edtime - sttime))
    #'''

def main():
    lib_name = 'fem_solver.so'
    lib_path = './lib/'
    #lib_path = './femtools/fem_solver/lib/'
    lib = np.ctypeslib.load_library(lib_name, lib_path)

    #>> ctypes settings
    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    #>> Solve equation by LU solver
    #test_lu_solver(lib)
    #>> Solve equation by Gauss seidel method
    test_gauss_seidel(lib)

    #>> Gaussian elimination and upper triangular solver test
    #test_gausselem_triupper(lib)

    #>> Lower triangular solve test
    #test_lowertrig_solver(lib)




    """
    lib = np.ctypeslib.load_library('fem_solver.so', './lib/')
    row = 2
    col = 5
    n = 4.5
    matrix = np.random.rand(row, col)
    matrix1 = np.random.rand(col)


    ndpointer = np.ctypeslib.ndpointer

    c_int = ctypes.c_int
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(ctypes.c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')

    
    lib.test2d_double.argtypes = [c_double_pp, c_int, c_int, c_double]
    lib.test2d_double.restype = None
    pnt = convert_pointer(matrix)
    

    n = ctypes.c_double(n)
    row = ctypes.c_int(row)
    col = ctypes.c_int(col)


    print('before:\n', matrix)
    lib.test2d_double(pnt, row, col, n)
    print('after:\n', matrix)


    #row1 = 5
    #matrix1 = np.random.rand(row1)
    #row1 = ctypes.c_int(row1)

    lib.test1d_double.argtypes = [c_double_p, c_int, c_double]
    lib.test1d_double.restype = None
    pnt = convert_pointer(matrix1)

    print('before:\n', matrix1)
    lib.test1d_double(pnt, col, n)
    print('after:\n', matrix1)
    """



    print('OK')

if __name__=='__main__':
    main()
