#include "sapack.h"

// Returns the QR decomposition of a matrix A using the Gram-Schmidt process
// Q is an orthogonal matrix, and R is an upper triangular matrix
void qr_decomposition_gs(Matrix* A, Matrix* Q, Matrix* R) {
    // *Q = copy_matrix(A);  // Initialize Q with the same size as A
    shrink(Q, A->r, A->c);
    shrink(R, A->r, A->c);
    memcpy(Q->data, A->data, sizeof(double complex) * A->r * A->c);
    // *R = zeros_like(A);  // Initialize R as a square matrix

    for (int j = 0; j < A->c; j++) {
        // Normalize Q_j and set R[j, j]
        double complex norm_qj = csqrt(self_dot_product(Q, j, j));
        E(R, j, j) = norm_qj;
        if (norm_qj != 0) {
            for (int i = 0; i < A->r; i++) {
                E(Q, i, j) /= norm_qj;
            }
        }

        // Orthogonalize later columns
        // #pragma omp parallel shared(A, R, Q) 
        {
            // #pragma omp for
            for (int k = j+1; k < A->r; k++) {

                E(R, j, k) = self_dot_product(Q, k, j);  // R[k, j] = Q_k^T * A_j

                for (int i = 0; i < A->r; i++) {
                    E(Q, i, k) -= E(R, j, k) * E(Q, i, j);  // Q_j -= R[k, j] * Q_k
                }
            }
        }

        for (int k = j+1; k<A->r; k++) {
            E(R, k, j) = 0;
        }
    }
}

void qr_decomposition_hh(Matrix* A, Matrix** Q_out, Matrix** R_out, double tol) {
    if (!A || (A->r != A->c)) {
        printf("Invalid matrix for QR decomposition\n");
        return;
    }

    unsigned m = A->r;
    Matrix *R = copy_matrix(A); // Start with R as a copy of A
    Matrix *Q = eye(m, m);
    Matrix *_Q = Q, *_R = R;

    for (unsigned i = 0; i < m-1; i++) {
        double complex norm_x = csqrt(sub_col_dot(R, i, i));
        if (cabs(norm_x) == 0) norm_x = 1;
        double complex alpha = norm_x*(creal(E(R, i, i)) >= 0?1:-1);
        E(R, i, i) -= alpha;
        // printf("\nPre R %d %lf%+lf:\n", i, creal(norm_x), cimag(norm_x));
        // print_matrix(R);
        double complex norm_u = sub_col_dot(R, i, i);
        if (cabs(norm_u) == 0) norm_u = 1;
        //  printf("\nPre R %d %lf%+lf:\n", i, creal(norm_u), cimag(norm_u));
        double complex v[m];
        for (int j=0; j<m; j++) v[j] =  E(R, j, i);
        E(R, i, i) += alpha;

        double complex dots[m];
        memset(dots, 0, m*sizeof(double complex));

        {
        for (int j=0; j<Q->c; j++) {
            for (int k=i; k<Q->r; k++) {
                dots[j] += (E(Q, k, j)) * v[k];
            }
        }}

        // if (A->r == 3) for (int j=0; j<m; j++) printf("%lf%+lf\n", creal(v[j]), cimag(v[j]));
        // if (A->r == 3) print_matrix(Q);
        // if (A->r == 3) print_matrix(R);
        // if (A->r == 3) for (int j=0; j<m; j++) printf("%lf%+lf\n", creal(dots[j]), cimag(dots[j]));

        // Q = gemm(H, Q);

        // #pragma omp parallel for shared(Q,v,dots,norm_u) num_threads(4)
        for (int j=0; j<Q->c; j++) {
            for(int k=i; k<Q->r; k++) {
                E(Q, k, j) -= 2*v[k]*dots[j]/norm_u;
            }
        }
        // print_matrix(Q);
        // print_matrix(R);

        memset(dots, 0, m*sizeof(double complex));
        for (int j=0; j<R->c; j++) {
            for (int k=i; k<R->r; k++) {
                dots[j] += (E(R, k, j)) * v[k];
            }
        }

        // if (A->r == 3) for (int j=0; j<m; j++) printf("%lf%+lf\n", creal(dots[j]), cimag(dots[j]));
        
        // #pragma omp parallel for shared(R,v,dots,norm_u) num_threads(4)
        for (int j=0; j<R->c; j++) {
            for(int k=i; k<R->r; k++) {
                E(R, k, j) -= 2*v[k]*dots[j]/norm_u;
            }
        }

        // print_matrix(Q);
        // print_matrix(R);
        // print_matrix(R_t);
        // free(R_t);

        // printf("\n\n");


        // Matrix* H = eye(m, m);

        // for (int j=i; j<m; j++) {
        //     for (int k=i; k<m; k++) {
        //         E(H, j, k) -= 2*v[j]*v[k]/norm_u;
        //     }
        // }
        // Matrix* R_t = gemm(H, R);

        // // printf("\nH:\n");
        // // print_matrix(H);
        // R = gemm(H, R);
        // free(_R);
        // _R = R;
        // Q = gemm(H, Q);
        // free(_Q);
        // _Q = Q;

        // printf("Iter %d:\n", i);
        // printf("\nRQ %d:\n", i);
        // print_matrix(R);
        // print_matrix(Q);
    }   
        // exit(0);
    
    *Q_out = transpose(Q); // Transpose Q to make it orthogonal
    *R_out = R; // R is already in upper triangular form
    free(Q);
}


// Solves 2x2 for eigenvalues inplace
void eig2x2(Matrix* M, unsigned i, unsigned j) {
    if (M->r < i+1 || M->c < j+1) return;
    
    #define _a E(M, i, j)
    #define _b E(M, i, j+1)
    #define _c E(M, (i+1), j)
    #define _d E(M, i+1, j+1)

    double complex t = (_a + _d)/2;
    double complex d = _a*_d - _b*_c;
    double complex temp = csqrt(t*t - d);

    _a = t + temp;
    _b = 0;
    _c = 0;
    _d = t - temp;

    #undef _a
    #undef _b
    #undef _c
    #undef _d
}

// Traverses Diagonal, solving any 2x2 blocks, leaving only eigenvalues on the diagonal
void solve2x2(Matrix* M, double tolerance) {
    size_t len = M->r>M->c?M->c:M->r;
    int prev_comp = 0;

    for (int i=len-1; i>0; i--) {
        // printf("%lf%+lfj\n",  creal(E(M, i, i)), cimag(E(M, i, i)));
        if (cabs(E(M, i, i-1)) > tolerance) {
            eig2x2(M, i-1, i-1);
            // print_matrix(M);
            // printf("Comp-Solving gave: %lf%+lfj\n", creal(E(M, i, i)), cimag(E(M, i, i)));
            prev_comp = 1;
        }
        else if (prev_comp) {
            prev_comp = 0;
            // printf("Follow-Real gave: %lf%+lfj\n", creal(E(M, i, i)), cimag(E(M, i, i)));
        } else {
            // printf("Direct Got: %lf%+lfj\n", creal(E(M, i, i)), cimag(E(M, i, i)));
        }
    }
}

// Solve for eigenvalues of matrix A
double complex* eig(Matrix* A, double tolerance, unsigned max_iter, int high_stable, Algorithm algo, int quiet) {
    Matrix *Q = zeros_like(A), *R = zeros_like(A), *Ak = copy_matrix(A), *An = zeros_like(A);
    double complex* eigenvalues = malloc(sizeof(double complex) * A->r);
    memset(eigenvalues, 0, sizeof(double complex) * A->r);
    unsigned iterations = 1;
    unsigned eigen_count = 0;
    int skip_swap = 0;

    while (1) {
        // Perform QR decomposition on A
        if (algo == GRAM_SCHMIDT) qr_decomposition_gs(Ak, Q, R);
        else {
            free(Q);
            free(R);
            // if (iterations >= 10368) print_matrix(Ak);
            qr_decomposition_hh(Ak, &Q, &R, tolerance);
            // if (iterations >= 10368) {print_matrix(Q);print_matrix(R);}
        }
        // printf("I: %d\n", iterations);
        // print_matrix(Q);
        // print_matrix(R);

        // Multiply R and Q to get the new A
        gemm_into(R, Q, An);

        // print_matrix(An);

        // Check for convergence (off-diagonal elements below tolerance)
        int converged = 1;

        for (int i = 0; i < An->r; i++) {
            for (int j = 0; j < i-1; j++) {
                if (cabs(E(An, i, j)) > tolerance) {
                    converged = 0;
                    break;
                }
            }
            if (!converged) break;
        }

        // printf("Rndm: %p %p\n", Ak, An);
        if (converged || iterations == max_iter) {
            // printf("Before I free\n: %p %p", Ak, An);
            // exit(0);
            free(Ak);
            free(Q);
            free(R);
            break;
        }

        // Every 8 iterations check for deflation opportunities
        if (!(iterations << (8*sizeof(unsigned))-3)) {
            // printf("%d: \n", iterations);
            // print_matrix(Ak);
            int deflations = 0, deflate[An->r];
            deflate[0] = 0;
            deflate[1] = 0;
            deflate[An->r-1] = 0;

            for (int i = An->r-2; i > 1; i--) {
                deflate[i] = 0;
                // printf("\n\n");
                // printf("Testing %d\n", i);

                if ((cabs(E(An, i+1, i)) < tolerance)) {
                    // printf("Passed a\n");
                    if ((cabs(E(An, i, i-1)) < tolerance)) {
                        // printf("Calling reg delf at %d %d %lf%+lf\n", i, i, creal(E(An, i, i)), cimag(E(An, i, i)));
                        // print_matrix(An);
                        // printf("\n");
                        deflate[i] = 1;
                        eigenvalues[eigen_count++] = E(An,i,i); 
                        deflations++;
                    } else {
                        if (high_stable) continue;
                        // printf("Passed b\n");
                        if ((cabs(E(An, i+1, i-1)) < tolerance) && (cabs(E(An, i-1, i-2)) < tolerance)) {
                            // printf("Passed c\n");
                            #define _a E(An, i-1, i-1)
                            #define _b E(An, i-1, i)
                            #define _c E(An, i, i-1)
                            #define _d E(An, i, i)

                            double trace = creal(_a + _d) / 2.0; // Real part of the eigenvalues
                            double det = creal(_a * _d - _b * _c); // Determinant of the block
                            double discriminant = trace * trace - det;

                            if (discriminant < 0) {
                                // Complex eigenvalues detected
                                // printf("Calling comp delf at %d %d\n", i, i);
                                // print_matrix(An);
                                eig2x2(An, i-1, i-1);
                                // printf("for %lf%+lf\n", creal(E(An, i, i)), cimag(E(An, i, i)));
                                deflate[i] = 1;
                                eigenvalues[eigen_count++] = E(An,i,i); 
                                deflations++;
                                // print_matrix(An);
                            }

                            #undef _a
                            #undef _b
                            #undef _c
                            #undef _d
                        }
                    }
                }
            }

            if (deflations) {
                // printf("%d Deflation on %d\n", deflations, iterations);
                // free(Ak);
                skip_swap = 1;
                shrink(Ak, Ak->r-deflations, Ak->c-deflations);
                // An = new_matrix(An->r-deflations, An->r-deflations, NULL);
                // printf("Shrink! %d %d\n")
                int a = 0,b = 0;

                for (int i = 0; i < An->r; i++) {
                    if (deflate[i]) continue;
                    b = 0;
                    for (int j = 0; j < An->c; j++) {
                        if (deflate[j]) continue;
                        // printf("%d: %d,%d <- %d,%d\n", An->r,a,b,i,j);
                        E(Ak, a, b) = E(An, i, j);
                        b++;
                    }

                    a++;
                }

                // print_matrix(An);
            }            
        }

        // Update A with AQ and continue iteration
        if (skip_swap) {
            skip_swap = 0;
        } else {
            Matrix* temp = Ak;
            Ak = An;
            An = temp;
        }
        // free(Q);
        // free(R);

        iterations++;
    }

    if (!quiet) printf("Converged in %d iterations %d defl\n\n", iterations, eigen_count);
    // print_matrix(An);
    solve2x2(An, tolerance);
    // print_matrix(An);
    double complex* rem_eigenvalues = diag(An);
    memcpy(&eigenvalues[eigen_count], rem_eigenvalues, (An->r)*sizeof(double complex));
    free(rem_eigenvalues); 
    free(An);

    return eigenvalues;
}