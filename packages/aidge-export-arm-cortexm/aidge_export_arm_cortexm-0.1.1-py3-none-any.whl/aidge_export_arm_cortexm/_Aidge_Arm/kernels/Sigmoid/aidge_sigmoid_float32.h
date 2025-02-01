#include <math.h>


void aidge_sigmoid_float32 (float* inputs, 
                            float* outputs,
                            unsigned int size)
{
    for (unsigned int i = 0; i < size; ++i) {
        outputs[i] = 1 / ( 1 + exp(-inputs[i]) );
    }
}