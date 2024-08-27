// Loads a series of random points and also calculates the LHS and RHS or the equation in the question
int get_data(float *array) {
    array[0] = 1.0;  
    array[1] = 2;

    array[2] = 2;  
    array[3] = 4;  
    
    array[4] = 3;  
    array[5] = 6;
    
    array[6] = (array[3]-array[1])/(array[2]-array[0]);
    array[7] = (array[5]-array[3])/(array[4]-array[2]);

    return 0;
}
