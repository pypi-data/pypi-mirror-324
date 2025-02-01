#include <math.h>


void aidge_batchnorm2d_chw_float32 (float* inputs,
                                float* outputs,
                                float* input_mean,
                                float* input_var,
                                float* scale,
                                float* bias,
                                float epsilon,
                                const int nb_channels,
                                const int channel_width, const int channel_height)
{
    int featureMapSize = channel_width * channel_height;
    for (int ch = 0; ch < nb_channels; ++ch) 
    {
        int ioIndex = ch * featureMapSize;
        for (int i = ioIndex; i < ioIndex + featureMapSize; i++){
            outputs[i] = bias[ch];
        }
        float var =sqrt(input_var[ch] + epsilon);

        for (int feature = 0; feature<featureMapSize; ++feature) {
            outputs[ioIndex + feature] += scale[ch] * (inputs[ioIndex + feature]-input_mean[ch]) / var;
        }
    
    }
}