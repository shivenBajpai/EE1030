#include <math.h>
#include <stdlib.h>
#include <time.h>

typedef struct {
    float x;
    float y;
    float z;
    float norm;
} Vector;

void generate_random_vectors(Vector* vectors, size_t n, unsigned int seed) {
    
    srand(seed);
    float x,y,z,norm;

    for (size_t i = 0; i < n; i++) {
        x = (((float)rand()*2 / RAND_MAX)-1);
        y = (((float)rand()*2 / RAND_MAX)-1);
        z = (((float)rand()*2 / RAND_MAX)-1);
        norm = sqrtf(x*x + y*y + z*z);
        
        vectors[i].x = (x / norm) * 4;
        vectors[i].y = (y / norm) * 4;
        vectors[i].z = (z / norm) * 4;
        vectors[i].norm = 4;
    }
}

void scale_vectors(Vector* in_vectors, Vector* out_vectors, size_t n) {

    float lambda;
    
    for (size_t i = 0; i < n; i++) {
        lambda = ((float)rand()*5/RAND_MAX)-3;

        out_vectors[i].x = in_vectors[i].x * lambda;
        out_vectors[i].y = in_vectors[i].y * lambda;
        out_vectors[i].z = in_vectors[i].z * lambda;
        out_vectors[i].norm = sqrtf(pow(out_vectors[i].x, 2) + pow(out_vectors[i].y, 2) + pow(out_vectors[i].z, 2));
    }
}

Vector** get_data(int n) {
    Vector* vectors = malloc(n*sizeof(Vector));
    Vector* scaled_vectors = malloc(n*sizeof(Vector));

    generate_random_vectors(vectors, n, time(NULL));

    scale_vectors(vectors, scaled_vectors, n);

    return (Vector*[2]){vectors, scaled_vectors};
}

