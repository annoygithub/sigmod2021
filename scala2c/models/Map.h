#ifndef __MAP_H__
#define __MAP_H__

#include "typedef.h"

_Bool MStringAny_equals(MStringAny l, MStringAny r);
MStringAny MStringAny_from_arrays(AString as, AAny aa);
MStringAny MStringAny_concat(MStringAny m1, MStringAny m2);

#endif
