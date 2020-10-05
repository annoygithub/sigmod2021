#ifndef __ANY_H__
#define __ANY_H__

#include "typedef.h"

Any toAny(int tpe, void *obj);

_Bool Any_equals(Any a1, Any a2);

#endif
