#ifndef MATLIB_H 
#define MATLIB_H 1
#include <math.h>
#include <complex.h>
#include <omp.h> 
#include "complex.h"
#include "string.h"
#include "stdlib.h"
#include "stdio.h"

#define E(m, i, j) (m)->data[(i)*((m)->c)+(j)]
#define norm(A, col) sqrt(self_dot_product(A, col, col))
#define copy_matrix(A) new_matrix(A->r, A->c, A->data) 
#define zeros_like(A) new_matrix(A->r, A->c, NULL)
#define shrink(A, rows, cols) A->r = rows; A->c = cols;

typedef struct Matrix {
    unsigned r;
    unsigned c;
    double complex data[];
} Matrix;

void print_matrix(Matrix* M);
void np_print_matrix(Matrix* M);
Matrix* new_matrix(unsigned n, unsigned m, double complex data[]);
Matrix* rand_matrix(unsigned n, unsigned m, double complex scale);
Matrix* eye(unsigned n, unsigned m);
double complex* diag(Matrix* M);
void gemm_into(Matrix* A, Matrix* B, Matrix* C);
Matrix* gemm(Matrix* A, Matrix* B);
Matrix* sub_gemm(Matrix* A, unsigned ar, unsigned ac, Matrix* B, unsigned br, unsigned bc);
double complex dot_product(Matrix* A, int cola, Matrix* B ,int colb);
double complex sub_col_dot(Matrix* A, int cola, int row);
double complex vec_mat_dot(Matrix* A, int col, double complex* v);
Matrix* vec_mat(double complex* v1, unsigned n1, double complex* v2, unsigned n2 );
double complex self_dot_product(Matrix* A, int col1, int col2);
Matrix* transpose(Matrix* A);

#endif