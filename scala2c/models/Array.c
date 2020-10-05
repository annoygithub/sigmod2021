#include <stdlib.h>
#include "Array.h"
#include "String.h"
#include "Any.h"
#include "Tuple.h"
#include "rand_input.h"

String AString_get(AString astr, int i) {
    assume(i>=0 && i < astr->size);
    return astr->arr[i];
}


int AString_len(AString astr) {
    return astr->size;
}


_Bool AString_equals(AString a, AString b) {
    if (a->size != b->size) return 0;
    for (int i=0; i<a->size; i++) {
        if (! String_equals(a->arr[i], b->arr[i])) return 0;
    }
    return 1;
}


AString AString0() {
    AString astr = malloc(sizeof(_AString));
    astr->size = 0;
    return astr;
}


AString AString1(String s1)
{
    AString astr = malloc(sizeof(_AString));
    astr->size = 1;
    astr->arr = malloc(sizeof(String));
    astr->arr[0] = s1;
    return astr;
}


AString AString2(String s1, String s2)
{
    AString astr = malloc(sizeof(_AString));
    astr->size = 2;
    astr->arr = malloc(2*sizeof(_String));
    astr->arr[0] = s1;
    astr->arr[1] = s2;
    return astr;
}


AString AString4(String s1, String s2, String s3, String s4) {
    AString astr = malloc(sizeof(_AString));
    astr->size = 4;
    astr->arr = malloc(4*sizeof(String));
    astr->arr[0] = s1;
    astr->arr[1] = s2;
    astr->arr[2] = s3;
    astr->arr[3] = s4;
    return astr;
}


_Bool AString_contains(AString astr, String s) {
    for (int i=0; i<astr->size; i++) {
        if (String_equals(astr->arr[i], s)) return 1;
    }
    return 0;
}


AString AString_concat(AString a, AString b) {
    AString r = malloc(sizeof(_AString));
    r->size = a->size + b->size;
    r->arr = malloc(r->size * sizeof(String));
    for (int i=0; i<a->size; i++) {
        r->arr[i] = a->arr[i];
    }
    for (int i=0; i<b->size; i++) {
        r->arr[a->size+i] = b->arr[i];
    }
    return r;
}


AAny AAny1(Any a) {
    AAny aa = malloc(sizeof(_AAny));
    aa->size = 1;
    aa->arr = malloc(sizeof(Any));
    aa->arr[0] = a;
    return aa;
}


AAny AAny2(Any a1, Any a2) {
    AAny aa = malloc(sizeof(_AAny));
    aa->size = 2;
    aa->arr = malloc(2*sizeof(Any));
    aa->arr[0] = a1;
    aa->arr[1] = a2;
    return aa;
}


_Bool AAny_equals(AAny aa1, AAny aa2) {
    if (aa1->size != aa2->size) return 0;
    for (int i=0; i<aa1->size; i++) {
        if (! Any_equals(aa1->arr[i], aa2->arr[i])) return 0;
    }
    return 1;
}


AStringAny AStringAny_zip(AString a1, AAny a2) {
    assume(a1->size == a2->size);
    AStringAny ret = malloc(sizeof(_AStringAny));
    ret->size = a1->size;
    ret->arr = malloc(a1->size * sizeof(TStringAny));
    for (int i=0; i<a1->size; i++) {
        ret->arr[i] = (TStringAny)Tuple_construct(a1->arr[i], a2->arr[i]);
    }
    return ret;
}


_Bool AStringAny_equals(AStringAny a1, AStringAny a2) {
    if (a1->size != a2->size) return 0;
    for (int i=0; i<a1->size; i++) {
        if (! String_equals(a1->arr[i]->_1, a2->arr[i]->_1)) return 0;
        if (! Any_equals(a1->arr[i]->_2, a2->arr[i]->_2)) return 0;
    }
    return 1;
}


MStringAny AStringAny_toMap(AStringAny asa) {
    MStringAny ret = malloc(sizeof(_MStringAny));
    ret->size = asa->size;
    ret->map = malloc(asa->size * sizeof(TStringAny));
    for (int i=0; i<asa->size; i++) {
        ret->map[i] = malloc(sizeof(_TStringAny));
        ret->map[i]->_1 = dup_string(asa->arr[i]->_1);
        ret->map[i]->_2 = dup_any(asa->arr[i]->_2);
    }
    return ret;
}


AString AString_intersect(AString a1, AString a2) {
    AString astr = malloc(sizeof(_AString));
    String *buf = malloc(sizeof(String) * a1->size);
    size_t size = 0;
    for (int i=0; i<a1->size; i++) {
        for (int j=0; j<a2->size; j++) {
            if (String_equals(a1->arr[i], a2->arr[j])) {
                int found = 0;
                for (int k=0; k<size; k++) {
                    if (String_equals(a1->arr[i], buf[k])) {
                        found = 1;
                        break;
                    }
                }
                if (! found) {
                    buf[size] = a1->arr[i];
                    size ++;
                }
                break;
            }
        }
    }
    astr->arr = buf;
    astr->size = size;
    return astr;
}


AAny AAny_concat(AAny a, AAny b) {
    AAny r = malloc(sizeof(_AAny));
    r->size = a->size + b->size;
    r->arr = malloc(r->size * sizeof(Any));
    for (int i=0; i<a->size; i++) {
        r->arr[i] = a->arr[i];
    }
    for (int i=0; i<b->size; i++) {
        r->arr[a->size+i] = b->arr[i];
    }
    return r;
}


AString AString_map(AString astr, String (*func)(String s)) {
    AString ret = malloc(sizeof(_AString));
    ret->size = astr->size;
    ret->arr = malloc(astr->size*sizeof(_String));
    for (int i=0; i<astr->size; i++) {
        ret->arr[i] = func(astr->arr[i]);
    }
    return ret;
}
