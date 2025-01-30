#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <omp.h>
#include <mpi.h>

void  set_diagonal
(int n, int *diagonal)
{
  int  i;
  for  (i = 0; i < n; i++)  diagonal[i] = i;
}

void  set_handling_rows
(int num_procs, int n, int *count_send, int *count_rows)
{
  int  i;
  int  count = 0;
  while (1) {
    for (i = 0; i < num_procs; i++) {
      count_send[i] = count_send[i] + 1;
      count_rows[i] = count_send[i];
      count++;
      if (count == n) break;
    }
    if (count == n) break;
  }
}

void  jacobi
(double *X, double *N_x, double **a, double *b,\
 int *diag, int Count, int N, int n, int Rank)
{
  // N : total number of elements in A
  int  i = 0, j = 0;
  double  sum1 = 0.0, sum2 = 0.0;

  while (i < Count) {
    for (j = 0; j < diag[i]; j++) {
      sum1 += a[i][j]*X[j];
    }
    for (j = (diag[i] + 1); j < n; j++) {
      sum2 += a[i][j]*X[j];
    }
    N_x[i] = (b[i] - sum1 - sum2) / a[i][diag[i]];
    i++;
    sum1 = 0.0;
    sum2 = 0.0;
  }
}



void  mpi_solver2
(MPI_Comm comm, char *method, int n,
 double *A, double *b, double *x)
{
  printf("Solver 2 \n");
  //MPI_Init ();

  int i = 0;
  for (i = 0; i < 5; i++){
    printf("A[%d] = %lf ", i, A[i]);
  }
  printf("\n");

  MPI_Barrier(MPI_COMM_WORLD);

}

void  mpi_solver
(MPI_Comm comm, char *method, int n,
 double *A, double *b, double *x)
{

  int  rank, num_procs;
  int  name_length = 10;
  char  name[name_length];
  double  *rec_A, *rec_b;
  int  *Diag;

  /* MPI initialization */
  /* mpi4pyから読み出す場合はMPI_Init は不要 */
  /* だが，MPI_Finalize は必要*/
  MPI_Comm_size (comm, &num_procs); // 全プロセス数の取得
  MPI_Comm_rank (comm, &rank);      // ランクの取得
  MPI_Get_processor_name (name, &name_length);
  if (rank == 0) printf("MPI solver! [method] %s\n", method);
  printf("Process %d/%d : %s\n", rank, num_procs, name);

  //int  *count_send = (int*)calloc (sizeof (int), num_procs);
  int  *count_send = (int*)malloc (num_procs*sizeof (int));
  int  *count_rows = (int*)malloc (num_procs*sizeof (int));
  int  *index_rows = (int*)malloc (num_procs*sizeof (int));
  int  *index_cols = (int*)malloc (num_procs*sizeof (int));
  int  count;


  double  *nx = (double*)malloc (n*sizeof (double));
  int  *diagonal = (int*)malloc (n*sizeof (int));

  int i, j, k=0;
  if (rank == 0) {
    // 送信データ数の初期化
    for (i = 0; i < num_procs; i++) {
        count_send[i] = 0;
        count_rows[i] = 0;
        index_rows[i] = 0;
        index_cols[i] = 0;
    }

    // 対角成分の列数の設定
    set_diagonal (n, diagonal);

    // 割り当て行数の設定
    set_handling_rows (num_procs, n, count_send, count_rows);

    // 各ランクへ送るデータ数の設定
    for (i = 1; i < num_procs;  i++) {
      index_cols[i] = index_cols[i-1] + count_send[i-1]*n;
      index_rows[i] = index_rows[i-1] + count_rows[i-1];
      count_send[i-1] = count_send[i-1]*n;
    }
    count_send[num_procs-1] = count_send[num_procs-1]*n;

    // 送信データ数の確認
    for (i = 0; i < num_procs; i++) {
      printf("count_send :%3d, count_rows :%3d, disp: %3d, rowdisp: %3d\n",\
             count_send[i], count_rows[i], index_cols[i], index_rows[i]);
    }
  }

  // MPI broad casting
  MPI_Bcast (count_send, num_procs, MPI_INT, 0, MPI_COMM_WORLD);
  MPI_Bcast (count_rows, num_procs, MPI_INT, 0, MPI_COMM_WORLD);
  MPI_Bcast (index_cols, num_procs, MPI_INT, 0, MPI_COMM_WORLD);
  MPI_Bcast (index_rows, num_procs, MPI_INT, 0, MPI_COMM_WORLD);
  MPI_Bcast (&n, 1, MPI_INT, 0, MPI_COMM_WORLD);

  // Init nx
  for (i = 0; i < n; i++) nx[i] = 0.0;

  MPI_Bcast (x, n, MPI_DOUBLE, 0, MPI_COMM_WORLD);

  rec_A = (double*)malloc (count_send[rank]*sizeof (double));
  rec_b = (double*)malloc (count_rows[rank]*sizeof (double));
  Diag = (int*)malloc (count_rows[rank]*sizeof (int));

  MPI_Scatterv (A, count_send, index_cols, MPI_DOUBLE,\
                rec_A, count_send[rank],   MPI_DOUBLE, 0, MPI_COMM_WORLD);
  MPI_Scatterv (b, count_rows, index_rows, MPI_DOUBLE,\
                rec_b, count_rows[rank],   MPI_DOUBLE, 0, MPI_COMM_WORLD);
  MPI_Scatterv (diagonal, count_rows, index_rows, MPI_INT,\
                Diag, count_rows[rank], MPI_INT, 0, MPI_COMM_WORLD);

  count = count_rows[rank];

  double *a[count];
  for (i = 0; i < count; i++) {
    a[i] = (double*)malloc (n*sizeof (double));
  }

  double *tmp;
  tmp = (double*)malloc (n*sizeof (double));
  for (i = 0; i < n; i++) {
    tmp[i] = 0.0;
  }

  k = 0;
  for (i = 0; i < count; i++) {
    for (j = 0; j < n; j++) {
      a[i][j] = rec_A[k];
      //printf("a[%d][%d] = %f, ", i,j,a[i][j]);
      k++;
    }
    //printf("\n");
  }
  
  int iter = 0;
  double  residual = 0.0;
  int converged = 0;
  double  eps = 1.0e-8;

  /* main loop */
  while (1) {
    jacobi (x, nx, a, rec_b, Diag, count_rows[rank], count_send[rank], n, rank);

    MPI_Allgatherv (nx, count_rows[rank], MPI_DOUBLE, tmp, count_rows,\
                    index_rows, MPI_DOUBLE, MPI_COMM_WORLD);
    if (rank == 0) {
      iter ++;
      for (i = 0; i < n; i++) {
        residual += (tmp[i] - x[i])*(tmp[i] - x[i]);
      }
      residual = sqrt (residual);
      //printf("Iter, residual : %d, %e\n", iter, residual);

      if (residual < eps) {
        converged = 1;
        printf("Iter, residual : %d, %e\n", iter, residual);
        //for (i = 0; i < n; i++) {
        //  printf("x[%d] = %11.8f\n", i, tmp[i]);
        //}
        free (diagonal);
      }
      residual = 0.0;
    }

    MPI_Bcast (&converged, 1, MPI_INT, 0, MPI_COMM_WORLD);
    if (converged == 1) break;
    for (i = 0; i < n; i++) {
      x[i] = tmp[i];
    }
  }

  free (tmp);
  free (*a);
  free (rec_b);
  free (rec_A);
  free (Diag);
  //free (diagonal);
  free (nx);
  free (index_cols);
  free (index_rows);
  free (count_rows);
  free (count_send);
  MPI_Finalize();
  exit (0);

}
