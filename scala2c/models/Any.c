#include <stdlib.h>
#include <string.h>
#include "Any.h"
#include "String.h"
#include "Array.h"

Any toAny(int tpe, void *obj) {
    Any ret = malloc(sizeof(_Any));
    ret->type = tpe;
    ret->obj = obj;
    return ret;
}


_Bool Any_equals(Any a1, Any a2) {
    if (a1->type != a2->type) return 0;
    if (TYPE_INT == a1->type) {
        return ((Integer)(a1->obj))->v == ((Integer)(a2->obj))->v;
    } else if (TYPE_STRING == a1->type) {
        return String_equals(a1->obj, a2->obj);
    } else if (TYPE_ASTRING == a1->type) {
        return AString_equals(a1->obj, a2->obj);
    } else {
        assert(0);
    }
}


