
void aidge_reshape_chw_float32(float* inputs,
                           float* outputs,
                           unsigned int size)
{
    for (int i = 0; i < size; i++){
        outputs[i] = inputs[i];
    }
}