#include <stdio.h>
#include <stdlib.h>
#include <omp.h>


/****************************************************/
/* Solve the lower triangular system L*x = b.       */
/****************************************************/
void  solve_omptest
(int n, int p, double **L, double *b, double *x, int lower)
{
  printf("omp test\n");
  omp_set_num_threads(p);

  int  i;
  int  nn = 16384;
  double  *dx, *dy, *dz;
  dx = (double*)malloc (nn*nn*sizeof (double));
  dy = (double*)malloc (nn*nn*sizeof (double));
  dz = (double*)malloc (nn*nn*sizeof (double));

  #pragma omp parallel
  {
    #pragma omp for
    for (i = 0; i < nn*nn; i++) {
      dy[i] = 1.0;
      dz[i] = 1.0;
      dx[i] = dy[i] + dz[i];
    }
    #pragma omp for
    for (i = 0; i < nn*nn; i++) {
      dy[i] = 1.0;
      dz[i] = 1.0;
      dx[i] = dy[i] + dz[i];
    }
  }
  free (dz);
  free (dy);
  free (dx);
}

