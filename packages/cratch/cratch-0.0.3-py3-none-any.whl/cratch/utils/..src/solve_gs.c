#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/***********************************************************
 * Gauss-Seidel method for solve A*x = b.
 *
 * Parameters
 * ----------
 * n        : the dimensional the system.
 * A        : an n-by-n matrix A[i][i] != 0.0.
 * x        : start vector for the iteration.
 * b        : an n-dimensional vector.
 *
***********************************************************/

void  gs_solver
(int n, double **A, double *x, double *b)
{
  int  i, j;
  int  ite = 0;
  double  eps = 1.0e-8;
  double  resi = 0.0;
  double  *dx = (double*)malloc (n*sizeof (double));
  printf("Gauss-Seidel solver\n");

  while (1) {
    ite ++;
    resi = 0.0;
    for (i = 0; i < n; i++) {
      dx[i] = b[i];
      for (j = 0; j < n; j++) dx[i] -= A[i][j]*x[j];

      dx[i] /= A[i][i];
      x[i] += dx[i];
      resi += sqrt( dx[i]*dx[i] );
    }
    fprintf(stderr, "\r     ite:%6d, residual:%.4e", ite, resi);
    if (resi <= eps) break;
  }
  printf("\n");

  free(dx);
}
