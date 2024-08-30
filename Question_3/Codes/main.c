typedef struct {
    float x, y;
} point;

// Loads a series of random points and also calculates the LHS and RHS or the equation in the question
int get_data(point *points, float *lhs, float *rhs) {
    (points[0]) = (point) {.x=1., .y=2.};
    (points[1]) = (point) {.x=2., .y=4.};
    (points[2]) = (point) {.x=3., .y=6.};

    *lhs = (float) (points[1].y - points[0].y)/(points[1].x - points[0].x);
    *rhs = (float) (points[2].y - points[1].y)/(points[2].x - points[1].x);

    return 0;
}
