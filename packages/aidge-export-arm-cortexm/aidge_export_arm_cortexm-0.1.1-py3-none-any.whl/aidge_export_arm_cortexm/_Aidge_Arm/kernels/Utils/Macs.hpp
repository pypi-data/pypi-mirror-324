// /*
//     (C) Copyright 2017 CEA LIST. All Rights Reserved.
//     Contributor(s): N2D2 Team

//     This software is governed by the CeCILL-C license under French law and
//     abiding by the rules of distribution of free software.  You can  use,
//     modify and/ or redistribute the software under the terms of the CeCILL-C
//     license as circulated by CEA, CNRS and INRIA at the following URL
//     "http://www.cecill.info".

//     As a counterpart to the access to the source code and  rights to copy,
//     modify and redistribute granted by the license, users are provided only
//     with a limited warranty  and the software's author,  the holder of the
//     economic rights,  and the successive licensors  have only  limited
//     liability.

//     The fact that you are presently reading this means that you have had
//     knowledge of the CeCILL-C license and that you accept its terms.
// */

// #ifndef __N2D2_EXPORT_CPP_MACS_HPP__
// #define __N2D2_EXPORT_CPP_MACS_HPP__

// #include <cstdint>
// #include <limits>
// #include <type_traits>
// #include <cmsis_compiler.h>

// #include "swar_arm_acle.h"

// namespace N2D2_Export {


// template<typename Input_T>
// inline static
// uint32_t XTB16(uint32_t val) 
// {
//     return std::is_unsigned<Input_T>::value ? __UXTB16(val) : __SXTB16(val);
// }

// template<int INPUTS_INC = 1,
//          int WEIGHTS_INC = 1,
//          typename Input_T,
//          typename Weight_T,
//          typename Sum_T>
// inline static
// Sum_T dualMac(const Input_T* __restrict inputs, 
//               const Weight_T* __restrict weights, 
//               Sum_T weightedSum) 
// {
//     weightedSum += inputs[0] * weights[0]
//         + inputs[INPUTS_INC] * weights[WEIGHTS_INC];

//     return weightedSum;
// }

// template<int INPUTS_INC = 1,
//          int WEIGHTS_INC = 1,
//          typename Input_T,
//          typename Weight_T,
//          typename Sum_T,
//          typename std::enable_if<std::is_floating_point<Input_T>::value>::type* = nullptr>
// inline static
// Sum_T quadMac(const Input_T* __restrict inputs, 
//               const Weight_T* __restrict weights, 
//               Sum_T weightedSum) 
// {
//     weightedSum += inputs[0*INPUTS_INC] * weights[0*WEIGHTS_INC]
//         + inputs[1*INPUTS_INC] * weights[1*WEIGHTS_INC]
//         + inputs[2*INPUTS_INC] * weights[2*WEIGHTS_INC]
//         + inputs[3*INPUTS_INC] * weights[3*WEIGHTS_INC];

//     return weightedSum;
// }

// template<int INPUTS_INC = 1,
//          int WEIGHTS_INC = 1,
//          typename Input_T,
//          typename Weight_T,
//          typename Sum_T,
//          typename std::enable_if<!std::is_floating_point<Input_T>::value>::type* = nullptr>
// inline static
// Sum_T quadMac(const Input_T* __restrict inputs, 
//               const Weight_T* __restrict weights, 
//               Sum_T weightedSum) 
// {
//     if(INPUTS_INC != 1 || WEIGHTS_INC != 1) {
//         weightedSum += inputs[0*INPUTS_INC] * weights[0*WEIGHTS_INC]
//             + inputs[1*INPUTS_INC] * weights[1*WEIGHTS_INC]
//             + inputs[2*INPUTS_INC] * weights[2*WEIGHTS_INC]
//             + inputs[3*INPUTS_INC] * weights[3*WEIGHTS_INC];

//         return weightedSum;
//     }

//     // Inputs loading & preparation
//     uint32_t in;
//     memcpy((void*) &in, inputs, sizeof(in));
    
//     uint32_t in1 = XTB16<Input_T>(in);
//     uint32_t in2 = XTB16<Input_T>(in >> 8);
    
//     // Weights loading & preparation
//     uint32_t wt;
//     memcpy((void*) &wt, weights, sizeof(wt));
    
//     uint32_t wt1 = XTB16<Weight_T>(wt);
//     uint32_t wt2 = XTB16<Weight_T>(wt >> 8);

//     // Computation
//     if(std::is_same<Sum_T, int32_t>::value) {
//         weightedSum = __SMLAD(in1, wt1, weightedSum);
//         weightedSum = __SMLAD(in2, wt2, weightedSum);
//     }
//     else {
//         weightedSum = __SMLALD(in1, wt1, weightedSum);
//         weightedSum = __SMLALD(in2, wt2, weightedSum);
        
//     }
    
//     return weightedSum;
// }




// // ----------------------------------------------------------------------------
// // -------------- MAC computing functions for kernel 4W-4A --------------------
// // ----------------------------------------------------------------------------

// /**
//  * @brief   Unsigned mono mac operation (4W/4A version)
//  * @details Performs one mac operation for signed 4-bits weights
//  *          and unsigned 4-bits inputs.
//  * 
//  * @tparam  Input_T     Input type (should be udata<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to input vector
//  * @param[in]      weights         Pointer to kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the dual mac operation
//  */
// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T monoMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     weightedSum += __UBFX(inputs[0], 4, 4) * __SBFX(weights[0], 4, 4);
//     return weightedSum;
// }

// /**
//  * @brief   Signed mono mac operation (4W/4A version)
//  * @details Performs one mac operation for signed 4-bits weights
//  *          and signed 4-bits inputs.
//  * 
//  * @tparam  Input_T     Input type (should be data<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to input vector
//  * @param[in]      weights         Pointer to kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the dual mac operation
//  */
// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(!std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T monoMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     weightedSum += __SBFX(inputs[0], 4, 4) * __SBFX(weights[0], 4, 4);
//     return weightedSum;
// }

// /**
//  * @brief   Unsigned dual mac operation (4W/4A version)
//  * @details Performs two mac operations for signed 4-bits weights
//  *          and unsigned 4-bits inputs. Extracts the two 4-bits weights
//  *          from a stored 8-bits weight and associates them into 
//  *          a 32-bits value. Then extracts the two 4-bits inputs
//  *          from a stored 8-bits input and associates them into 
//  *          a 32-bits value. Finally performs a dual mac operation 
//  *          with the __SMLAD instruction
//  * 
//  * @tparam  Input_T     Input type (should be udata<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to compressed input vector
//  * @param[in]      weights         Pointer to compressed kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the dual mac operation
//  */
// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T dualMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     uint8_t wt;
//     std::memcpy((void*) &wt, weights, sizeof(wt));

//     int32_t w0 = __SBFX(wt, 0, 4);
//     int32_t w1 = __SBFX(wt, 4, 4);
//     uint32_t wght = __BFI(w1, w0, 16, 16);

//     uint8_t in;
//     std::memcpy((void*) &in, inputs, sizeof(in));

//     int32_t a0 = __UBFX(in, 0, 4);
//     int32_t a1 = __UBFX(in, 4, 4);
//     uint32_t act = __BFI(a1, a0, 16, 16);

//     weightedSum = __SMLAD(act, wght, weightedSum);

//     return weightedSum;
// }

// /**
//  * @brief   Signed dual mac operation (4W/4A version)
//  * @details Performs two mac operations for signed 4-bits weights
//  *          and signed 4-bits inputs. Extracts the two 4-bits weights
//  *          from a stored 8-bits weight and associates them into 
//  *          a 32-bits value. Then extracts the two 4-bits inputs
//  *          from a stored 8-bits input and associates them into 
//  *          a 32-bits value. Finally performs a dual mac operation 
//  *          with the __SMLAD instruction
//  * 
//  * @tparam  Input_T     Input type (should be data<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to compressed input vector
//  * @param[in]      weights         Pointer to compressed kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the dual mac operation
//  */
// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(!std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T dualMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     uint8_t wt;
//     std::memcpy((void*) &wt, weights, sizeof(wt));

//     int32_t w0 = __SBFX(wt, 0, 4);
//     int32_t w1 = __SBFX(wt, 4, 4);
//     uint32_t wght = __BFI(w1, w0, 16, 16);

//     uint8_t in;
//     std::memcpy((void*) &in, inputs, sizeof(in));

//     int32_t a0 = __SBFX(in, 0, 4);
//     int32_t a1 = __SBFX(in, 4, 4);
//     uint32_t act = __BFI(a1, a0, 16, 16);

//     weightedSum = __SMLAD(act, wght, weightedSum);

//     return weightedSum;
// }

// /**
//  * @brief   Unsigned quad mac operation (4W/4A version)
//  * @details Performs four mac operations for signed 4-bits weights
//  *          and unsigned 4-bits inputs. Extracts the four 4-bits weights
//  *          from two stored 8-bits weights and associates them into 
//  *          two 32-bits values. Then extracts the four 4-bits inputs
//  *          from two stored 8-bits inputs and associates them into 
//  *          two 32-bits values. Finally performs a double dual mac operation 
//  *          with the __SMLAD instruction
//  * 
//  * @tparam  Input_T     Input type (should be udata<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to compressed input vector
//  * @param[in]      weights         Pointer to compressed kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the quad mac operation
//  */
// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T quadMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     uint16_t wt;
//     std::memcpy((void*) &wt, weights, sizeof(wt));

//     int32_t w0 = __SBFX(wt, 0, 4);
//     int32_t w1 = __SBFX(wt, 4, 4);
//     int32_t w2 = __SBFX(wt, 8, 4);
//     int32_t w3 = __SBFX(wt, 12, 4);

//     uint32_t evenW1 = __BFI(w2, w0, 16, 16);
//     uint32_t oddW1  = __BFI(w3, w1, 16, 16);

//     uint16_t in;
//     std::memcpy((void*) &in, inputs, sizeof(in));

//     int32_t a0 = __UBFX(in, 0, 4);
//     int32_t a1 = __UBFX(in, 4, 4);
//     int32_t a2 = __UBFX(in, 8, 4);
//     int32_t a3 = __UBFX(in, 12, 4);

//     uint32_t evenA1 = __BFI(a2, a0, 16, 16);
//     uint32_t oddA1  = __BFI(a3, a1, 16, 16);

//     weightedSum = __SMLAD(evenA1, evenW1, weightedSum);
//     weightedSum = __SMLAD(oddA1, oddW1, weightedSum);

//     return weightedSum;
// }

// /**
//  * @brief   Signed quad mac operation (4W/4A version)
//  * @details Performs four mac operations for signed 4-bits weights
//  *          and signed 4-bits inputs. Extracts the four 4-bits weights
//  *          from two stored 8-bits weights and associates them into 
//  *          two 32-bits values. Then extracts the four 4-bits inputs
//  *          from two stored 8-bits inputs and associates them into 
//  *          two 32-bits values. Finally performs a double dual mac operation 
//  *          with the __SMLAD instruction
//  * 
//  * @tparam  Input_T     Input type (should be data<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to compressed input vector
//  * @param[in]      weights         Pointer to compressed kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the quad mac operation
//  */
// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(!std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T quadMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     uint16_t wt;
//     std::memcpy((void*) &wt, weights, sizeof(wt));

//     int32_t w0 = __SBFX(wt, 0, 4);
//     int32_t w1 = __SBFX(wt, 4, 4);
//     int32_t w2 = __SBFX(wt, 8, 4);
//     int32_t w3 = __SBFX(wt, 12, 4);

//     uint32_t evenW1 = __PKHBT(w2, w0, 16);
//     uint32_t oddW1  = __PKHBT(w3, w1, 16);

//     uint16_t in;
//     std::memcpy((void*) &in, inputs, sizeof(in));

//     int32_t a0 = __SBFX(in, 0, 4);
//     int32_t a1 = __SBFX(in, 4, 4);
//     int32_t a2 = __SBFX(in, 8, 4);
//     int32_t a3 = __SBFX(in, 12, 4);
    
//     uint32_t evenA1 = __PKHBT(a2, a0, 16);
//     uint32_t oddA1  = __PKHBT(a3, a1, 16);

//     weightedSum = __SMLAD(evenA1, evenW1, weightedSum);
//     weightedSum = __SMLAD(oddA1, oddW1, weightedSum);

//     return weightedSum;
// }

// /**
//  * @brief   Unsigned octo mac operation (4W/4A version)
//  * @details Performs eight mac operations for signed 4-bits weights
//  *          and unsigned 4-bits inputs. Extracts the eight 4-bits weights
//  *          from four stored 8-bits weights and associates them into 
//  *          four 32-bits values. Then extracts the eight 4-bits inputs
//  *          from four stored 8-bits inputs and associates them into 
//  *          four 32-bits values. Finally performs a quadruple dual mac operation 
//  *          with the __SMLAD instruction
//  * 
//  * @tparam  Input_T     Input type (should be udata<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to compressed input vector
//  * @param[in]      weights         Pointer to compressed kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the octo mac operation
//  */
// // template<typename Input_T, typename Weight_T,
// //          typename std::enable_if<(std::is_unsigned<Input_T>::value
// //          && std::numeric_limits<Weight_T>::digits == 4
// //          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// // __attribute__((always_inline)) static inline
// // Sum_T octoMac(const Input_T* __restrict inputs,
// //               const Weight_T* __restrict weights,
// //               Sum_T weightedSum)
// // {
// //     uint32_t wt;
// //     std::memcpy((void*) &wt, weights, sizeof(wt));

// //     int32_t w0 = __SBFX(wt, 0, 4);
// //     int32_t w1 = __SBFX(wt, 4, 4);
// //     int32_t w2 = __SBFX(wt, 8, 4);
// //     int32_t w3 = __SBFX(wt, 12, 4);
// //     int32_t w4 = __SBFX(wt, 16, 4);
// //     int32_t w5 = __SBFX(wt, 20, 4);
// //     int32_t w6 = __SBFX(wt, 24, 4);
// //     int32_t w7 = __SBFX(wt, 28, 4);

// //     // uint32_t weight0 = __BFI(w4, w0, 16, 16);
// //     // uint32_t weight1 = __BFI(w5, w1, 16, 16);
// //     // uint32_t weight2 = __BFI(w6, w2, 16, 16);
// //     // uint32_t weight3 = __BFI(w7, w3, 16, 16);

// //     uint32_t weight0 = __PKHBT(w0, w4, 16);
// //     uint32_t weight1 = __PKHBT(w1, w5, 16);
// //     uint32_t weight2 = __PKHBT(w2, w6, 16);
// //     uint32_t weight3 = __PKHBT(w3, w7, 16);

// //     uint32_t in;
// //     std::memcpy((void*) &in, inputs, sizeof(in));

// //     uint32_t act0 = in & 0xF000F;
// //     uint32_t act1 = (in >> 4) & 0xF000F;
// //     uint32_t act2 = (in >> 8) & 0xF000F;
// //     uint32_t act3 = (in >> 12) & 0xF000F;

// //     weightedSum = __SMLAD(act0, weight0, weightedSum);
// //     weightedSum = __SMLAD(act1, weight1, weightedSum);
// //     weightedSum = __SMLAD(act2, weight2, weightedSum);
// //     weightedSum = __SMLAD(act3, weight3, weightedSum);

// //     return weightedSum;
// // }

// // template<typename Input_T, typename Weight_T,
// //          typename std::enable_if<(std::is_unsigned<Input_T>::value
// //          && std::numeric_limits<Weight_T>::digits == 4
// //          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// // __attribute__((always_inline)) static inline
// // Sum_T octoMac(const Input_T* __restrict inputs,
// //               const Weight_T* __restrict weights,
// //               Sum_T weightedSum)
// // {
// //     union n2d2_dataword wt;
// //     std::memcpy((void*) &wt, weights, sizeof(wt));

// //     union n2d2_udataword in;
// //     std::memcpy((void*) &in, inputs, sizeof(in));

// //     for (int i = 0; i < 4; ++i) {
// //         weightedSum += (data<32>)(in.half_bytes[i].fields.op0) * wt.half_bytes[i].fields.op0;
// //         weightedSum += (data<32>)(in.half_bytes[i].fields.op1) * wt.half_bytes[i].fields.op1;
// //     }

// //     // weightedSum += (data<32>)(in.half_bytes[0].fields.op0) * wt.half_bytes[0].fields.op0;
// //     // weightedSum += (data<32>)(in.half_bytes[0].fields.op1) * wt.half_bytes[0].fields.op1;
// //     // weightedSum += (data<32>)(in.half_bytes[1].fields.op0) * wt.half_bytes[1].fields.op0;
// //     // weightedSum += (data<32>)(in.half_bytes[1].fields.op1) * wt.half_bytes[1].fields.op1;
// //     // weightedSum += (data<32>)(in.half_bytes[2].fields.op0) * wt.half_bytes[2].fields.op0;
// //     // weightedSum += (data<32>)(in.half_bytes[2].fields.op1) * wt.half_bytes[2].fields.op1;
// //     // weightedSum += (data<32>)(in.half_bytes[3].fields.op0) * wt.half_bytes[3].fields.op0;
// //     // weightedSum += (data<32>)(in.half_bytes[3].fields.op1) * wt.half_bytes[3].fields.op1;

// //     return weightedSum;
// // }

// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T octoMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     uint32_t wt;
//     memcpy((void*) &wt, weights, sizeof(wt));

//     // Works with weights * 4096 (weights << 12)
//     const uint32_t WeightMask = 0xF000F000;
//     uint32_t weight0 = WeightMask & (wt << 12);
//     uint32_t weight1 = WeightMask & (wt << 8);
//     uint32_t weight2 = WeightMask & (wt << 4);
//     uint32_t weight3 = WeightMask & (wt);

//     uint32_t in;
//     memcpy((void*) &in, inputs, sizeof(in));

//     const uint32_t ActMask = 0x000F000F; // to explicit instructions
//     uint32_t act0 = in & ActMask;
//     // Expect second operand shift
//     uint32_t act1 = ActMask & (in >> 4);
//     uint32_t act2 = ActMask & (in >> 8);
//     uint32_t act3 = ActMask & (in >> 12);

//     Sum_T sum = 0;
//     sum = __SMLAD(act0, weight0, sum);
//     sum = __SMLAD(act1, weight1, sum);
//     sum = __SMLAD(act2, weight2, sum);
//     sum = __SMLAD(act3, weight3, sum);

//     return weightedSum + (sum >> 12);
// }

// /**
//  * @brief   Signed octo mac operation (4W/4A version)
//  * @details Performs eight mac operations for signed 4-bits weights
//  *          and signed 4-bits inputs. Extracts the eight 4-bits weights
//  *          from four stored 8-bits weights and associates them into 
//  *          four 32-bits values. Then extracts the eight 4-bits inputs
//  *          from four stored 8-bits inputs and associates them into 
//  *          four 32-bits values. Finally performs a quadruple dual mac operation 
//  *          with the __SMLAD instruction
//  * 
//  * @tparam  Input_T     Input type (should be data<4>)
//  * @tparam  Weight_T    Weight type (should be data<4>)
//  * 
//  * @param[in]      inputs          Pointer to compressed input vector
//  * @param[in]      weights         Pointer to compressed kernel weights
//  * @param[in,out]  weightedSum     Accumulating sum from the 
//  *                                 previous mac operations
//  * @returns                        Updated weightedSum with 
//  *                                 the result of the octo mac operation
//  */
// template<typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(!std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T octoMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     uint32_t wt;
//     std::memcpy((void*) &wt, weights, sizeof(wt));

//     int32_t w0 = __SBFX(wt, 0, 4);
//     int32_t w1 = __SBFX(wt, 4, 4);
//     int32_t w2 = __SBFX(wt, 8, 4);
//     int32_t w3 = __SBFX(wt, 12, 4);
//     int32_t w4 = __SBFX(wt, 16, 4);
//     int32_t w5 = __SBFX(wt, 20, 4);
//     int32_t w6 = __SBFX(wt, 24, 4);
//     int32_t w7 = __SBFX(wt, 28, 4);

//     uint32_t evenW1 = __PKHBT(w2, w0, 16);
//     uint32_t oddW1  = __PKHBT(w3, w1, 16);
//     uint32_t evenW2 = __PKHBT(w6, w4, 16);
//     uint32_t oddW2  = __PKHBT(w7, w5, 16);

//     uint32_t in;
//     std::memcpy((void*) &in, inputs, sizeof(in));

//     int32_t a0 = __SBFX(in, 0, 4);
//     int32_t a1 = __SBFX(in, 4, 4);
//     int32_t a2 = __SBFX(in, 8, 4);
//     int32_t a3 = __SBFX(in, 12, 4);
//     int32_t a4 = __SBFX(in, 16, 4);
//     int32_t a5 = __SBFX(in, 20, 4);
//     int32_t a6 = __SBFX(in, 24, 4);
//     int32_t a7 = __SBFX(in, 28, 4);

//     uint32_t evenA1 = __PKHBT(a2, a0, 16);
//     uint32_t oddA1  = __PKHBT(a3, a1, 16);
//     uint32_t evenA2 = __PKHBT(a6, a4, 16);
//     uint32_t oddA2  = __PKHBT(a7, a5, 16);

//     weightedSum = __SMLAD(evenA1, evenW1, weightedSum);
//     weightedSum = __SMLAD(oddA1, oddW1, weightedSum);
//     weightedSum = __SMLAD(evenA2, evenW2, weightedSum);
//     weightedSum = __SMLAD(oddA2, oddW2, weightedSum);

//     return weightedSum;
// }


// // template<typename Input_T, typename Weight_T, typename Sum_T,
// //          typename std::enable_if<(std::is_unsigned<Input_T>::value
// //          && std::numeric_limits<Weight_T>::digits == 4
// //          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// // void macsOnParallel(const Input_T* __restrict inputs,
// //                     const Weight_T* __restrict weights,
// //                     Sum_T* weightedSums,
// //                     const int nb_data)
// // {
// //     uint32_t wt = 0;
// //     std::memcpy((void*) &wt, weights, ceil((double)nb_data/2));

// //     uint32_t in = 0;
// //     std::memcpy((void*) &in, inputs, ceil((double)nb_data/2));

// //     for (int i = 0; i < nb_data; ++i) {
// //         weightedSums[i] += __SBFX(wt, 4*i, 4) * __UBFX(in, 4*i, 4);
// //     }
// // }

// // template<typename Input_T, typename Weight_T, typename Sum_T,
// //          typename std::enable_if<(!std::is_unsigned<Input_T>::value
// //          && std::numeric_limits<Weight_T>::digits == 4
// //          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// // void macsOnParallel(const Input_T* __restrict inputs,
// //                     const Weight_T* __restrict weights,
// //                     Sum_T* weightedSums,
// //                     const int nb_data)
// // {
// //     uint32_t wt = 0;
// //     std::memcpy((void*) &wt, weights, ceil((double)nb_data/2));

// //     uint32_t in = 0;
// //     std::memcpy((void*) &in, inputs, ceil((double)nb_data/2));

// //     for (int i = 0; i < nb_data; ++i) {
// //         weightedSums[i] += __SBFX(wt, 4*i, 4) * __SBFX(in, 4*i, 4);
// //     }
// // }




// // **************************************************************************
// // * Multiply-accumulate the values in inputs and weights for NB_ITERATIONS *
// // **************************************************************************

// template<int NB_ITERATIONS,
//          int INPUTS_INC = 1,
//          int WEIGHTS_INC = 1,
//          class Input_T, 
//          class Weight_T,
//          class Sum_T,
//          typename std::enable_if<(NB_ITERATIONS == 0)>::type* = nullptr>
// inline static 
// void macsOnRange(const Input_T* __restrict /*inputs*/, 
//                  const Weight_T* __restrict /*weights*/, 
//                  Sum_T& __restrict /*weightedSum*/) 
// {
//     // Nothing to do
// }

// template<int NB_ITERATIONS,
//          int INPUTS_INC = 1,
//          int WEIGHTS_INC = 1,
//          class Input_T, 
//          class Weight_T,
//          class Sum_T,
//          typename std::enable_if<(NB_ITERATIONS == 1)>::type* = nullptr>
// inline static 
// void macsOnRange(const Input_T* __restrict inputs, 
//                  const Weight_T* __restrict weights, 
//                  Sum_T& __restrict weightedSum) 
// {
//     weightedSum += (*weights) * (*inputs);
// }

// template<int NB_ITERATIONS,
//          int INPUTS_INC = 1,
//          int WEIGHTS_INC = 1,
//          class Input_T, 
//          class Weight_T,
//          class Sum_T,
//          typename std::enable_if<(NB_ITERATIONS >= 2 && NB_ITERATIONS < 4)>::type* = nullptr>
// inline static 
// void macsOnRange(const Input_T* __restrict inputs, 
//                  const Weight_T* __restrict weights, 
//                  Sum_T& __restrict weightedSum) 
// {
//     weightedSum = dualMac<INPUTS_INC, WEIGHTS_INC>(inputs, weights, weightedSum);
//     macsOnRange<NB_ITERATIONS - 2, INPUTS_INC, WEIGHTS_INC>(inputs + 2*INPUTS_INC, 
//                                                             weights + 2*WEIGHTS_INC, 
//                                                             weightedSum);
// }

// /**
//  * @brief   MACs Processing
//  * @details Performs NB_ITERATIONS MACs operations, storing results into the
//  *          weightedSum variable. 
//  * 
//  * @tparam  NB_ITERATIONS   Number of MACs to perform
//  * @tparam  INPUTS_INC      Input Stride
//  * @tparam  WEIGHTS_INC     Weights Stride
//  * @tparam  Input_T         Input Type
//  * 
//  * @param   inputs          Pointer to inputs vector
//  * @param   weights         Pointer to weights vector
//  * @param   weightedSum     Pointer to weightedSum
// */
// template<int NB_ITERATIONS,
//          int INPUTS_INC = 1,
//          int WEIGHTS_INC = 1,
//          class Input_T, 
//          class Weight_T,
//          class Sum_T,
//          typename std::enable_if<(NB_ITERATIONS >= 4)>::type* = nullptr>
// inline static 
// void macsOnRange(const Input_T* __restrict inputs, 
//                  const Weight_T* __restrict weights, 
//                  Sum_T& __restrict weightedSum) 
// {
//     weightedSum = quadMac<INPUTS_INC, WEIGHTS_INC>(inputs, weights, weightedSum);
//     macsOnRange<NB_ITERATIONS - 4, INPUTS_INC, WEIGHTS_INC>(inputs + 4*INPUTS_INC, 
//                                                             weights + 4*WEIGHTS_INC, 
//                                                             weightedSum);
// }


// template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(NB_ITERATIONS >= 2 && NB_ITERATIONS < 4 && std::numeric_limits<Weight_T>::digits > 1)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// void macsOnRange(const Input_T* __restrict inputs,
//                  const Weight_T* __restrict weights,
//                  Sum_T& weightedSum)
// {
//     constexpr unsigned int idxI 
//         = (std::numeric_limits<Input_T>::digits > 4) ? 2 : 1;
//     constexpr unsigned int idxW 
//         = (std::numeric_limits<Weight_T>::digits > 4) ? 2 : 1;

//     weightedSum = dualMac(inputs, weights, weightedSum);
//     macsOnRange<NB_ITERATIONS - 2>(inputs + idxI, weights + idxW, weightedSum);
// }

// template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<NB_ITERATIONS >= 4 
//          && (std::numeric_limits<Weight_T>::digits > 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// void macsOnRange(const Input_T* __restrict inputs,
//                  const Weight_T* __restrict weights,
//                  Sum_T& weightedSum)
// {
//     constexpr unsigned int idxI 
//         = (std::numeric_limits<Input_T>::digits > 4) 
//           ? 4 : (std::numeric_limits<Input_T>::digits == 4) ? 2 : 1;

//     constexpr unsigned int idxW = 4;

//     weightedSum = quadMac(inputs, weights, weightedSum);
//     macsOnRange<NB_ITERATIONS - 4>(inputs + idxI, weights + idxW, weightedSum);
// }

// template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<(NB_ITERATIONS >= 4 && NB_ITERATIONS < 8) 
//          && (std::numeric_limits<Weight_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// void macsOnRange(const Input_T* __restrict inputs,
//                  const Weight_T* __restrict weights,
//                  Sum_T& weightedSum)
// {
//     constexpr unsigned int idxI 
//         = (std::numeric_limits<Input_T>::digits > 4) 
//           ? 4 : (std::numeric_limits<Input_T>::digits == 4) ? 2 : 1;

//     constexpr unsigned int idxW = 2;

//     weightedSum = quadMac(inputs, weights, weightedSum);
//     macsOnRange<NB_ITERATIONS - 4>(inputs + idxI, weights + idxW, weightedSum);
// }

// template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
//          typename std::enable_if<NB_ITERATIONS >= 8 
//          && (std::numeric_limits<Weight_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// void macsOnRange(const Input_T* __restrict inputs,
//                  const Weight_T* __restrict weights,
//                  Sum_T& weightedSum)
// {
//     constexpr unsigned int idxI 
//         = (std::numeric_limits<Input_T>::digits > 4) 
//           ? 8 : (std::numeric_limits<Input_T>::digits == 4) 
//             ? 4 : (std::numeric_limits<Input_T>::digits == 2)
//               ? 2 : 1;

//     constexpr unsigned int idxW = 4;

//     weightedSum = octoMac(inputs, weights, weightedSum);
//     macsOnRange<NB_ITERATIONS - 8>(inputs + idxI, weights + idxW, weightedSum);
// }


// }   // N2D2_Export

// #endif  // __N2D2_EXPORT_CPP_MACS_HPP__




/**
 ******************************************************************************
 * @file     mac_functions.hpp
 * @brief    Mac operation functions for ARM Cortex m7 and m4
 *           This file provides different functions to perform
 *           signed and unsigned mac operations. Those functions can calculate
 *           up to eight mac operations at once.
 *           The file also provides two general mac operation which can be
 *           used in other files, especially in Network.hpp
 * 
 ******************************************************************************
 * @attention
 * 
 * (C) Copyright 2021 CEA LIST. All Rights Reserved.
 *  Contributor(s): Vincent TEMPLIER (vincent.templier@cea.fr)
 *                  Philippe DORE (philippe.dore@cea.fr)
 *                  David BRIAND (david.briand@cea.fr)
 * 
 * This file is not part of the open source version of N2D2 and is NOT under
 * the CeCILL-C license. This code is the property of the CEA. It can not be
 * copied or disseminated without its authorization.
 * 
 ******************************************************************************
 */

#ifndef __N2D2_MAC_FUNCTIONS_HPP__
#define __N2D2_MAC_FUNCTIONS_HPP__

#include <cstring>
#include "swar_arm_acle.h"
#include "kernels/typedefs.hpp"


// ----------------------------------------------------------------------------
// --------------- MAC computing functions for all kernels --------------------
// ----------------------------------------------------------------------------


// ----------------------------------------------------------------------------
// -------------- MAC computing functions for kernel 8W-8A --------------------
// ----------------------------------------------------------------------------

/**
 * @brief   Mono mac operation (8W/8A version)
 * @details Performs one mac operation for signed 8-bits weights
 *          and 8-bits inputs (signed or not).
 * 
 * @tparam  Input_T     Input type (udata<8> or data<8>)
 * @tparam  Weight_T    Weight type (should be data<8>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 8
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T monoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    weightedSum += (Sum_T)inputs[0] * weights[0];
    return weightedSum;
}

/**
 * @brief   Dual mac operation (8W/8A version)
 * @details Performs two mac operations for signed 8-bits weights
 *          and 8-bits inputs (signed or not).
 * 
 * @tparam  Input_T     Input type (udata<8> or data<8>)
 * @tparam  Weight_T    Weight type (should be data<8>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 8
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T dualMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    weightedSum += (Sum_T)inputs[0] * weights[0] + (Sum_T)inputs[1] * weights[1];
    return weightedSum;
}

/**
 * @brief   Unsigned quad mac operation (8W/8A version)
 * @details Performs four mac operations for signed 8-bits weights
 *          and unsigned 8-bits inputs. Sign extends four 8-bits weights
 *          and associates them into two 32-bits values. Then zero extends 
 *          four 8-bits inputs and associates them into two 32-bits values. 
 *          Finally performs a double dual mac operation 
 *          with the __SMLAD instruction.
 * 
 * @tparam  Input_T     Input type (should be udata<8>)
 * @tparam  Weight_T    Weight type (should be data<8>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the quad mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 8
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint32_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    uint32_t in1 = __UXTB16(in);
    uint32_t in2 = __UXTB16_RORn(in, 8);

    uint32_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    uint32_t wt1 = __SXTB16(wt);
    uint32_t wt2 = __SXTB16_RORn(wt, 8);

    weightedSum = __SMLAD(in1, wt1, weightedSum);
    weightedSum = __SMLAD(in2, wt2, weightedSum);
    
    return weightedSum;
}

/**
 * @brief   Signed quad mac operation (8W/8A version)
 * @details Performs four mac operations for signed 8-bits weights
 *          and signed 8-bits inputs. Sign extends four 8-bits weights
 *          and associates them into two 32-bits values. Then sign extends 
 *          four 8-bits inputs and associates them into two 32-bits values. 
 *          Finally performs a double dual mac operation 
 *          with the __SMLAD instruction.
 * 
 * @tparam  Input_T     Input type (should be data<8>)
 * @tparam  Weight_T    Weight type (should be data<8>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the quad mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 8
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint32_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    uint32_t in1 = __SXTB16(in);
    uint32_t in2 = __SXTB16_RORn(in, 8);

    uint32_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    uint32_t wt1 = __SXTB16(wt);
    uint32_t wt2 = __SXTB16_RORn(wt, 8);

    weightedSum = __SMLAD(in1, wt1, weightedSum);
    weightedSum = __SMLAD(in2, wt2, weightedSum);
    
    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 8
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
void macsOnParallel(const Input_T* __restrict inputs,
                    const Weight_T* __restrict weights,
                    Sum_T* weightedSums,
                    const int nb_data)
{
    union n2d2_dataword wt = {0};
    std::memcpy((void*) &wt, weights, nb_data);

    typename std::conditional<(!std::is_unsigned<Input_T>::value), 
            union n2d2_dataword, union n2d2_udataword>::type in = {0};
    std::memcpy((void*) &in, inputs, nb_data);

    for (int i = 0; i < nb_data; ++i) {
        weightedSums[i] += (Sum_T)wt.bytes[i] * in.bytes[i];
    }
}



// ----------------------------------------------------------------------------
// -------------- MAC computing functions for kernel 4W-8A --------------------
// ----------------------------------------------------------------------------

/**
 * @brief   Mono mac operation (4W/8A version)
 * @details Performs one mac operation for signed 4-bits weights
 *          and 8-bits inputs (signed or not).
 * 
 * @tparam  Input_T     Input type (udata<8> or data<8>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T monoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    weightedSum += (Sum_T)inputs[0] * __SBFX(weights[0], 4, 4);
    return weightedSum;
}

/**
 * @brief   Unsigned dual mac operation (4W/8A version)
 * @details Performs two mac operations for signed 4-bits weights
 *          and unsigned 8-bits inputs. Extracts the two 4-bits weights
 *          from a stored 8-bits weight and associates them into 
 *          a 32-bits value. Then zero extends two 8-bits inputs and 
 *          associates them into a 32-bits value. Finally performs a
 *          dual mac operation with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be udata<8>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T dualMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint8_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    uint32_t wght = __BFI(w0, w1, 16, 16);

    uint16_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));
    
    uint32_t act = ((in << 8) | in);
    act = __UXTB16(act);
    
    weightedSum = __SMLAD(act, wght, weightedSum);

    return weightedSum;
}

/**
 * @brief   Signed dual mac operation (4W/8A version)
 * @details Performs two mac operations for signed 4-bits weights
 *          and signed 8-bits inputs. Extracts the two 4-bits weights
 *          from a stored 8-bits weight and associates them into 
 *          a 32-bits value. Then sign extends two 8-bits inputs and 
 *          associates them into a 32-bits value. Finally performs a
 *          dual mac operation with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be data<8>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T dualMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint8_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    uint32_t wght = __BFI(w0, w1, 16, 16);

    uint16_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));
    
    uint32_t act = ((in << 8) | in);
    act = __SXTB16(act);
    
    weightedSum = __SMLAD(act, wght, weightedSum);

    return weightedSum;
}

/**
 * @brief   Unsigned quad mac operation (4W/8A version)
 * @details Performs four mac operations for signed 4-bits weights
 *          and unsigned 8-bits inputs. Extracts the four 4-bits weights
 *          from two stored 8-bits weights and associates them into 
 *          two 32-bits values. Then zero extends four 8-bits inputs and 
 *          associates them into two 32-bits values. Finally performs a
 *          double dual mac operation with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be udata<8>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the quad mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint16_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    int32_t w2 = __SBFX(wt, 8, 4);
    int32_t w3 = __SBFX(wt, 12, 4);

    uint32_t evenW1 = __PKHBT(w0, w2, 16);
    uint32_t oddW1  = __PKHBT(w1, w3, 16);

    uint32_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    uint32_t evenA1 = __UXTB16(in);
    uint32_t oddA1  = __UXTB16_RORn(in, 8);

    weightedSum = __SMLAD(evenA1, oddW1, weightedSum);
    weightedSum = __SMLAD(oddA1, evenW1, weightedSum);

    return weightedSum;
}

/**
 * @brief   Signed quad mac operation (4W/8A version)
 * @details Performs four mac operations for signed 4-bits weights
 *          and signed 8-bits inputs. Extracts the four 4-bits weights
 *          from two stored 8-bits weights and associates them into 
 *          two 32-bits values. Then sign extends four 8-bits inputs and 
 *          associates them into two 32-bits values. Finally performs a
 *          double dual mac operation with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be data<8>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the quad mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint16_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    int32_t w2 = __SBFX(wt, 8, 4);
    int32_t w3 = __SBFX(wt, 12, 4);

    uint32_t evenW1 = __BFI(w2, w0, 16, 16);
    uint32_t oddW1  = __BFI(w3, w1, 16, 16);

    uint32_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    uint32_t evenA1 = __SXTB16(in);
    uint32_t oddA1  = __SXTB16_RORn(in, 8);

    weightedSum = __SMLAD(evenA1, oddW1, weightedSum);
    weightedSum = __SMLAD(oddA1, evenW1, weightedSum);

    return weightedSum;
}

/**
 * @brief   Unsigned octo mac operation (4W/8A version)
 * @details Performs eight mac operations for signed 4-bits weights
 *          and unsigned 8-bits inputs. Extracts the eight 4-bits weights
 *          from four stored 8-bits weights and associates them into 
 *          four 32-bits values. Then zero extends eights 8-bits inputs and 
 *          associates them into four 32-bits values. Finally performs a
 *          quadruple dual mac operation with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be udata<8>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the octo mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    // uint32_t wt;
    // std::memcpy((void*) &wt, weights, sizeof(wt));

    // int32_t w0 = __SBFX(wt, 0, 4);
    // int32_t w1 = __SBFX(wt, 4, 4);
    // int32_t w2 = __SBFX(wt, 8, 4);
    // int32_t w3 = __SBFX(wt, 12, 4);
    // int32_t w4 = __SBFX(wt, 16, 4);
    // int32_t w5 = __SBFX(wt, 20, 4);
    // int32_t w6 = __SBFX(wt, 24, 4);
    // int32_t w7 = __SBFX(wt, 28, 4);

    // // uint32_t evenW1 = __BFI(w2, w0, 16, 16);
    // // uint32_t oddW1  = __BFI(w3, w1, 16, 16);
    // // uint32_t evenW2 = __BFI(w6, w4, 16, 16);
    // // uint32_t oddW2  = __BFI(w7, w5, 16, 16);

    // uint32_t evenW1 = __PKHBT(w0, w2, 16);
    // uint32_t oddW1  = __PKHBT(w1, w3, 16);
    // uint32_t evenW2 = __PKHBT(w4, w6, 16);
    // uint32_t oddW2  = __PKHBT(w5, w7, 16);

    // uint32_t in1, in2;
    // std::memcpy((void*) &in1, inputs, sizeof(in1));
    // std::memcpy((void*) &in2, (inputs + 4), sizeof(in2));
    
    // uint32_t evenA1 = __UXTB16(in1);
    // uint32_t oddA1  = __UXTB16_RORn(in1, 8);
    // uint32_t evenA2 = __UXTB16(in2);
    // uint32_t oddA2  = __UXTB16_RORn(in2, 8);
    
    // weightedSum = __SMLAD(evenA1, oddW1, weightedSum);
    // weightedSum = __SMLAD(oddA1, evenW1, weightedSum);
    // weightedSum = __SMLAD(evenA2, oddW2, weightedSum);
    // weightedSum = __SMLAD(oddA2, evenW2, weightedSum);

    // 2nd implementation
    // union n2d2_dataword wt;
    // std::memcpy((void*) &wt, weights, sizeof(wt));

    // union n2d2_udataword in1, in2;
    // std::memcpy((void*) &in1, inputs, sizeof(in1));
    // std::memcpy((void*) &in2, inputs + 4, sizeof(in2));

    // weightedSum += (data<32>)(in1.bytes[0]) * wt.half_bytes[0].fields.op1;
    // weightedSum += (data<32>)(in1.bytes[1]) * wt.half_bytes[0].fields.op0;
    // weightedSum += (data<32>)(in1.bytes[2]) * wt.half_bytes[1].fields.op1;
    // weightedSum += (data<32>)(in1.bytes[3]) * wt.half_bytes[1].fields.op0;
    // weightedSum += (data<32>)(in2.bytes[0]) * wt.half_bytes[2].fields.op1;
    // weightedSum += (data<32>)(in2.bytes[1]) * wt.half_bytes[2].fields.op0;
    // weightedSum += (data<32>)(in2.bytes[2]) * wt.half_bytes[3].fields.op1;
    // weightedSum += (data<32>)(in2.bytes[3]) * wt.half_bytes[3].fields.op0;

    uint32_t wt;
    memcpy((void*) &wt, weights, sizeof(wt));

    // Works with weights * 4096 (weights << 12)
    const uint32_t WeightMask = 0xF000F000;
    uint32_t weight0 = WeightMask & (wt << 12);
    uint32_t weight1 = WeightMask & (wt << 8);
    uint32_t weight2 = WeightMask & (wt << 4);
    uint32_t weight3 = WeightMask & (wt);

    uint32_t in1, in2;
    std::memcpy((void*) &in1, inputs, sizeof(in1));
    std::memcpy((void*) &in2, (inputs + 4), sizeof(in2));

    uint32_t in_a = __PKHBT(in1, in2, 16);
    uint32_t in_b = __PKHTB(in2, in1, 16);
    
    uint32_t evenA1 = __UXTB16(in_a);
    uint32_t oddA1  = __UXTB16_RORn(in_a, 8);
    uint32_t evenA2 = __UXTB16(in_b);
    uint32_t oddA2  = __UXTB16_RORn(in_b, 8);

    Sum_T sum = 0;
    sum = __SMLAD(oddA1, weight0, sum);
    sum = __SMLAD(evenA1, weight1, sum);
    sum = __SMLAD(oddA2, weight2, sum);
    sum = __SMLAD(evenA2, weight3, sum);
    weightedSum += sum >> 12;

    return weightedSum;
}

/**
 * @brief   Signed octo mac operation (4W/8A version)
 * @details Performs eight mac operations for signed 4-bits weights
 *          and signed 8-bits inputs. Extracts the eight 4-bits weights
 *          from four stored 8-bits weights and associates them into 
 *          four 32-bits values. Then sign extends eights 8-bits inputs and 
 *          associates them into four 32-bits values. Finally performs a
 *          quadruple dual mac operation with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be data<8>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the octo mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint32_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    int32_t w2 = __SBFX(wt, 8, 4);
    int32_t w3 = __SBFX(wt, 12, 4);
    int32_t w4 = __SBFX(wt, 16, 4);
    int32_t w5 = __SBFX(wt, 20, 4);
    int32_t w6 = __SBFX(wt, 24, 4);
    int32_t w7 = __SBFX(wt, 28, 4);

    uint32_t evenW1 = __BFI(w2, w0, 16, 16);
    uint32_t oddW1  = __BFI(w3, w1, 16, 16);
    uint32_t evenW2 = __BFI(w6, w4, 16, 16);
    uint32_t oddW2  = __BFI(w7, w5, 16, 16);

    uint32_t in1, in2;
    std::memcpy((void*) &in1, inputs, sizeof(in1));
    std::memcpy((void*) &in2, (inputs + 4), sizeof(in2));
    
    uint32_t evenA1 = __SXTB16(in1);
    uint32_t oddA1  = __SXTB16_RORn(in1, 8);
    uint32_t evenA2 = __SXTB16(in2);
    uint32_t oddA2  = __SXTB16_RORn(in2, 8);
    
    weightedSum = __SMLAD(evenA1, oddW1, weightedSum);
    weightedSum = __SMLAD(oddA1, evenW1, weightedSum);
    weightedSum = __SMLAD(evenA2, oddW2, weightedSum);
    weightedSum = __SMLAD(oddA2, evenW2, weightedSum);

    return weightedSum;
}


template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(
            std::numeric_limits<Weight_T>::digits == 4 && 
            std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
void macsOnParallel(const Input_T* __restrict inputs,
                    const Weight_T* __restrict weights,
                    Sum_T* weightedSums,
                    const int nb_data)
{
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, ceil((double)nb_data/2));

    for (int i = 0; i < nb_data; ++i) {
        weightedSums[i] += __SBFX(wt, 4*i, 4) * inputs[i];
    }
}


// ----------------------------------------------------------------------------
// -------------- MAC computing functions for kernel 4W-4A --------------------
// ----------------------------------------------------------------------------

/**
 * @brief   Unsigned mono mac operation (4W/4A version)
 * @details Performs one mac operation for signed 4-bits weights
 *          and unsigned 4-bits inputs.
 * 
 * @tparam  Input_T     Input type (should be udata<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T monoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    weightedSum += __UBFX(inputs[0], 4, 4) * __SBFX(weights[0], 4, 4);
    return weightedSum;
}

/**
 * @brief   Signed mono mac operation (4W/4A version)
 * @details Performs one mac operation for signed 4-bits weights
 *          and signed 4-bits inputs.
 * 
 * @tparam  Input_T     Input type (should be data<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to input vector
 * @param[in]      weights         Pointer to kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T monoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    weightedSum += __SBFX(inputs[0], 4, 4) * __SBFX(weights[0], 4, 4);
    return weightedSum;
}

/**
 * @brief   Unsigned dual mac operation (4W/4A version)
 * @details Performs two mac operations for signed 4-bits weights
 *          and unsigned 4-bits inputs. Extracts the two 4-bits weights
 *          from a stored 8-bits weight and associates them into 
 *          a 32-bits value. Then extracts the two 4-bits inputs
 *          from a stored 8-bits input and associates them into 
 *          a 32-bits value. Finally performs a dual mac operation 
 *          with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be udata<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to compressed input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T dualMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint8_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    uint32_t wght = __BFI(w1, w0, 16, 16);

    uint8_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    int32_t a0 = __UBFX(in, 0, 4);
    int32_t a1 = __UBFX(in, 4, 4);
    uint32_t act = __BFI(a1, a0, 16, 16);

    weightedSum = __SMLAD(act, wght, weightedSum);

    return weightedSum;
}

/**
 * @brief   Signed dual mac operation (4W/4A version)
 * @details Performs two mac operations for signed 4-bits weights
 *          and signed 4-bits inputs. Extracts the two 4-bits weights
 *          from a stored 8-bits weight and associates them into 
 *          a 32-bits value. Then extracts the two 4-bits inputs
 *          from a stored 8-bits input and associates them into 
 *          a 32-bits value. Finally performs a dual mac operation 
 *          with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be data<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to compressed input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the dual mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T dualMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint8_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    uint32_t wght = __BFI(w1, w0, 16, 16);

    uint8_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    int32_t a0 = __SBFX(in, 0, 4);
    int32_t a1 = __SBFX(in, 4, 4);
    uint32_t act = __BFI(a1, a0, 16, 16);

    weightedSum = __SMLAD(act, wght, weightedSum);

    return weightedSum;
}

/**
 * @brief   Unsigned quad mac operation (4W/4A version)
 * @details Performs four mac operations for signed 4-bits weights
 *          and unsigned 4-bits inputs. Extracts the four 4-bits weights
 *          from two stored 8-bits weights and associates them into 
 *          two 32-bits values. Then extracts the four 4-bits inputs
 *          from two stored 8-bits inputs and associates them into 
 *          two 32-bits values. Finally performs a double dual mac operation 
 *          with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be udata<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to compressed input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the quad mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint16_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    int32_t w2 = __SBFX(wt, 8, 4);
    int32_t w3 = __SBFX(wt, 12, 4);

    uint32_t evenW1 = __BFI(w2, w0, 16, 16);
    uint32_t oddW1  = __BFI(w3, w1, 16, 16);

    uint16_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    int32_t a0 = __UBFX(in, 0, 4);
    int32_t a1 = __UBFX(in, 4, 4);
    int32_t a2 = __UBFX(in, 8, 4);
    int32_t a3 = __UBFX(in, 12, 4);

    uint32_t evenA1 = __BFI(a2, a0, 16, 16);
    uint32_t oddA1  = __BFI(a3, a1, 16, 16);

    weightedSum = __SMLAD(evenA1, evenW1, weightedSum);
    weightedSum = __SMLAD(oddA1, oddW1, weightedSum);

    return weightedSum;
}

/**
 * @brief   Signed quad mac operation (4W/4A version)
 * @details Performs four mac operations for signed 4-bits weights
 *          and signed 4-bits inputs. Extracts the four 4-bits weights
 *          from two stored 8-bits weights and associates them into 
 *          two 32-bits values. Then extracts the four 4-bits inputs
 *          from two stored 8-bits inputs and associates them into 
 *          two 32-bits values. Finally performs a double dual mac operation 
 *          with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be data<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to compressed input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the quad mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint16_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    int32_t w2 = __SBFX(wt, 8, 4);
    int32_t w3 = __SBFX(wt, 12, 4);

    uint32_t evenW1 = __PKHBT(w2, w0, 16);
    uint32_t oddW1  = __PKHBT(w3, w1, 16);

    uint16_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    int32_t a0 = __SBFX(in, 0, 4);
    int32_t a1 = __SBFX(in, 4, 4);
    int32_t a2 = __SBFX(in, 8, 4);
    int32_t a3 = __SBFX(in, 12, 4);
    
    uint32_t evenA1 = __PKHBT(a2, a0, 16);
    uint32_t oddA1  = __PKHBT(a3, a1, 16);

    weightedSum = __SMLAD(evenA1, evenW1, weightedSum);
    weightedSum = __SMLAD(oddA1, oddW1, weightedSum);

    return weightedSum;
}

/**
 * @brief   Unsigned octo mac operation (4W/4A version)
 * @details Performs eight mac operations for signed 4-bits weights
 *          and unsigned 4-bits inputs. Extracts the eight 4-bits weights
 *          from four stored 8-bits weights and associates them into 
 *          four 32-bits values. Then extracts the eight 4-bits inputs
 *          from four stored 8-bits inputs and associates them into 
 *          four 32-bits values. Finally performs a quadruple dual mac operation 
 *          with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be udata<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to compressed input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the octo mac operation
 */
// template<typename Input_T, typename Weight_T,
//          typename std::enable_if<(std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T octoMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     uint32_t wt;
//     std::memcpy((void*) &wt, weights, sizeof(wt));

//     int32_t w0 = __SBFX(wt, 0, 4);
//     int32_t w1 = __SBFX(wt, 4, 4);
//     int32_t w2 = __SBFX(wt, 8, 4);
//     int32_t w3 = __SBFX(wt, 12, 4);
//     int32_t w4 = __SBFX(wt, 16, 4);
//     int32_t w5 = __SBFX(wt, 20, 4);
//     int32_t w6 = __SBFX(wt, 24, 4);
//     int32_t w7 = __SBFX(wt, 28, 4);

//     // uint32_t weight0 = __BFI(w4, w0, 16, 16);
//     // uint32_t weight1 = __BFI(w5, w1, 16, 16);
//     // uint32_t weight2 = __BFI(w6, w2, 16, 16);
//     // uint32_t weight3 = __BFI(w7, w3, 16, 16);

//     uint32_t weight0 = __PKHBT(w0, w4, 16);
//     uint32_t weight1 = __PKHBT(w1, w5, 16);
//     uint32_t weight2 = __PKHBT(w2, w6, 16);
//     uint32_t weight3 = __PKHBT(w3, w7, 16);

//     uint32_t in;
//     std::memcpy((void*) &in, inputs, sizeof(in));

//     uint32_t act0 = in & 0xF000F;
//     uint32_t act1 = (in >> 4) & 0xF000F;
//     uint32_t act2 = (in >> 8) & 0xF000F;
//     uint32_t act3 = (in >> 12) & 0xF000F;

//     weightedSum = __SMLAD(act0, weight0, weightedSum);
//     weightedSum = __SMLAD(act1, weight1, weightedSum);
//     weightedSum = __SMLAD(act2, weight2, weightedSum);
//     weightedSum = __SMLAD(act3, weight3, weightedSum);

//     return weightedSum;
// }

// template<typename Input_T, typename Weight_T,
//          typename std::enable_if<(std::is_unsigned<Input_T>::value
//          && std::numeric_limits<Weight_T>::digits == 4
//          && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
// __attribute__((always_inline)) static inline
// Sum_T octoMac(const Input_T* __restrict inputs,
//               const Weight_T* __restrict weights,
//               Sum_T weightedSum)
// {
//     union n2d2_dataword wt;
//     std::memcpy((void*) &wt, weights, sizeof(wt));

//     union n2d2_udataword in;
//     std::memcpy((void*) &in, inputs, sizeof(in));

//     for (int i = 0; i < 4; ++i) {
//         weightedSum += (data<32>)(in.half_bytes[i].fields.op0) * wt.half_bytes[i].fields.op0;
//         weightedSum += (data<32>)(in.half_bytes[i].fields.op1) * wt.half_bytes[i].fields.op1;
//     }

//     // weightedSum += (data<32>)(in.half_bytes[0].fields.op0) * wt.half_bytes[0].fields.op0;
//     // weightedSum += (data<32>)(in.half_bytes[0].fields.op1) * wt.half_bytes[0].fields.op1;
//     // weightedSum += (data<32>)(in.half_bytes[1].fields.op0) * wt.half_bytes[1].fields.op0;
//     // weightedSum += (data<32>)(in.half_bytes[1].fields.op1) * wt.half_bytes[1].fields.op1;
//     // weightedSum += (data<32>)(in.half_bytes[2].fields.op0) * wt.half_bytes[2].fields.op0;
//     // weightedSum += (data<32>)(in.half_bytes[2].fields.op1) * wt.half_bytes[2].fields.op1;
//     // weightedSum += (data<32>)(in.half_bytes[3].fields.op0) * wt.half_bytes[3].fields.op0;
//     // weightedSum += (data<32>)(in.half_bytes[3].fields.op1) * wt.half_bytes[3].fields.op1;

//     return weightedSum;
// }

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint32_t wt;
    memcpy((void*) &wt, weights, sizeof(wt));

    // Works with weights * 4096 (weights << 12)
    const uint32_t WeightMask = 0xF000F000;
    uint32_t weight0 = WeightMask & (wt << 12);
    uint32_t weight1 = WeightMask & (wt << 8);
    uint32_t weight2 = WeightMask & (wt << 4);
    uint32_t weight3 = WeightMask & (wt);

    uint32_t in;
    memcpy((void*) &in, inputs, sizeof(in));

    const uint32_t ActMask = 0x000F000F; // to explicit instructions
    uint32_t act0 = in & ActMask;
    // Expect second operand shift
    uint32_t act1 = ActMask & (in >> 4);
    uint32_t act2 = ActMask & (in >> 8);
    uint32_t act3 = ActMask & (in >> 12);

    Sum_T sum = 0;
    sum = __SMLAD(act0, weight0, sum);
    sum = __SMLAD(act1, weight1, sum);
    sum = __SMLAD(act2, weight2, sum);
    sum = __SMLAD(act3, weight3, sum);

    return weightedSum + (sum >> 12);
}

/**
 * @brief   Signed octo mac operation (4W/4A version)
 * @details Performs eight mac operations for signed 4-bits weights
 *          and signed 4-bits inputs. Extracts the eight 4-bits weights
 *          from four stored 8-bits weights and associates them into 
 *          four 32-bits values. Then extracts the eight 4-bits inputs
 *          from four stored 8-bits inputs and associates them into 
 *          four 32-bits values. Finally performs a quadruple dual mac operation 
 *          with the __SMLAD instruction
 * 
 * @tparam  Input_T     Input type (should be data<4>)
 * @tparam  Weight_T    Weight type (should be data<4>)
 * 
 * @param[in]      inputs          Pointer to compressed input vector
 * @param[in]      weights         Pointer to compressed kernel weights
 * @param[in,out]  weightedSum     Accumulating sum from the 
 *                                 previous mac operations
 * @returns                        Updated weightedSum with 
 *                                 the result of the octo mac operation
 */
template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac(const Input_T* __restrict inputs,
              const Weight_T* __restrict weights,
              Sum_T weightedSum)
{
    uint32_t wt;
    std::memcpy((void*) &wt, weights, sizeof(wt));

    int32_t w0 = __SBFX(wt, 0, 4);
    int32_t w1 = __SBFX(wt, 4, 4);
    int32_t w2 = __SBFX(wt, 8, 4);
    int32_t w3 = __SBFX(wt, 12, 4);
    int32_t w4 = __SBFX(wt, 16, 4);
    int32_t w5 = __SBFX(wt, 20, 4);
    int32_t w6 = __SBFX(wt, 24, 4);
    int32_t w7 = __SBFX(wt, 28, 4);

    uint32_t evenW1 = __PKHBT(w2, w0, 16);
    uint32_t oddW1  = __PKHBT(w3, w1, 16);
    uint32_t evenW2 = __PKHBT(w6, w4, 16);
    uint32_t oddW2  = __PKHBT(w7, w5, 16);

    uint32_t in;
    std::memcpy((void*) &in, inputs, sizeof(in));

    int32_t a0 = __SBFX(in, 0, 4);
    int32_t a1 = __SBFX(in, 4, 4);
    int32_t a2 = __SBFX(in, 8, 4);
    int32_t a3 = __SBFX(in, 12, 4);
    int32_t a4 = __SBFX(in, 16, 4);
    int32_t a5 = __SBFX(in, 20, 4);
    int32_t a6 = __SBFX(in, 24, 4);
    int32_t a7 = __SBFX(in, 28, 4);

    uint32_t evenA1 = __PKHBT(a2, a0, 16);
    uint32_t oddA1  = __PKHBT(a3, a1, 16);
    uint32_t evenA2 = __PKHBT(a6, a4, 16);
    uint32_t oddA2  = __PKHBT(a7, a5, 16);

    weightedSum = __SMLAD(evenA1, evenW1, weightedSum);
    weightedSum = __SMLAD(oddA1, oddW1, weightedSum);
    weightedSum = __SMLAD(evenA2, evenW2, weightedSum);
    weightedSum = __SMLAD(oddA2, oddW2, weightedSum);

    return weightedSum;
}


template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
void macsOnParallel(const Input_T* __restrict inputs,
                    const Weight_T* __restrict weights,
                    Sum_T* weightedSums,
                    const int nb_data)
{
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, ceil((double)nb_data/2));

    uint32_t in = 0;
    std::memcpy((void*) &in, inputs, ceil((double)nb_data/2));

    for (int i = 0; i < nb_data; ++i) {
        weightedSums[i] += __SBFX(wt, 4*i, 4) * __UBFX(in, 4*i, 4);
    }
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(!std::is_unsigned<Input_T>::value
         && std::numeric_limits<Weight_T>::digits == 4
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
void macsOnParallel(const Input_T* __restrict inputs,
                    const Weight_T* __restrict weights,
                    Sum_T* weightedSums,
                    const int nb_data)
{
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, ceil((double)nb_data/2));

    uint32_t in = 0;
    std::memcpy((void*) &in, inputs, ceil((double)nb_data/2));

    for (int i = 0; i < nb_data; ++i) {
        weightedSums[i] += __SBFX(wt, 4*i, 4) * __SBFX(in, 4*i, 4);
    }
}


// ----------------------------------------------------------------------------
// ------------------ Notes about performing MAC operations -------------------
// --------------------------- with 1-bit weights -----------------------------
// ----------------------------------------------------------------------------

/**
 * @note How to perform MAC operations with 1-bit weight
 * 
 * Working with an 1-bit weight means working only with two possible values 
 * for each weight. Thus, it has been defined a convention that will be used 
 * in the following functions in this file.
 * Convention: when the value of a weight is 0, it means 1
 *             when the value of a weight is 1, it means -1
 * 
 * Example: let's take a simple dual MAC operation
 *          weightedSum = w0 * a0 + w1 * a1;
 * 
 * if w0 = 0x00 and w1 = 0x01 then weightedSum should be:
 *          weightedSum = a0 - a1;
 * 
 * To easily perform MAC operations and use as often as possible
 * SIMD instructions to parallelize and speed up MAC calculations, most of
 * the following functions use the same scheme:
 * 
 *  - Perform a parallel subtraction of 0 and the weights
 *      Some SIMD instructions as __USUB16 and __USUB8 can perform 
 *      parallel subtractions and activate a Greater or Equal flag (GE) if
 *      the results of each subtraction is positive. 
 *      Thus, if the result of 0 - w0 >= 0 ==> GE[0] = 1
 *                             0 - w0 < 0  ==> GE[0] = 0
 *      (the results of the subtractions are not saved because only the 
 *       GE flags trigger is required)
 * 
 *  - Use of the __SEL instruction to read the GE flags
 *      The __SEL can select an input from two values according to the
 *      the GE flag provided by the previous subtraction. In the case of 
 *      the 1W/8A project, the two possible values selected by __SEL are
 *      (+input) or (-input). Thus, __SEL is often used like "__SEL(in, -in)"
 *      The results of __SEL are saved as MAC results
 * 
 *  - Addition of the accumuling sums with the results of the MAC operations
 *      Use of __SADD16 or __SADD8 for signed additions
 * 
 */

// ----------------------------------------------------------------------------
// ----------------- MAC computing functions for kernel -----------------------
// ------------------------------- 1W / 8A ------------------------------------
// ------------------------------- 1W / 7A ------------------------------------
// ------------------------------- 1W / 6A ------------------------------------
// ------------------------------- 1W / 5A ------------------------------------
// ----------------------------------------------------------------------------

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T monoMac (const Input_T* __restrict inputs,
               const Weight_T* __restrict weights,
               Sum_T weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0])) : (Sum_T)(inputs[0]);
    return weightedSum;
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS == 2)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0])) : (Sum_T)(inputs[0]);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[1])) : (Sum_T)(inputs[1]);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS == 3)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0])) : (Sum_T)(inputs[0]);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[1])) : (Sum_T)(inputs[1]);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[2])) : (Sum_T)(inputs[2]);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0])) : (Sum_T)(inputs[0]);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[1])) : (Sum_T)(inputs[1]);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[2])) : (Sum_T)(inputs[2]);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[3])) : (Sum_T)(inputs[3]);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS == 5)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0])) : (Sum_T)(inputs[0]);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[1])) : (Sum_T)(inputs[1]);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[2])) : (Sum_T)(inputs[2]);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[3])) : (Sum_T)(inputs[3]);
    weightedSum += (weights[0].fields.op3) ? (Sum_T)(-(inputs[4])) : (Sum_T)(inputs[4]);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS == 6)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0])) : (Sum_T)(inputs[0]);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[1])) : (Sum_T)(inputs[1]);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[2])) : (Sum_T)(inputs[2]);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[3])) : (Sum_T)(inputs[3]);
    weightedSum += (weights[0].fields.op3) ? (Sum_T)(-(inputs[4])) : (Sum_T)(inputs[4]);
    weightedSum += (weights[0].fields.op2) ? (Sum_T)(-(inputs[5])) : (Sum_T)(inputs[5]);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS == 7)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0])) : (Sum_T)(inputs[0]);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[1])) : (Sum_T)(inputs[1]);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[2])) : (Sum_T)(inputs[2]);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[3])) : (Sum_T)(inputs[3]);
    weightedSum += (weights[0].fields.op3) ? (Sum_T)(-(inputs[4])) : (Sum_T)(inputs[4]);
    weightedSum += (weights[0].fields.op2) ? (Sum_T)(-(inputs[5])) : (Sum_T)(inputs[5]);
    weightedSum += (weights[0].fields.op1) ? (Sum_T)(-(inputs[6])) : (Sum_T)(inputs[6]);
}


// ----------------------------------------------------------------------------
// ----------------- MAC computing functions for kernel -----------------------
// ------------------------------- 1W / 8A ------------------------------------
// ----------------------------------------------------------------------------

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T weightedSum)
{
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 1);
    wt |= wt << 16;

    memcpy((void*) &in, inputs, sizeof(in));
    uint32_t evenA1 = __UXTB16(in);
    uint32_t oddA1  = __UXTB16_RORn(in, 8);
    uint32_t neg_evenA1 = __SSUB16(0, evenA1);
    uint32_t neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x40001);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x80002);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  


    memcpy((void*) &in, inputs + 4, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x400010);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x800020);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 2);
    wt |= wt << 16;
    
    memcpy((void*) &in, inputs, sizeof(in));
    uint32_t evenA1 = __UXTB16(in);
    uint32_t oddA1  = __UXTB16_RORn(in, 8);
    uint32_t neg_evenA1 = __SSUB16(0, evenA1);
    uint32_t neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x40001);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x80002);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  


    memcpy((void*) &in, inputs + 4, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x400010);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x800020);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum); 


    memcpy((void*) &in, inputs + 8, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x4000100);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x8000200);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  


    memcpy((void*) &in, inputs + 12, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x40001000);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x80002000);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 8)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t wt;
    memcpy((void*) &wt, weights, 4);
    uint32_t wt1 = __PKHBT(wt, wt, 16);
    uint32_t wt2 = __PKHTB(wt, wt, 16);

    memcpy((void*) &in, inputs, sizeof(in));
    uint32_t evenA1 = __UXTB16(in);
    uint32_t oddA1  = __UXTB16_RORn(in, 8);
    uint32_t neg_evenA1 = __SSUB16(0, evenA1);
    uint32_t neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x40001);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x80002);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  


    memcpy((void*) &in, inputs + 4, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x400010);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x800020);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum); 


    memcpy((void*) &in, inputs + 8, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x4000100);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x8000200);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  


    memcpy((void*) &in, inputs + 12, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt & 0x40001000);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt & 0x80002000);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);


    memcpy((void*) &in, inputs + 16, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt2 & 0x40001);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt2 & 0x80002);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  


    memcpy((void*) &in, inputs + 20, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt2 & 0x400010);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt2 & 0x800020);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum); 


    memcpy((void*) &in, inputs + 24, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt2 & 0x4000100);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt2 & 0x8000200);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);  


    memcpy((void*) &in, inputs + 28, sizeof(in));
    evenA1 = __UXTB16(in);
    oddA1  = __UXTB16_RORn(in, 8);
    neg_evenA1 = __SSUB16(0, evenA1);
    neg_oddA1 = __SSUB16(0, oddA1);

    __USUB16(0, wt2 & 0x40001000);  
    mac_result = __SEL(evenA1, neg_evenA1);
    weightedSum = __SADD16(mac_result, weightedSum);  

    __USUB16(0, wt2 & 0x80002000);  
    mac_result = __SEL(oddA1, neg_oddA1);
    weightedSum = __SADD16(mac_result, weightedSum);

    return weightedSum;
}

// ----------------------------------------------------------------------------
// ----------------- MAC computing functions for kernel -----------------------
// ------------------------------- 1W / 7A ------------------------------------
// ----------------------------------------------------------------------------

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 7)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T weightedSum)
{
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 1);
    wt |= wt << 8;
    wt |= wt << 16;

    memcpy((void*) &in, inputs, sizeof(in));

    // Sign extend 
    if (!std::is_unsigned<Input_T>::value)
        in = (in + 0xC0C0C0C0) ^ 0xC0C0C0C0;

    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x08040201);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 4, sizeof(in));

    // Sign extend 
    if (!std::is_unsigned<Input_T>::value)
        in = (in + 0xC0C0C0C0) ^ 0xC0C0C0C0;

    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x80402010);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 7)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 4);

    memcpy((void*) &in, inputs, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x01010101);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 4, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x02020202);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 8, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x04040404);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 12, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x08080808);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 7)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 4);

    memcpy((void*) &in, inputs, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x01010101);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 4, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x02020202);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 8, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x04040404);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 12, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x08080808);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 16, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x10101010);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 20, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x20202020);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 24, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x40404040);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    memcpy((void*) &in, inputs + 28, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x80808080);  
    mac_result = __SEL(in, neg_in);
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    return weightedSum;
}

// ----------------------------------------------------------------------------
// ----------------- MAC computing functions for kernel -----------------------
// ------------------------------- 1W / 5A ------------------------------------
// ----------------------------------------------------------------------------

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 5)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T weightedSum)
{
    uint32_t sum = 0;
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 1);
    wt |= wt << 8;
    wt |= wt << 16;

    memcpy((void*) &in, inputs, sizeof(in));

    // Sign extend 
    if (!std::is_unsigned<Input_T>::value)
        in = (in + 0x70707070) ^ 0x70707070;

    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x08040201);  
    sum = __SEL(in, neg_in);

    memcpy((void*) &in, inputs + 4, sizeof(in));

    // Sign extend 
    if (!std::is_unsigned<Input_T>::value)
        in = (in + 0x70707070) ^ 0x70707070;

    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x80402010);  
    mac_result = __SEL(in, neg_in);
      
    sum = __QADD8(sum, mac_result);

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 5)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t sum = 0;
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 2);

    memcpy((void*) &in, inputs, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x01010101);  
    sum = __SEL(in, neg_in);

    memcpy((void*) &in, inputs + 4, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x02020202);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 8, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x04040404);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 12, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x08080808);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    weightedSum = __SXTAB16(weightedSum, sum);
    weightedSum = __SXTAB16_RORn(weightedSum, sum, 8);

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 5)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t sum = 0;
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 4);

    memcpy((void*) &in, inputs, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x01010101);  
    sum = __SEL(in, neg_in);

    memcpy((void*) &in, inputs + 4, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x02020202);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 8, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x04040404);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 12, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x08080808);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 16, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x10101010);  
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 20, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x20202020);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 24, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x40404040);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 28, sizeof(in));
    neg_in = __SSUB8(0, in);
    __USUB8(0, wt & 0x80808080);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    weightedSum = __SXTAB16(weightedSum, sum);
    weightedSum = __SXTAB16_RORn(weightedSum, sum, 8);

    return weightedSum;
}


template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS >= 8 && NB_ITERATIONS < 16)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum = octoMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS-8>(inputs + 8, weights + 1, weightedSum);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS >= 16 && NB_ITERATIONS < 32)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum = quadquadMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS-16>(inputs + 16, weights + 2, weightedSum);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits <= 8 
         && std::numeric_limits<Input_T>::digits > 4
         && NB_ITERATIONS >= 32)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum = octoquadMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS-32>(inputs + 32, weights + 4, weightedSum);
}


// ----------------------------------------------------------------------------
// ----------------- MAC computing functions for kernel -----------------------
// ------------------------------- 1W / 4A ------------------------------------
// ----------------------------------------------------------------------------

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T monoMac (const Input_T* __restrict inputs,
               const Weight_T* __restrict weights,
               Sum_T weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0].fields.op1)) : (Sum_T)(inputs[0].fields.op1);
    return weightedSum;
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS == 2)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0].fields.op1)) : (Sum_T)(inputs[0].fields.op1);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[0].fields.op0)) : (Sum_T)(inputs[0].fields.op0);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS == 3)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0].fields.op1)) : (Sum_T)(inputs[0].fields.op1);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[0].fields.op0)) : (Sum_T)(inputs[0].fields.op0);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[1].fields.op1)) : (Sum_T)(inputs[1].fields.op1);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0].fields.op1)) : (Sum_T)(inputs[0].fields.op1);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[0].fields.op0)) : (Sum_T)(inputs[0].fields.op0);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[1].fields.op1)) : (Sum_T)(inputs[1].fields.op1);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[1].fields.op0)) : (Sum_T)(inputs[1].fields.op0);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS == 5)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0].fields.op1)) : (Sum_T)(inputs[0].fields.op1);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[0].fields.op0)) : (Sum_T)(inputs[0].fields.op0);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[1].fields.op1)) : (Sum_T)(inputs[1].fields.op1);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[1].fields.op0)) : (Sum_T)(inputs[1].fields.op0);
    weightedSum += (weights[0].fields.op3) ? (Sum_T)(-(inputs[2].fields.op1)) : (Sum_T)(inputs[2].fields.op1);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS == 6)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0].fields.op1)) : (Sum_T)(inputs[0].fields.op1);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[0].fields.op0)) : (Sum_T)(inputs[0].fields.op0);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[1].fields.op1)) : (Sum_T)(inputs[1].fields.op1);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[1].fields.op0)) : (Sum_T)(inputs[1].fields.op0);
    weightedSum += (weights[0].fields.op3) ? (Sum_T)(-(inputs[2].fields.op1)) : (Sum_T)(inputs[2].fields.op1);
    weightedSum += (weights[0].fields.op2) ? (Sum_T)(-(inputs[2].fields.op0)) : (Sum_T)(inputs[2].fields.op0);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS == 7)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum += (weights[0].fields.op7) ? (Sum_T)(-(inputs[0].fields.op1)) : (Sum_T)(inputs[0].fields.op1);
    weightedSum += (weights[0].fields.op6) ? (Sum_T)(-(inputs[0].fields.op0)) : (Sum_T)(inputs[0].fields.op0);
    weightedSum += (weights[0].fields.op5) ? (Sum_T)(-(inputs[1].fields.op1)) : (Sum_T)(inputs[1].fields.op1);
    weightedSum += (weights[0].fields.op4) ? (Sum_T)(-(inputs[1].fields.op0)) : (Sum_T)(inputs[1].fields.op0);
    weightedSum += (weights[0].fields.op3) ? (Sum_T)(-(inputs[2].fields.op1)) : (Sum_T)(inputs[2].fields.op1);
    weightedSum += (weights[0].fields.op2) ? (Sum_T)(-(inputs[2].fields.op0)) : (Sum_T)(inputs[2].fields.op0);
    weightedSum += (weights[0].fields.op1) ? (Sum_T)(-(inputs[3].fields.op1)) : (Sum_T)(inputs[3].fields.op1);
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoMac (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T weightedSum)
{
    uint32_t sum = 0;
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 1);
    wt |= wt << 8;
    wt |= wt << 16;

    memcpy((void*) &in, inputs, sizeof(in));

    neg_in = __SSUB8(0, in & 0x0F0F0F0F);
    __USUB8(0, wt & 0x40100401);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    neg_in = __SSUB8(0, (in >> 4) & 0xF0F0F0F0);
    __USUB8(0, wt & 0x80200802);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T quadquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t sum = 0;
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 4);

    memcpy((void*) &in, inputs, sizeof(in));

    neg_in = __SSUB8(0, in & 0x0F0F0F0F);
    __USUB8(0, wt & 0x01010101);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    neg_in = __SSUB8(0, (in >> 4) & 0x0F0F0F0F);
    __USUB8(0, wt & 0x02020202);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 4, sizeof(in));

    neg_in = __SSUB8(0, in & 0x0F0F0F0F);
    __USUB8(0, wt & 0x04040404);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    neg_in = __SSUB8(0, (in >> 4) & 0x0F0F0F0F);
    __USUB8(0, wt & 0x08080808);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);


    weightedSum = __SXTAB16(weightedSum, sum);
    weightedSum = __SXTAB16_RORn(weightedSum, sum, 8);

    return weightedSum;
}

template<typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
Sum_T octoquadMac (const Input_T* __restrict inputs,
                   const Weight_T* __restrict weights,
                   Sum_T weightedSum)
{
    uint32_t sum = 0;
    uint32_t mac_result = 0;
    uint32_t in;
    uint32_t neg_in;
    uint32_t wt = 0;
    std::memcpy((void*) &wt, weights, 4);

    memcpy((void*) &in, inputs, sizeof(in));

    neg_in = __SSUB8(0, in & 0x0F0F0F0F);
    __USUB8(0, wt & 0x01010101);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    neg_in = __SSUB8(0, (in >> 4) & 0x0F0F0F0F);
    __USUB8(0, wt & 0x02020202);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 4, sizeof(in));

    neg_in = __SSUB8(0, in & 0x0F0F0F0F);
    __USUB8(0, wt & 0x04040404);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    neg_in = __SSUB8(0, (in >> 4) & 0x0F0F0F0F);
    __USUB8(0, wt & 0x08080808);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 8, sizeof(in));

    neg_in = __SSUB8(0, in & 0x0F0F0F0F);
    __USUB8(0, wt & 0x10101010);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    neg_in = __SSUB8(0, (in >> 4) & 0x0F0F0F0F);
    __USUB8(0, wt & 0x20202020);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    memcpy((void*) &in, inputs + 12, sizeof(in));

    neg_in = __SSUB8(0, in & 0x0F0F0F0F);
    __USUB8(0, wt & 0x40404040);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    neg_in = __SSUB8(0, (in >> 4) & 0x0F0F0F0F);
    __USUB8(0, wt & 0x80808080);   
    mac_result = __SEL(in, neg_in);
    sum = __QADD8(sum, mac_result);

    weightedSum = __SXTAB16(weightedSum, sum);
    weightedSum = __SXTAB16_RORn(weightedSum, sum, 8);

    return weightedSum;
}


template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS >= 8 && NB_ITERATIONS < 16)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum = octoMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS-8>(inputs + 4, weights + 1, weightedSum);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS >= 16 && NB_ITERATIONS < 32)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum = quadquadMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS-16>(inputs + 8, weights + 2, weightedSum);
}

template<int NB_ITERATIONS,
         typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(std::numeric_limits<Weight_T>::digits == 1
         && std::numeric_limits<Input_T>::digits == 4
         && NB_ITERATIONS >= 32)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange (const Input_T* __restrict inputs,
                  const Weight_T* __restrict weights,
                  Sum_T& weightedSum)
{
    weightedSum = octoquadMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS-32>(inputs + 16, weights + 4, weightedSum);
}


// ----------------------------------------------------------------------------
// -------------- MAC computing functions for kernel 1W-7A --------------------
// ----------------------------------------------------------------------------

template<typename Input_T,
         typename std::enable_if<(std::numeric_limits<Input_T>::digits == 7)>::type* = nullptr>
__attribute__((always_inline)) static inline
uint32_t quadMacInter(const Input_T* __restrict inputs,
                      const uint32_t weight,
                      uint32_t weightedSum)
{
    uint32_t in;
    memcpy((void*) &in, inputs, sizeof(in));

    // Sign extend 
    if (!std::is_unsigned<Input_T>::value)
        in = (in + 0xC0C0C0C0) ^ 0xC0C0C0C0;

    uint32_t neg_in = __SSUB8(0, in);

    __USUB8(0, weight);  
    uint32_t mac_result = __SEL(in, neg_in);
      
    uint32_t evenA1 = __SXTB16(mac_result);
    uint32_t oddA1  = __SXTB16_RORn(mac_result, 8);

    weightedSum = __SADD16(evenA1, weightedSum);  
    weightedSum = __SADD16(oddA1, weightedSum);  

    return weightedSum;
}

template<typename Input_T,
         typename std::enable_if<(std::numeric_limits<Input_T>::digits == 7)>::type* = nullptr>
__attribute__((always_inline)) static inline
uint32_t quadMacInterV2(const Input_T* __restrict inputs,
                      const uint32_t weight,
                      uint32_t weightedSum)
{
    uint32_t in;
    memcpy((void*) &in, inputs, sizeof(in));

    // Sign extend 
    if (!std::is_unsigned<Input_T>::value)
        in = (in + 0xC0C0C0C0) ^ 0xC0C0C0C0;

    uint32_t neg_in = __SSUB8(0, in);

    __USUB8(0, weight);  
    uint32_t mac_result = __SEL(in, neg_in);
      
    weightedSum = __SXTAB16(weightedSum, mac_result);
    weightedSum = __SXTAB16_RORn(weightedSum, mac_result, 8); 

    return weightedSum;
}


// ----------------------------------------------------------------------------
// -------------- MAC computing functions for kernel 1W-5A --------------------
// ----------------------------------------------------------------------------

template<typename Input_T,
         typename std::enable_if<(std::numeric_limits<Input_T>::digits == 5)>::type* = nullptr>
__attribute__((always_inline)) static inline
uint32_t quadMacInter(const Input_T* __restrict inputs,
                      const uint32_t weight,
                      uint32_t weightedSum)
{
    uint32_t in;
    memcpy((void*) &in, inputs, sizeof(in));

    // Sign extend 
    if (!std::is_unsigned<Input_T>::value)
        in = (in + 0x70707070) ^ 0x70707070;

    uint32_t neg_in = __SSUB8(0, in);

    __USUB8(0, weight);  
    uint32_t mac_result = __SEL(in, neg_in);
      
    weightedSum = __QADD8(weightedSum, mac_result);

    return weightedSum;
}


// ----------------------------------------------------------------------------
// ------------------- MAC computing general functions ------------------------
// ----------------------------------------------------------------------------

template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(NB_ITERATIONS == 0)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange(const Input_T* __restrict /*inputs*/,
                 const Weight_T* __restrict /*weights*/,
                 Sum_T& /*weightedSum*/)
{
    // Nothing should happen
}

template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(NB_ITERATIONS == 1)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange(const Input_T* __restrict inputs,
                 const Weight_T* __restrict weights,
                 Sum_T& weightedSum)
{
    weightedSum = monoMac(inputs, weights, weightedSum);
}

template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(NB_ITERATIONS >= 2 && NB_ITERATIONS < 4 && std::numeric_limits<Weight_T>::digits > 1)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange(const Input_T* __restrict inputs,
                 const Weight_T* __restrict weights,
                 Sum_T& weightedSum)
{
    constexpr unsigned int idxI 
        = (std::numeric_limits<Input_T>::digits > 4) ? 2 : 1;
    constexpr unsigned int idxW 
        = (std::numeric_limits<Weight_T>::digits > 4) ? 2 : 1;

    weightedSum = dualMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS - 2>(inputs + idxI, weights + idxW, weightedSum);
}

template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<NB_ITERATIONS >= 4 
         && (std::numeric_limits<Weight_T>::digits > 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange(const Input_T* __restrict inputs,
                 const Weight_T* __restrict weights,
                 Sum_T& weightedSum)
{
    constexpr unsigned int idxI 
        = (std::numeric_limits<Input_T>::digits > 4) 
          ? 4 : (std::numeric_limits<Input_T>::digits == 4) ? 2 : 1;

    constexpr unsigned int idxW = 4;

    weightedSum = quadMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS - 4>(inputs + idxI, weights + idxW, weightedSum);
}

template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<(NB_ITERATIONS >= 4 && NB_ITERATIONS < 8) 
         && (std::numeric_limits<Weight_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange(const Input_T* __restrict inputs,
                 const Weight_T* __restrict weights,
                 Sum_T& weightedSum)
{
    constexpr unsigned int idxI 
        = (std::numeric_limits<Input_T>::digits > 4) 
          ? 4 : (std::numeric_limits<Input_T>::digits == 4) ? 2 : 1;

    constexpr unsigned int idxW = 2;

    weightedSum = quadMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS - 4>(inputs + idxI, weights + idxW, weightedSum);
}

template<int NB_ITERATIONS, typename Input_T, typename Weight_T, typename Sum_T,
         typename std::enable_if<NB_ITERATIONS >= 8 
         && (std::numeric_limits<Weight_T>::digits == 4)>::type* = nullptr>
__attribute__((always_inline)) static inline
void macsOnRange(const Input_T* __restrict inputs,
                 const Weight_T* __restrict weights,
                 Sum_T& weightedSum)
{
    constexpr unsigned int idxI 
        = (std::numeric_limits<Input_T>::digits > 4) 
          ? 8 : (std::numeric_limits<Input_T>::digits == 4) 
            ? 4 : (std::numeric_limits<Input_T>::digits == 2)
              ? 2 : 1;

    constexpr unsigned int idxW = 4;

    weightedSum = octoMac(inputs, weights, weightedSum);
    macsOnRange<NB_ITERATIONS - 8>(inputs + idxI, weights + idxW, weightedSum);
}


#endif // __N2D2_MAC_FUNCTIONS_HPP__
