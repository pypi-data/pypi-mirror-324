#include <stdio.h>
#include <math.h>



void check_include(int jj, int *nodeID, int numIDs, int *flg_inc, int *idx_eq)
{
  int i;
  *flg_inc = 0;
  *idx_eq = 0;

  for (i=0; i < numIDs; i++) {
    if (nodeID[i] == jj) {
      *flg_inc = 1;    // 節点が含まれるかどうか
      *idx_eq = i;     // 節点が含まれているindex
      break;
    }
  }
}


////////////////////////////////////////////////////////////////////////////////
//   2-dimensional fem ssor solver                                            //
//   Sparce Successive Over-Relaxation method                                 //
////////////////////////////////////////////////////////////////////////////////
//void fem_solver_ssor(double *A, double *x, double *b) {
void fem_solver_ssor_c (
double *A, double *x0, double *b,
int num_nodes, int *start_index,
double *x, double *tmp, int *numIDs, int **nodeID,
int *iterate, double *residual)
{
  int flg_inc = 0;
  int idx_eq = 0;
  int i, jj;
  int iNode, jNode, jnodeID;
  int flag;
  double before, after;
  int index0;
  double aj00, aj01, aj10, aj11;
  double a00, a01, a10, a11;
  double eps = 1e-8;
  double omega = 1.1;
  double temp = 0.0;
  for (i = 0; i < 2*num_nodes; i++) {
    x[i] = x0[i];
  }
  //while (*residual > eps) {
  while (1) {
    *iterate = *iterate + 1;
    // copy x
    for (i = 0; i < 2*num_nodes; i++) {
      tmp[i] = x[i];
    }
    for (i = 0; i < 2*num_nodes; i++) {
      iNode = i/2;
      flag = i%2;

      // calculate after value
      after = 0.0;
      index0 = start_index[iNode];
      for (jNode = 1; jNode < numIDs[iNode]; jNode++) {
        jnodeID = nodeID[iNode][jNode];
        aj00 = A[index0 + jNode*4 + 0];
        aj01 = A[index0 + jNode*4 + 1];
        aj10 = A[index0 + jNode*4 + 2];
        aj11 = A[index0 + jNode*4 + 3];

        if (flag == 0) {
          after += (aj00*x[jnodeID*2+0] + aj01*x[jnodeID*2+1]);
        } else if (flag == 1) {
          after += (aj10*x[jnodeID*2+0] + aj11*x[jnodeID*2+1]);
        }
      }

      //fprintf(stderr, "%f\n", after);

      // calculate before value
      before = 0.0;
      for (jj = 0; jj < iNode; jj++) {
        check_include (iNode, nodeID[jj], numIDs[jj],
                       &flg_inc, &idx_eq);
        if (flg_inc == 1) {
          index0 = start_index[jj];
          aj00 = A[index0 + idx_eq*4 + 0];
          aj01 = A[index0 + idx_eq*4 + 1];
          aj10 = A[index0 + idx_eq*4 + 2];
          aj11 = A[index0 + idx_eq*4 + 3];
          if (flag == 0) {
            before += (aj00*x[jj*2 + 0] + aj10*x[jj*2 + 1]);
          } else if (flag == 1) {
            before += (aj01*x[jj*2 + 0] + aj11*x[jj*2 + 1]);
          }
        }
      }

      // self calculation
      index0 = start_index[iNode];
      a00 = A[index0 + 0];
      a01 = A[index0 + 1];
      a10 = A[index0 + 2];
      a11 = A[index0 + 3];

      if (flag == 0) {
        after += a01*x[i+1];
        x[i] = (omega / a00)*(b[i] - before - after) + (1.0 - omega)*x[i];
      } else if (flag == 1) {
        before += a10*x[i-1];
        x[i] = (omega / a11)*(b[i] - before - after) + (1.0 - omega)*x[i];
      }
    }

    // calculate residual
    *residual = 0.0;
    temp = 0.0;
    for (i = 0; i < 2*num_nodes; i++) {
      temp = x[i] - tmp[i];
      *residual += sqrt(temp * temp);
    }
    if (*residual <= eps) break;

    if (*iterate%100 == 0) {
      fprintf (stderr, "\r     ite: %5d, residual: %.4e", *iterate, *residual);
    }
  }
  printf ("\r\033[K");
}

void test1d_int(int *A, int col) {
  int i;
  for (i = 0; i < col; i++) {
    A[i] = A[i] + i;
  }
}

void test2d_int(int **A, int row, int col, int *ite) {
  int i, j;
  for (i = 0; i < row; i++) {
    for (j = 0; j < col; j++) {
      A[i][j] = A[i][j] + 1;
      ite += 1;
      fprintf(stderr,"%d\n", *ite);
    }
  }
}

void test1d_double(double *A, int col, double n) {
  int i;
  for (i = 0; i < col; i++) {
    A[i] = A[i] + n;
  }
}

void test2d_double(double **A, int row, int col, double n) {
  int i, j;
  for (i = 0; i < row; i++) {
    for (j = 0; j < col; j++) {
      A[i][j] = A[i][j] + n;
    }
  }
}

