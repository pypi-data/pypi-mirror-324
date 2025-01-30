#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

void  solve_triangular_upper_omp
( int n, double **U, double *b, double *x );
void  solve_triangular_lower_omp
( int n, double **L, double *b, double *x );

/* ***************************************************
 * Solve the triangular system with OpenMP.
 * lower is flag
 * lower = 0 (False) : use solve_triangular_upper
 * lower = 1 (True ) : use solve_triangular_lower
   *************************************************** */
void  solve_triangular_omp
( int n, int p, double **A, double *b, double *x, int lower)
{
  omp_set_num_threads(p);
  printf("omp\n");

  if (lower == 0) {
    solve_triangular_upper_omp(n, A, b, x);
  } else if (lower == 1) {
    solve_triangular_lower_omp(n, A, b, x);
  }
}


/* ***************************************************
 * Solve the lower triangular system L*x = b.
   *************************************************** */
void  solve_triangular_lower_omp
( int n, double **L, double *b, double *x )
{
  int  i, j;
  /*
  for (i = 0; i < n; i++) {
    x[i] = b[i];
    for (j = 0; j < i; j++) {
      x[i] = x[i] - L[i][j]*x[j];
    }
    x[i] = x[i] / L[i][i];
  }
  */

  for (i = 0; i < n; i++) {
    x[i] = b[i];
    #pragma omp parallel shared(L, x) private(j)
    {
      #pragma omp for
      for (j = 0; j < i; j++)
	x[i] = x[i] - L[i][j]*x[j];
    }
    x[i] = x[i] / L[i][i];
  }
  /*
  for (i = 0; i < n; i++) {
    printf("%10.3e\n", x[i]);
  }
  */
}

/* ***************************************************
 * Solve the upper triangular system L*x = b.
   *************************************************** */
void solve_triangular_upper_omp
( int n, double **U, double *b, double *x )
{
  int  i, j;
  /*
  for (i = n-1; i > -1; i--) {
    x[i] = b[i];
    for (j = i+1; j < n; j++) {
      x[i] = x[i] - U[i][j]*x[j];
    }
    x[i] = x[i] / U[i][i];
  }
  */

  for (i = n-1; i > -1; i--) {
    x[i] = b[i];
    #pragma omp parallel shared(U, x) private(j)
    {
      #pragma omp for
      for (j = i+1; j < n; j++)
	x[i] = x[i] - U[i][j]*x[j];
    }
    x[i] = x[i] / U[i][i];
  }

  /*
  printf("x\n");
  for (i = 0; i < n; i++) {
    printf("%10.3e\n", x[i]);
  }
  */
}
