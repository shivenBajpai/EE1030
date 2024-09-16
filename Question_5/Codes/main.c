#include <math.h>
#include <stdlib.h>

#define PI 3.14159

// Struct to represent 3 dimensional vectors
typedef struct {
    double x;
    double y;
    double z;
} Vector;

// Calculate the cosines, given 2 angles
Vector* calculate_cosines(double alpha, double beta) {
    
    // Convert to radians
    alpha = alpha*PI/180;
    beta = beta*PI/180;

    // Calculate cosines
    double cos_alpha = cos(alpha);
    double cos_beta = cos(beta);
    double cos_gamma = sqrt(1 - pow(cos_alpha,2) - pow(cos_beta,2));
    
    // Create and populate struct
    Vector* vector = malloc(sizeof(Vector));
    vector->x = cos_alpha;
    vector->y = cos_gamma;
    vector->z = cos_beta;

    return vector;
}
