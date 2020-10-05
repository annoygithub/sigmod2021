#include <stdarg.h>
#include <stdio.h> 
#include <stdlib.h> 
#include <time.h>
#include <string.h>
#include <assert.h>
#include "rand_input.h"
#include "box.h"

static int array_size = 0;

static void set_seed() {
    static int done = 0;
    if (done == 0) {
        srand(time(0));
        done = 1;
    }
}


int rand_int() {
    set_seed();
    int r = rand();
    r -= RAND_MAX / 2;
    return r % 33;
}


long rand_long() {
    return (long)rand_int();
}


_Bool rand_bool() {
    set_seed();
    return rand() % 2;
}

double rand_double() {
    set_seed();
    return rand_int() / 1.0;
}


String rand_string() {
    set_seed();
    int size = rand() % 32;
    char* buf = malloc(size);
    for (int i=0; i<size; i++) {
        char c = rand() % ('~' - ' ');
        buf[i] = c + ' ';
    }

    String str = malloc(sizeof(_String));
    str->size = size;
    str->buf = buf;
    return str;
}


AString rand_astring() {
    String *arr = malloc(array_size * sizeof(String));
    for (int i=0; i<array_size; i++) {
        arr[i] = rand_string();
    }

    AString astr = malloc(sizeof(_AString));
    astr->size = array_size;
    astr->arr = arr;
    return astr;
}

typedef void* (*RandFunc)();

typedef struct _Type2RandFuncMap {
    int tpe;
    RandFunc func;
} _Type2RandFuncMap;

static Integer rand_integer() {
    return boxInteger(rand_int());
}


Any rand_any() {
    _Type2RandFuncMap type2randfunc[] = {
        {TYPE_INT, (RandFunc)rand_integer},
        {TYPE_STRING, (RandFunc)rand_string},
        {TYPE_ASTRING, (RandFunc)rand_astring}
    };

    set_seed();
    int ntypes = sizeof(type2randfunc) / sizeof(type2randfunc[0]);
    int i = rand() % ntypes;

    return toAny(type2randfunc[i].tpe, type2randfunc[i].func());
}


AAny rand_aany() {
    Any *arr = malloc(array_size * sizeof(Any));
    for (int i=0; i<array_size; i++) {
        arr[i] = rand_any();
    }

    AAny aa = malloc(sizeof(_AAny));
    aa->size = array_size;
    aa->arr = arr;
    return aa;
}


AStringAny rand_astringany() {
    TStringAny *arr = malloc(array_size * sizeof(TStringAny));
    for (int i=0; i< array_size; i++) {
        arr[i] = malloc(sizeof(_TStringAny));
        arr[i]->_1 = rand_string();
        arr[i]->_2 = rand_any();
    }

    AStringAny asa = malloc(sizeof(_AStringAny));
    asa->size = array_size;
    asa->arr = arr;
    return asa;
}


char* hex(const char* buf, int size) {
    char* r = malloc(size*2 + 1);
    r[2*size] = '\0';
    
    unsigned char *hexs="0123456789ABCDEF";
    for (int i=0; i<size; i++) {
        unsigned char c = buf[i];
        // printf("%u\n", c);
        r[2*i] = hexs[c>>4];
        r[2*i+1] = hexs[c%16];
    }

    return r;
}


static int h2i(char h) {
    if ('0' <= h && h <= '9') return h-'0';
    if ('a' <= h && h <= 'f') return h-'a'+10;
    if ('A' <= h && h <= 'Z') return h-'A'+10;
    assert(0);
}


char* unhex(const char* h, int size) {
    int rl = size/2;
    unsigned char *r = malloc(rl+1);
    for (int i=0; i<rl; i++) {
        r[i] = h2i(h[2*i])*16 + h2i(h[2*i+1]);
    }
    r[rl] = '\0';
    return r;
}


char* astr2cstr(AString astr) {
    if (astr->size == 0) return "[]";

    char* buf = malloc(1024*1024);
    buf[0] = '[';
    int pos = 1;
    for (int i=0; i<astr->size; i++) {
        pos += sprintf(buf+pos, "\"%s\",", hex(astr->arr[i]->buf, astr->arr[i]->size));
    }
    buf[pos-1] = ']';
    buf[pos] = '\0';

    return buf;
}


AString cstr2astr(char* str) {
    int len = strlen(str);
    String *arr = malloc(len * sizeof(String));
    int size = 0;

    assert(str[0] == '[');
    int pos = 1;
    int next = pos;
    while (next < len - 1 && str[pos] != ']') {
        while (next < len-1 && str[next] != ',' && str[next] != ']') next ++;

        assert(str[pos] == '"' && str[next-1] == '"');
        arr[size] = malloc(sizeof(_String));
        arr[size]->size = (next-pos-2) / 2;
        arr[size]->buf = unhex(str+pos+1, arr[size]->size * 2);

        size ++;
        if (str[next] == ']') break;
        next ++;
        pos = next;
    }

    AString ret = malloc(sizeof(_AString));
    ret->size = size;
    ret->arr = arr;
    return ret;
}


String dup_string(String s){
    String ret = malloc(sizeof(_String));
    ret->buf = malloc(s->size);
    ret->size = s->size;
    memcpy(ret->buf, s->buf, s->size);
    return ret;
}


AString dup_astring(AString a) {
    AString ret = malloc(sizeof(_AString));
    ret->arr = malloc(sizeof(String) * a->size);
    ret->size = a->size;
    for (int i=0; i<a->size; i++) {
        ret->arr[i] = dup_string(a->arr[i]);
    }
    return ret;
}


Any dup_any(Any a) {
    return toAny(a->type, a->obj);
}


AStringAny dup_astringany(AStringAny asa) {
    AStringAny ret = malloc(sizeof(_AStringAny));
    ret->size = asa->size;
    ret->arr = malloc(asa->size * sizeof(TStringAny));
    for (int i=0; i<asa->size; i++) {
        ret->arr[i] = malloc(sizeof(_TStringAny));
        ret->arr[i]->_1 = dup_string(asa->arr[i]->_1);
        ret->arr[i]->_2 = dup_any(asa->arr[i]->_2);
    }
    return ret;
}


char* any2str(Any a) {
    char* buf = malloc(1024*1024);
    int len = 0;
    if (TYPE_INT == a->type) {
        len = sprintf(buf, "[%d,%d]", a->type, ((Integer)(a->obj))->v);
    } else if (TYPE_STRING == a->type) {
        String s = a->obj;
        len = sprintf(buf, "[%d,\"%s\"]", a->type, hex(s->buf, s->size));
    } else if (TYPE_ASTRING == a->type) {
        len = sprintf(buf, "[%d,%s]", a->type, astr2cstr(a->obj));
    } else {
        assert(0);
    }
    buf[len] = '\0';
    return buf;
}


char* aany2str(AAny aa) {
    if (aa->size == 0) return "[]";

    char* buf = malloc(1024*1024);
    buf[0] = '[';
    int pos = 1;
    for (int i=0; i<aa->size; i++) {
        pos += sprintf(buf+pos, "%s,", any2str(aa->arr[i]));
    }
    buf[pos-1] = ']';
    buf[pos] = '\0';

    return buf;
}


String cstr2string(char *str) {
    assert(str[0] == '"');
    int pos = 1;
    while (str[pos] != '"') pos ++;
    return constString(unhex(str+1, pos-1));
}


Any str2any(char* str) {
    assert(str[0] == '[');
    assert(str[2] == ',');
    int type = atoi(str+1);
    void *obj = NULL;
    if (type == TYPE_INT) {
        obj = boxInteger(atoi(str+3));
    } else if (type == TYPE_STRING) {
        obj = cstr2string(str+3);
    } else if (type == TYPE_ASTRING) {
        obj = cstr2astr(str+3);
    } else {
        assert(0);
    }
    return toAny(type, obj);
}


AAny dup_aany(AAny aa) {
    AAny ret = malloc(sizeof(_AAny));
    ret->size = aa->size;

    ret->arr = malloc(aa->size * sizeof(Any));
    for (int i=0; i<ret->size; i++) {
        ret->arr[i] = dup_any(aa->arr[i]);
    }
    return ret;
}


char* string2cstr(String s) {
    char *buf = malloc(1024*1024);
    int pos = sprintf(buf, "\"%s\"", hex(s->buf, s->size));
    buf[pos] = '\0';
    return buf;
}


char* astringany2str(AStringAny asa) {
    if (asa->size == 0) return "[]";

    char* buf = malloc(1024*1024);
    buf[0] = '[';
    int pos = 1;
    for (int i=0; i<asa->size; i++) {
        pos += sprintf(buf+pos, "[%s,%s],", string2cstr(asa->arr[i]->_1), any2str(asa->arr[i]->_2));
    }
    buf[pos-1] = ']';
    buf[pos] = '\0';

    return buf;
}


char* mstringany2str(MStringAny msa) {
    if (msa->size == 0) return "{}";

    char *buf = malloc(1024*1024);
    buf[0] = '{';
    int pos = 1;
    for (int i=0; i<msa->size; i++) {
        pos += sprintf(buf+pos, "%s: %s,", string2cstr(msa->map[i]->_1), any2str(msa->map[i]->_2));
    }
    buf[pos-1] = '}';
    buf[pos] = '\0';

    return buf;
}


AAny str2aany(char* str) {
    int len = strlen(str);
    Any *arr = malloc(len * sizeof(Any));
    int size = 0;

    assert(str[0] == '[');
    int pos = 1;
    int next = pos;
    int depth = 1;
    while (next < len - 1 && str[pos] != ']') {
        while (next < len-1) {
            if (str[next] == '[') depth ++;
            if (str[next] == ']') depth --;
            if (depth == 0) break;
            if (depth == 1 && str[next] == ',') break;
            next ++;
        }

        assert(str[pos] == '[' && str[next-1] == ']');
        arr[size] = str2any(str+pos);

        size ++;
        if (depth == 0) break;
        next ++;
        pos = next;
    }

    AAny ret = malloc(sizeof(_AAny));
    ret->size = size;
    ret->arr = arr;
    return ret;
}


AStringAny str2astringany(char* str) {
    int len = strlen(str);
    TStringAny *arr = malloc(len * sizeof(TStringAny));
    int size = 0;

    assert(str[0] == '[');
    int pos = 1;
    int next = pos;
    int depth = 1;
    while (next < len - 1 && str[pos] != ']') {
        while (next < len-1) {
            if (str[next] == '[') depth ++;
            if (str[next] == ']') depth --;
            if (depth == 0) break;
            if (depth == 1 && str[next] == ',') break;
            next ++;
        }

        assert(str[pos] == '[' && str[next-1] == ']');
        arr[size] = malloc(sizeof(_TStringAny));
        arr[size]->_1 = cstr2string(str+pos+1);
        while (str[pos] != ',') pos ++;
        arr[size]->_2 = str2any(str+pos+1);

        size ++;
        if (depth == 0) break;
        next ++;
        pos = next;
    }

    AStringAny ret = malloc(sizeof(_AStringAny));
    ret->size = size;
    ret->arr = arr;
    return ret;
}


void rand_inputs(int num, ...) {
    set_seed();
    array_size = rand() % 3;
    va_list valist;
    va_start(valist, num);
    for (int i=0; i<num; i++) {
        int type = va_arg(valist, int);
        if (TYPE_int == type) {
            *(va_arg(valist, int *)) = rand_int();
        } else if (TYPE_String == type) {
            *(va_arg(valist, String *)) = rand_string();
        } else if (TYPE_long == type) {
            *(va_arg(valist, long *)) = rand_long();
        } else if (TYPE__Bool == type) {
            *(va_arg(valist, _Bool *)) = rand_bool();
        } else if (TYPE_AString == type) {
            *(va_arg(valist, AString *)) = rand_astring();
        } else if (TYPE_Any == type) {
            *(va_arg(valist, Any *)) = rand_any();
        } else if (TYPE_AAny == type) {
            *(va_arg(valist, AAny *)) = rand_aany();
        } else if (TYPE_AStringAny == type) {
            *(va_arg(valist, AStringAny *)) = rand_astringany();
        } else if (TYPE_double == type) {
            *(va_arg(valist, double *)) = rand_double();
        } else {
            assert(0);
        }
    }
    va_end(valist);
}


