#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

/***********************************************************
 * Gauss-Seidel method for solve A*x = b. [OpenMP version]
 *
 * Parameters
 * ----------
 * n        : the dimensional the system.
 * A        : an n-by-n matrix A[i][i] != 0.0.
 * x        : start vector for the iteration.
 * b        : an n-dimensional vector.
 *
***********************************************************/

void  gs_solver_omp
(int n, int p, double **A, double *x, double *b)
{
  int  i, j;
  int  ite = 0;
  int  id, jstart, jstop;
  int  dnp = n / p;
  double  dxi = 0.0;
  double  eps = 1.0e-8;
  double  resi = 0.0;
  double  *dx = (double*)malloc (n*sizeof (double));
  printf("Gauss-Seidel solver [OpenMP]\n");

  omp_set_num_threads(p);

  while (1) {
    ite ++;
    resi = 0.0;
    for (i = 0; i < n; i++) {
      dx[i] = b[i];
      #pragma omp parallel \
	shared(A, x) private(id, j, jstart, jstop, dxi)
      {
	id = omp_get_thread_num();
	jstart = id*dnp;
	jstop = jstart + dnp;
	dxi = 0.0;
	for (j = jstart; j < jstop; j++)
	//#pragma omp for
	//for (j = 0; j < n; j++)
	  dxi += A[i][j]*x[j];
	#pragma omp critical
	  dx[i] -= dxi;
      }
      //for (j = 0; j < n; j++) dx[i] -= A[i][j]*x[j];

      dx[i] /= A[i][i];
      x[i] += dx[i];
      //resi += ((dx[i] >= 0.0) ? dx[i] : -dx[i]);
      resi += sqrt ( dx[i]*dx[i]);
    }
    fprintf(stderr, "\r     ite:%6d, residual:%.4e", ite, resi);
    if (resi <= eps) break;
  }
  printf("\n");

  free(dx);
}
