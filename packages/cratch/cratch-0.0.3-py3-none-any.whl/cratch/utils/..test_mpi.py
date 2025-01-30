#coding:UTF-8

import numpy as np
import ctypes
import time
import os

from mpi4py import MPI

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def convert_pointer(arr):
    """
    numpy 配列をc言語ライブラリ用のポインタに変換

    Parameters
    ----------
    arr : ndarray(1D) or ndarray(2D)
        data type is float

    Returns
    -------
    pnt : pointer
    """
    if len(arr.shape) == 1: # 1 dimensional array
        c_double_p = ctypes.POINTER(ctypes.c_double)
        pnt = arr.ctypes.data_as(c_double_p)
    elif len(arr.shape) == 2: # 2 dimensional array
        pnt = (arr.__array_interface__['data'][0]\
              + np.arange(arr.shape[0])*arr.strides[0]).astype(np.uintp)
    else:
        print('Array dimensional error [exit]')
        exit()
    return pnt

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def solve_parallel_jacobi(lib):
    """
    Solve equation by Parallel (MPI) Jacobi method

    Parameters
    ----------
    lib : library information
    """
    #>> ctypes settings
    ndpointer = np.ctypeslib.ndpointer
    c_int = ctypes.c_int
    c_int_p = ctypes.POINTER(c_int)
    c_int_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_double = ctypes.c_double
    c_double_p = ctypes.POINTER(c_double)
    c_double_pp = ndpointer(dtype=np.uintp, ndim=1, flags='C')
    c_char_p = ctypes.c_char_p

    #>> Make test matrix
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    n = 20
    if rank == 0: # 計算する行列の生成(テスト用)
        A, b, x = make_testmat(n)
    else: # rank0以外はダミー行列を生成
        A, b, x = make_dummy(n)

    #>> Convert pointer of variables
    A = convert_pointer(A)
    b = convert_pointer(b)
    x_pt = convert_pointer(x)
    n = c_int(n)

    #>> Select method
    method = convert_char('jacobi')
    #method = convert_char('sor')

    #>> Set MPI communication parameter
    if MPI._sizeof(MPI.Comm) == ctypes.sizeof(ctypes.c_int):
        MPI_Comm = ctypes.c_int
    else:
        MPI_Comm = ctypes.c_void_p
    comm_ptr = MPI._addressof(MPI.COMM_WORLD)
    comm_val = MPI_Comm.from_address(comm_ptr)

    #>> Solver setting
    solver = lib.mpi_solver
    solver.restype = None
    solver.argtypes = [MPI_Comm, c_char_p, c_int,\
                       c_double_p, c_double_p, c_double_p]
    #>> Solve equation
    if rank == 0:
        print(x)
    solver(comm_val, method, n, A, b, x_pt)
    a = 10
    print('a',a)
    #MPI.Finalize()
    if rank == 0:
        print(x)
    exit()

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def convert_char(string):
    return ctypes.create_string_buffer(string.encode('utf-8'))

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def make_testmat(n):
    A = np.zeros((n, n), dtype=float)
    b = np.zeros(n, dtype=float)
    x = np.zeros(n, dtype=float)

    for i in range(n):
        b[i] = 2.0*n
        for j in range(n):
            A[i][j] = 1.0
        A[i][i] = n + 1.0
    A = A.flatten()
    return A, b, x

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def make_dummy(n):
    A = np.zeros(1, dtype=float)
    b = np.zeros(n, dtype=float)
    x = np.zeros(n, dtype=float)
    return A, b, x

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def main():
    #print("process: %d" % os.getpid())
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    #print(rank)
    lib_name = 'fem_solver.so'
    lib_path = './lib/'
    solvelib = np.ctypeslib.load_library(lib_name, lib_path)

    '''
    if rank == 0:
        A = np.zeros(12, dtype=float)
    else:
        A = np.ones(12, dtype=float)
    A = convert_pointer(A)
    #>> Set MPI communication parameter
    if MPI._sizeof(MPI.Comm) == ctypes.sizeof(ctypes.c_int):
        MPI_Comm = ctypes.c_int
    else:
        MPI_Comm = ctypes.c_void_p
    comm_ptr = MPI._addressof(MPI.COMM_WORLD)
    comm_val = MPI_Comm.from_address(comm_ptr)
    solver = solvelib.mpi_solver2(comm_val, A)

    a = 10
    print(a)

    exit()
    '''

    #>> Solve equation by Parallel (MPI) Jacobi method
    solve_parallel_jacobi(solvelib)
    print('OK')

if __name__=='__main__':
    main()
