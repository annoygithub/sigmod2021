#include <stdint.h>
#include <stdlib.h>
#include "sym_input.h"

#define MAX_STRING_SIZE 100
// #define PRINTABLE_STRING
#define MIN_INT -256
#define MAX_INT 256
#define MAX_ASTRING_SIZE 2
#define MAX_AANY_SIZE 2

static size_t nondet_size_t();
static int nondet_int();
static long nondet_long();
static char nondet_char();
static _Bool nodet_bool();
static double nodet_double();

String sym_string() {
    String s = malloc(sizeof(_String));
    s->size = nondet_size_t();
    __CPROVER_assume(s->size <= MAX_STRING_SIZE);
    char *buf = malloc(MAX_STRING_SIZE);
    // for (int i=0; i<MAX_STRING_SIZE; i++) {
    //     buf[i] = nodet_char();
    // }
// #ifdef PRINTABLE_STRING
//     for (int i=0; i<MAX_STRING_SIZE; i++) {
//         char c = nondet_char();
//         __CPROVER_assume(' ' <= c && c <= '~');
//         buf[i] = c;
//     }
// #endif
    s->buf = buf;
    return s;
}


int sym_int() {
    int i = nondet_int();
    __CPROVER_assume(MIN_INT <= i && i<= MAX_INT);
    return i;
}


long sym_long() {
    long i = nondet_long();
    __CPROVER_assume(MIN_INT <= i && i<= MAX_INT);
    return i;
}


_Bool sym_bool() {
    int r = nondet_int();
    __CPROVER_assume(r == 1 || r == 0);
    return (_Bool)r;
}


AString sym_astring() {
    AString as = malloc(sizeof(_AString));
    as->size = nondet_size_t();
    __CPROVER_assume(as->size <= MAX_ASTRING_SIZE);
    String *arr = malloc(MAX_ASTRING_SIZE * sizeof(String));
    as->arr = arr;
    for (int i=0; i<MAX_ASTRING_SIZE; i++) {
        as->arr[i] = sym_string();
    }
    return as;
}


Any sym_any() {
    Any a = malloc(sizeof(_Any));
    size_t i = nondet_size_t() % 3;
    if (i == 0) {
        a->type = TYPE_INT;
        Integer obj = malloc(sizeof(_Integer));
        obj->v = sym_int();
        a->obj = obj;
    } else if (i == 1) {
        a->type = TYPE_STRING;
        a->obj = sym_string();
    } else if (i==2) {
        a->type = TYPE_ASTRING;
        a->obj = sym_astring();
    }
    return a;
}


AAny sym_aany() {
    AAny aa = malloc(sizeof(_AAny));
    aa->size = nondet_size_t();
    __CPROVER_assume(aa->size <= MAX_AANY_SIZE);
    Any *arr = malloc(MAX_AANY_SIZE * sizeof(Any));
    aa->arr = arr;
    for (int i=0; i<MAX_AANY_SIZE; i++) {
        aa->arr[i] = sym_any();
    }
    return aa;
}


double sym_double() {
    double i = nondet_double();
    __CPROVER_assume(MIN_INT <= i && i<= MAX_INT);
    return i;
}
