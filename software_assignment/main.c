#include <time.h>
#include <complex.h>
#include <omp.h>
#include "matlib.h"
#include "sapack.h"

int comp (const void* a, const void* b) {
    double f = cabs(*(double complex*) a);
    double s = cabs(*(double complex*) b);

    if (f > s) return  1;
    if (f < s) return -1;
    return 0;
}

int main() {
    srand(12);

    // Matrix* A = new_matrix(3, 3, (double complex[9]) {1, 0, 0, 2, 0, 0, 3, 0, 0}); 
    // Matrix* B = new_matrix(3, 3, (double complex[9]) {1, 2, 3, 0, 0, 0, 0, 0, 0}); 
    // Matrix* C = new_matrix(4, 4, NULL);

    Matrix* A = rand_matrix(100, 100, 1);
    // Matrix* B = rand_matrix(100, 100, 1);
    // for (int i=0; i<1000; i++) {
    //     Matrix* C = gemm(A,B);
    //     free(C);
    // }
    // gemm_into(A, B, C);
    // print_matrix(gemm(A,B));
    // np_print_matrix(A);

    // Matrix *Q, *R;
    // qr_decomposition_hh_mk3(A, &Q, &R);
    // print_matrix(Q);
    // print_matrix(R);

    // double complex* u_eigenvalues = eig(A, 1e-6, 100000, 0, HOUSEHOLDER, 0);
    double complex* s_eigenvalues = eig(A, 1e-12, 100000, 0, GRAM_SCHMIDT, 0);
    // qsort(u_eigenvalues, A->r, sizeof(double complex), comp);
    qsort(s_eigenvalues, A->r, sizeof(double complex), comp);
    for (int i=0; i<A->r; i++) printf("%lf%+lfj\n", creal(s_eigenvalues[i]), cimag(s_eigenvalues[i]));
    // for (int i=0; i<A->r; i++) printf("u: %lf%+lfj\ns: %lf%+lfj\n\n", creal(u_eigenvalues[i]), cimag(u_eigenvalues[i]), creal(s_eigenvalues[i]), cimag(s_eigenvalues[i]));
    // free(u_eigenvalues);
    free(s_eigenvalues);

    free(A);
    // free(B);
}