#include <stdlib.h>
#include "Map.h"
#include "String.h"
#include "Any.h"

_Bool MStringAny_equals(MStringAny l, MStringAny r) {
    if (l->size != r->size) return 0;
    int *mask = malloc(l->size * sizeof(int));
    for (int i=0; i<l->size; i++) mask[i] = 0;
    for (int i=0; i<l->size; i++) {
        int found = 0;
        for (int j=0; j<r->size; j++) {
            if (mask[j] == 1) continue;
            if (String_equals(l->map[i]->_1, r->map[j]->_1) && 
                Any_equals(l->map[i]->_2, r->map[j]->_2)) {
                found = 1;
                mask[j] = 1;
                break;
            }
        }
        if (found == 0) return 0;
    }
    return 1;
}


MStringAny MStringAny_from_arrays(AString as, AAny aa) {
    assume(as->size == aa->size);
    MStringAny ret = malloc(sizeof(_MStringAny));
    ret->size = as->size;
    ret->map = malloc(as->size * sizeof(TStringAny));
    for (int i=0; i<as->size; i++) {
        ret->map[i] = malloc(sizeof(_TStringAny));
        ret->map[i]->_1 = as->arr[i];
        ret->map[i]->_2 = aa->arr[i];
    }
    return ret;
}


MStringAny MStringAny_concat(MStringAny m1, MStringAny m2) {
    MStringAny ret = malloc(sizeof(_MStringAny));
    ret->size = m1->size + m2->size;
    ret->map = malloc(ret->size * sizeof(TStringAny));
    for (int i=0; i<m1->size; i++) {
        ret->map[i] = m1->map[i];
    }
    for (int i=0; i<m2->size; i++) {
        ret->map[m1->size + i] = m2->map[i];
    }
    return ret;
}


