#include <math.h>
#include <stdlib.h>
#include <assert.h>

#define PI 3.14159

// Struct to represent 3 dimensional vectors
typedef struct {
    float x;
    float y;
    float z;
    float norm;
} Vector;

// Create teh desired vector
Vector* get_vector() {
    Vector* vector = malloc(sizeof(Vector));
    vector->x = cos(60 * PI / 180);
    vector->y = cos(45 * PI / 180);
    vector->z = cos(45 * PI / 180);
    vector->norm = sqrt(pow(vector->x, 2) + pow(vector->y, 2) + pow(vector->z, 2));
    return vector;
}
