#ifndef SAPACK_H
#define SAPACK_H 1
#include <math.h>
#include <complex.h>
#include <omp.h> 
#include "string.h"
#include "stdlib.h"
#include "matlib.h"

typedef enum Algorithm {
    GRAM_SCHMIDT,
    HOUSEHOLDER
} Algorithm;

void qr_decomposition_gs(Matrix* A, Matrix* Q, Matrix* R);
void qr_decomposition_hh(Matrix* A, Matrix** Q_out, Matrix** R_out, double tol);
void eig2x2(Matrix* M, unsigned i, unsigned j);
void solve2x2(Matrix* M, double tolerance);
double complex* eig(Matrix* A, double tolerance, unsigned max_iter, int high_stable, Algorithm algo, int quiet);

#endif