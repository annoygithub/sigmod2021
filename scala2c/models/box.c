#include <stdlib.h>
#include <assert.h>
#include "box.h"
#include "String.h"

#ifndef CBMC
#define assume assert
#else
#define assume __CPROVER_assume
#endif

Long boxLong(long l) {
    Long ret = malloc(sizeof(_Long));
    ret->v = l;
    return ret;
}


long unboxLong(Long l) {
    assume(l != NULL);
    return l->v;
}


long math_pow(long a, long b) {
    assume(b >= 0);
    long r = 1;
    for (int i=0; i<b; i++) r *= a;
    return r;
}


double math_powD(double a, long b) {
    assume(b >= 0);
    long r = 1;
    for (int i=0; i<b; i++) r *= a;
    return r;
}


Integer boxInteger(int i) {
    Integer ret = malloc(sizeof(_Integer));
    ret->v = i;
    return ret;
}


Integer Integer_fromString(String str) {
    return boxInteger(String_toint(str));
}


int unboxInteger(Integer i) {
    assume(i != NULL);
    return i->v;
}


int math_signum(double a) {
    if (a == 0.0) return 0;
    else if (a < 0) return -1;
    else return 1;;
}


_Bool char_isDigit(char c) {
    return '0' <= c && c <= '9';
}


Double boxDouble(double v) {
    Double ret = malloc(sizeof(_Double));
    ret->v = v;
    return ret;
}

double unboxDouble(Double v) {
    assume(v != NULL);
    return v->v;
}


int math_mod(int a, int b) {
    assume(b != 0);
    return a % b;
}
