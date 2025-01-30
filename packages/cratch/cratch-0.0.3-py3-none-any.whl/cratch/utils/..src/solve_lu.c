#include <stdio.h>
#include <stdlib.h>


static  void  LUDecomposition
(int n, double **A)
{
  int  i, j, k;

  for (i = 0; i < n - 1; i++) {
    for (j = i + 1; j < n; j++) {
      double m = A[j][i] / A[i][i];

      for (k = i + 1; k < n; k++) {
	A[j][k] -= m*A[i][k];
      }
      A[j][i] = m;
    }
  }
}

static  void  LUSolve
(int n, double **A, double *x, double *b)
{
  int  i, j;

  for (i = 0; i < n; i++) {
    double ax = 0.0;

    for (j = 0; j < i; j++) {
      ax += A[i][j]*b[j];
    }
    b[i] -= ax;
  }

  for (i = n - 1; i >= 0; i--) {
    double ax = 0.0;

    for (j = i + 1; j < n; j++) {
      ax += A[i][j]*x[j];
    }
    x[i] = (b[i] - ax) / A[i][i];
  }
}

void lu_solver
(int n, double **A, double *x, double *b)
{
  printf("LU solver\n");
  LUDecomposition(n, A);

  LUSolve(n, A, x, b);
}


void lu_solver_full
(int n, double **A, double *x, double *b)
{
  int  i, j;
  double  sum1, sum2;

  double  *y = (double*)malloc (n*sizeof(double));
  double  **L = (double**)malloc (n*sizeof (double*));
  double  **U = (double**)malloc (n*sizeof (double*));

  for (i = 0; i < n; i++) {
    y[i] = b[i];
    L[i] = (double *)malloc (n*sizeof (double));
    U[i] = (double *)malloc (n*sizeof (double));
    for (j = 0; j < n; j++) {
      L[i][j] = 0.0; U[i][j] = 0.0;
    }
    L[i][i] = 1.0;
  }

  int k, l;
  // LU decomposition
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      if (i <= j) {
        sum1 = 0.0;
        for (k = 0; k <= i-1; k++) {
          sum1 += L[i][k] * U[k][j];
        }
        U[i][j] = A[i][j] - sum1;
      } else if (i > j) {
        sum2 = 0.0;
        for (l = 0; l <= j-1; l++) {
          sum2 += L[i][l] * U[l][j];
        }
        L[i][j] = (A[i][j] - sum2) / U[j][j];
      }
    }
  }

  // forward substitution Ly = b
  for (j = 0; j < n-1; j++) {
    for (i = j+1; i < n; i++) {
      y[i] -= y[j] * L[i][j];
    }
  }

  // backward substitution Ux = y
  for (i = 0; i < n; i++) {
    x[i] = y[i];
  }

  for (j = n-1; j >= 0; j--) {
    x[j] /= U[j][j];
    for (i = 0; i <= j-1; i++) {
      x[i] -= U[i][j] * x[j];
    }
  }

  free (*U);
  free (*L);
  free (U);
  free (L);
  free (y);
}
