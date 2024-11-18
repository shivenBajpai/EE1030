#include "matlib.h"

// Print a matrix to stdout
void print_matrix(Matrix* M) {
    if (!M) {
        printf("Invalid Matrix\n");
        return; 
    }

    putchar('[');
    for (int i=0; i<M->r; i++) {
        putchar('[');
        for (int j=0; j<M->c; j++) {
            printf("%lf%+lfj, ", creal(E(M, i, j)), cimag(E(M, i, j)));
        }
        putchar(']');
        putchar(',');
        putchar('\n');
    }
    putchar(']');
    putchar('\n');
}

// Prints a matrix in such a format that you can directly past ethe line into python
void np_print_matrix(Matrix* M) {
    if (!M) {
        printf("Invalid Matrix\n");
        return; 
    }

    printf("A = np.array([");
    for (int i=0; i<M->r; i++) {
        putchar('[');
        for (int j=0; j<M->c; j++) {
            printf("%lf%+lfj, ", creal(E(M, i, j)), cimag(E(M, i, j)));
        }
        putchar(']');
        putchar(',');
        // putchar('\n');
    }
    putchar(']');
    putchar(')');
    putchar('\n');
}

// Creates a struct for an n x m matrix
Matrix* new_matrix(unsigned n, unsigned m, double complex data[]) {
    Matrix* mat = malloc(sizeof(Matrix) + n*m*sizeof(double complex)); 
    // Matrix* mat = aligned_alloc(32, sizeof(Matrix) + n*m*sizeof(double complex)); 
    if (!mat) return NULL;

    mat->r = n;
    mat->c = m;
    if (data) memcpy(mat->data, data, n*m*sizeof(double complex));
    else memset(mat->data, 0, n*m*sizeof(double complex));

    return mat;
}

// Create a matrix with random entries
Matrix* rand_matrix(unsigned n, unsigned m, double complex scale) {
    Matrix* mat = new_matrix(n, m, NULL);
    if (!mat) return NULL;

    if (rand() > (double) RAND_MAX/1.33) { // 1 in 4 chance of getting a real matrix
    // if (1) {
        for (int i=0; i<n*m; i++) {
            mat->data[i] = (((double complex) rand()/RAND_MAX)-0.5) * scale;
        }
    } else {
        for (int i=0; i<n*m; i++) {
            mat->data[i] = (((double complex) rand()/RAND_MAX)-0.5 + (((double complex) rand()/RAND_MAX)-0.5) * I) * scale;
        }
    }

    return mat;
}

// Return a matrix of specified dimensions with diagonal elements set to 1
Matrix* eye(unsigned n, unsigned m) {
    Matrix* mat = new_matrix(n, m, NULL);
    if (!mat) return NULL;

    unsigned min_dim = m>n?n:m;
    for (int i=0; i<min_dim; i++) E(mat, i, i) = 1;

    return mat;
}

// Gets the diagonal entries of square matrix M and returns an array of size minimum dimension of matrix
double complex* diag(Matrix* M) {
    size_t len = M->r>M->c?M->c:M->r;
    double complex* diagonal = malloc(len*sizeof(double complex));
    if (!diagonal) return NULL;

    for (int i=0; i<len; i++) {
        diagonal[i] = E(M, i, i);
    }

    return diagonal;
}

// Returns matrix multiplication AB, writes into pointer C
void gemm_into(Matrix* A, Matrix* B, Matrix* C) {
    if (A->c != B->r) {
        printf("Err: Cannot multiply matrices of shape %ux%u and %ux%u\n", A->r, A->c, B->r, B->c);
        exit(0);
    }

    shrink(C, A->r, B->c);

    {
    #pragma omp parallel for collapse(2) shared(A,B,C) num_threads(6) schedule(dynamic, A->r)
    for (int i=0; i<A->r; i++) {
        for (int j=0; j<B->c; j++) {
            double complex sum = 0.0;
            for (int k=0; k<A->c; k++) {
                sum += E(A, i, k) * E(B, k, j);
            }
            E(C, i, j) = sum;
        }
    }
    }
}

// Returns matrix multiplication AB
Matrix* gemm(Matrix* A, Matrix* B) {
    if (A->c != B->r) {
        printf("Err: Cannot multiply matrices of shape %ux%u and %ux%u", A->r, A->c, B->r, B->c);
        return NULL;
    }

    Matrix* C = new_matrix(A->r, B->c, NULL);

    {
    #pragma omp parallel for collapse(2) shared(A,B,C) num_threads(6) schedule(dynamic, A->r)
    for (int i=0; i<A->r; i++) {
        for (int j=0; j<B->c; j++) {
            double complex sum = 0.0;
            for (int k=0; k<A->c; k++) {
                sum += E(A, i, k) * E(B, k, j);
            }
            E(C, i, j) = sum;
        }
    }
    }

    return C;
}

// Returns matrix multiplication AB, But only multiplies a subpart of the matrices
Matrix* sub_gemm(Matrix* A, unsigned ar, unsigned ac, Matrix* B, unsigned br, unsigned bc) {
    if (A->c-ac != B->r-br) {
        printf("Err: Cannot multiply matrices of shape %ux%u and %ux%u", A->r, A->c, B->r, B->c);
        return NULL;
    }

    Matrix* C = new_matrix(A->r-ar, B->c-bc, NULL);

    // #pragma omp parallel shared(A,B,C)
    {
    // #pragma omp for collapse(2)
    for (int i=0; i<A->r-ar; i++) {
        for (int j=0; j<B->c-bc; j++) {

            double complex sum = 0.0;
            for (int k=0; k<A->c-ac; k++) {
                printf("Acc: %u %u %u %u\n", i, j, k, br);
                sum += E(A, ar+i, ac+k) * E(B, br+k, bc+j);
            }
            E(C, i, j) = sum;
        
        }
    }
    }

    return C;
}

// Inner product between different columns of a matrix
double complex dot_product(Matrix* A, int cola, Matrix* B ,int colb) {
    double complex dot = 0;
    for (int i = 0; i < A->r; i++) {
        dot += E(A, i, cola) * E(B, i, colb);
    }
    return dot;
}

// Norm of a part of a column
double complex sub_col_dot(Matrix* A, int cola, int row) {
    double complex dot = 0;
    for (int i = row; i < A->r; i++) {
        dot += E(A, i, cola) * E(A, i, cola);
        // printf("Dot: %lf%+lf\n", creal(dot), cimag(dot));
    }
    return dot;
}

// Inner product between a vector and a column
double complex vec_mat_dot(Matrix* A, int col, double complex* v) {
    double complex sum = 0;

    for (int i=0; i<A->r; i++) {
        sum += E(A, col, i) * v[i];
    }

    return sum;
}

// Outer product
Matrix* vec_mat(double complex* v1, unsigned n1, double complex* v2, unsigned n2 ) {
    Matrix* mat = new_matrix(n1, n2, NULL);
    if (!mat) return NULL;

    for (int i=0; i<n1; i++) {
        for (int j=0; j<n2; j++) {
            E(mat, i, j) = v1[i] * v2[j];
        }
    }

    return mat;
}

// Function to calculate the dot product of two column vectors in a matrix
double complex self_dot_product(Matrix* A, int col1, int col2) {
   return dot_product(A, col1, A, col2);
} 

// Returns transpose of a matrix
Matrix* transpose(Matrix* A) {
    Matrix* At = new_matrix(A->c, A->r, NULL);
    for (int i = 0; i < A->r; i++) {
        for (int j = 0; j < A->c; j++) {
            E(At, j, i) = E(A, i, j);
        }
    }
    return At;
}