// alt.c

#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include "matfun.h"
#include "geofun.h"

// Calculate vertices given the lengths of a triangle, returns array of matrices [A, B1, B2, C]
double*** calculateVertices(double a, double b, double c) {
	
	if (fmax(a,fmax(b,c)) >= (a+b+c)/2) {
		printf("Lengths given cannot form a valid triangle!");
		return NULL;
	}

	double** A = createMat(2, 1);
	double** C = createMat(2, 1);
	C[0][0] = b;
	
	double** n = Matsub(C, A, 2, 1);
	double d = (pow(b, 2) + pow(c, 2) - pow(a, 2))/2;
	
	double** m = createMat(2, 1);
	m[0][0] = -1 * n[1][0];
	m[1][0] = n[0][0];

	double** h = Matscale(n, 2, 1, d/pow(Matnorm(n, 2),2));
	double** temp = Matscale(m, 2, 1, sqrt(pow(c, 2) - pow(Matnorm(h,2), 2))/Matnorm(m, 2)); 

	double** B1 = Matadd(h, temp, 2, 1);
	double** B2 = Matsub(h, temp, 2, 1);

	freeMat(n, 2);
	freeMat(m, 2);
	freeMat(h, 2);
	freeMat(temp, 2);
	
	double*** returnValues = malloc(sizeof(double**)*2*1*4);
	returnValues[0] = A;
	returnValues[1] = B1;
	returnValues[2] = B2;
	returnValues[3] = C;
	
	return returnValues;
}
