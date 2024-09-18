#include <math.h>
#include <stdlib.h>

// Struct to represent 2 dimensional vectors
typedef struct {
    double x;
    double y;
} Vector;

// Calculate vertcies given the lengths of a triangle
Vector* calculateVertices(double a, double b, double c) {
	Vector* vertices = malloc(sizeof(Vector) * 3);

	double cos_A = (pow(b,2) + pow(c,2) - pow(a,2)) / (2*b*c);
	double sin_A = sqrt(1 - pow(cos_A, 2));

	vertices[0].x = 0;
	vertices[0].y = 0;
	vertices[1].x = c*cos_A;
	vertices[1].y = c*sin_A;
	vertices[2].x = b;
	vertices[2].y = 0;

	return vertices;
}
