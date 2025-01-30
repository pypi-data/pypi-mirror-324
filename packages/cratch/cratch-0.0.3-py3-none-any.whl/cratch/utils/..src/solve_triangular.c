#include <stdio.h>
#include <stdlib.h>

void  solve_triangular_upper ( int n, double **U, double *b, double *x );
void  solve_triangular_lower ( int n, double **L, double *b, double *x );

/* ****************************************************/
/* Solve the triangular system.*/
/* lower is flag
 * lower = 0 (False) : use solve_triangular_upper
 * lower = 1 (True ) : use solve_triangular_lower
   *************************************************** */
void  solve_triangular
( int n, double **A, double *b, double *x, int lower)
{
  if (lower == 0) {
    solve_triangular_upper(n, A, b, x);
  } else if (lower == 1) {
    solve_triangular_lower(n, A, b, x);
  }
}


/* ***************************************************
 * Solve the lower triangular system L*x = b.
   *************************************************** */
void  solve_triangular_lower
( int n, double **L, double *b, double *x )
{
  int  i, j;

  for (i = 0; i < n; i++) {
    x[i] = b[i];
    for (j = 0; j < i; j++) {
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
void solve_triangular_upper
( int n, double **U, double *b, double *x )
{
  int  i, j;
  for (i = n-1; i > -1; i--) {
    x[i] = b[i];
    for (j = i+1; j < n; j++) {
      x[i] = x[i] - U[i][j]*x[j];
    }
    x[i] = x[i] / U[i][i];
  }
  /*
  for (i = 0; i < n; i++) {
    printf("%10.3e\n", x[i]);
  }
  */
}
