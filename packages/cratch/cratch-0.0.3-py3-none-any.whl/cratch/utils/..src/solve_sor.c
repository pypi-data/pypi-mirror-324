#include <stdio.h>
#include <stdlib.h>
#include <math.h>

/***********************************************************
 * Successive Over-Relaxation method for solve A*x = b.
 *
 * Parameters
 * ----------
 * n        : the dimensional the system.
 * A        : an n-by-n matrix A[i][i] != 0.0.
 * x        : start vector for the iteration.
 * b        : an n-dimensional vector.
 *
***********************************************************/

void  sor_solver
(int n, double **A, double *x, double *b)
{
  int  i, j;
  int  ite = 0;
  double  sum1, sum2;
  double  eps = 1.0e-8;
  double  resi = 0.0;
  double  omega = 1.1;
  double  *dx = (double*)malloc (n*sizeof (double));
  printf("SOR solver\n");

  while (1) {
    ite++;
    resi = 0.0;
    for (i = 0; i < n; i++) {
      sum1 = 0.0; sum2 = 0.0;
      for (j = 0; j < i; j++)
	sum1 += A[i][j]*x[j];
      for (j = i+1; j < n; j++)
	sum2 += A[i][j]*x[j];
      dx[i] = (1.0 - omega)*x[i];
      dx[i] += (omega / A[i][i])*(b[i] - sum1 - sum2);
      resi += sqrt( (dx[i] - x[i])*(dx[i] - x[i]) );
      x[i] = dx[i];
    }
    fprintf(stderr, "\r     ite:%6d, residual:%.4e", ite, resi);
    if (resi <= eps) break;
  }
  printf("\n");

  free(dx);
}
