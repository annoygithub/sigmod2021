#ifndef __BOX_MODEL_H__
#define __BOX_MODEL_H__

#include <stddef.h>
#include "typedef.h"

Long boxLong(long v);
long unboxLong(Long v);
long math_pow(long a, long b);
double math_powD(double a, long b);
int math_signum(double a);
int math_mod(int a, int b);

_Bool char_isDigit(char c);

Integer boxInteger(int i);
Integer Integer_fromString(String str);
int unboxInteger(Integer i);

Double boxDouble(double v);
double unboxDouble(Double v);

#endif
