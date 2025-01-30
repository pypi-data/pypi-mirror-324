#include <stdio.h>
#include <stdlib.h>

void GaussianElimination
(int n, double **A, double *b)
/*
 * Gaussian elimination program
 */
{
  int  i, j, k;
  double  ratio;

  for (i = 0; i < n-1; i++) {
    if (A[i][i] == 0.0){
      printf("Mathematical error!"); exit(0);
    }

    for (j = i+1; j < n; j++) {
      ratio = A[j][i] / A[i][i];
      for (k = 0; k < n; k++) {
	A[j][k] = A[j][k] - ratio*A[i][k];
      }
      b[j] = b[j] - ratio*b[i];
    }
  }
  /*
  for (i = 0; i < n; i++) {
    for (j = 0; j < n; j++) {
      printf("%10.3f", A[i][j]);
    }
    printf("\n");
  }
  for (i = 0; i < n; i++) {
    printf("%10.3f\n", b[i]);
  }
  */
}
