

void aidge_div_float32(float* input_a, 
                       float* input_b, 
                       float* output, 
                       unsigned int size)
{
    for (unsigned int i = 0; i < size; ++i) {
        output[i] = input_a[i] / input_b[i];
    }
}