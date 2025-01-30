###############################################################################
# File:     Makefile
# Author:   Takuya TOYOSHI
# Updated:  Dec. 15 2023
# Created:  Apr. 18 2023
# Copyright: (c) 2023 Takuya TOYOSHI
#
# Makefile for fem solver
###############################################################################

### ::: Compile options ::: ###
#CC	= icc
#CFLAGS	= -O3 -Wall -fPIC - qopenmp
CC	= gcc-13
CFLAGS	= -O3 -Wall -fPIC -fopenmp
LIBS	= -lm -lmpi

### ::: Command macros ::: ###
RM	= rm -f
MV	= mv

### ::: Target informations ::: ###
SRCDIR	= ./src/
LIBDIR	= ./lib/
TARGET	= $(LIBDIR)fem_solver.so
OBJS	= fem_solver_ssor.o\
	solve_gs.o\
	solve_gs_omp.o\
	gaussian_elimination.o\
	solve_triangular.o\
	solve_triangular_omp.o\
	solve_jacobi.o\
	solve_sor.o\
	solve_mpi.o\
	solve_omptest.o\
	solve_lu.o

OBJ	= $(addprefix $(SRCDIR), $(OBJS))

### ::: Dependencies & Compile ::: ###
all:	$(TARGET)
$(TARGET):	$(OBJ)
	$(CC) $(CFLAGS) $(LIBS) -shared -o $(TARGET) $(OBJ)

# Make rules
.c.o:
	$(CC) $(CFLAGS) $(LIBS) -o $@ -c $<

clean:
	$(RM) $(TARGET) $(OBJ)
