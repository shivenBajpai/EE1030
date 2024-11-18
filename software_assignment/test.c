#define _POSIX_C_SOURCE 199309L

#include "matlib.h"
#include "sapack.h"
#include <time.h>

// Function to test the QR decomposition
float test(int size) {
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);

    for (int i=1; i<5; i++) {
        Matrix* A = rand_matrix(size, size, 1);
        // printf("%d %d\n", i, size);
        double complex* u_eigenvalues = eig(A, 1e-6, 100000, 0, GRAM_SCHMIDT, 1);
        free(u_eigenvalues);
        free(A);
        // printf("Done one!\n");
    }
    clock_gettime(CLOCK_MONOTONIC, &end);
    return  (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / (5*1e9);
}

int main() {
    srand(1);
    printf("[");
    for (int size = 5; size<=120; size += 5 ) {
        printf("%.03f,", test(size));
        fflush(stdout);
    }
    printf("]\n");
}