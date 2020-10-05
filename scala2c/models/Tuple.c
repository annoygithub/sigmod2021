#include <stdlib.h>
#include "Tuple.h"

Tuple Tuple_construct(void *_1, void *_2) {
    Tuple ret = malloc(sizeof(_Tuple));
    ret->_1 = _1;
    ret->_2 = _2;
    return ret;
}


Tuple3 Tuple3_construct(void *_1, void *_2, void *_3) {
    Tuple3 ret = malloc(sizeof(_Tuple3));
    ret->_1 = _1;
    ret->_2 = _2;
    ret->_3 = _3;
    return ret;
}


Tuple Tuple_swap(Tuple t) {
    return Tuple_construct(t->_2, t->_1);
}


