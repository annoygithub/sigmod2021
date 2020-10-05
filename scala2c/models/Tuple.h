#ifndef __TUPLE_MODEL_H__
#define __TUPLE_MODEL_H__

#include <stddef.h>
#include "typedef.h"

Tuple Tuple_construct(void *_1, void *_2);
Tuple3 Tuple3_construct(void* _1, void* _2, void *_3);

Tuple Tuple_swap(Tuple t);
#endif
