#ifndef __TYPEDEF_H__
#define __TYPEDEF_H__

#include <assert.h>
#include <stddef.h>

#define TYPE_int 1
#define TYPE_String 2
#define TYPE_AString 3
#define TYPE_long 4
#define TYPE__Bool 5
#define TYPE_Any 6
#define TYPE_AAny 7
#define TYPE_AStringAny 8
#define TYPE_double 9

// Boxed
typedef struct _Long{
    long v;
} _Long, *Long;

typedef struct _Integer{
    int v;
} _Integer, *Integer;

typedef struct _Double{
    double v;
} _Double, *Double;

// Scalar
typedef struct _String{
    size_t size;
    char *buf;
} _String, *String;

#define TYPE_INT TYPE_int
#define TYPE_STRING TYPE_String
#define TYPE_ASTRING TYPE_AString

typedef struct _Any{
    int type;
    void *obj;
} _Any, *Any;

// Tuple
typedef struct _Tuple{
    void* _1;
    void* _2;
} _Tuple, *Tuple;

typedef struct _Tuple3{
    void* _1;
    void* _2;
    void* _3;
} _Tuple3, *Tuple3;

typedef struct _TStringAny {
    String _1;
    Any _2;
} _TStringAny, *TStringAny;

// Array
typedef struct _Array{
    size_t size;
    void *arr;
} _Array, *Array;

typedef struct _AString{
    size_t size;
    String *arr;
} _AString, *AString;

typedef struct _AAny{
    size_t size;
    Any *arr;
} _AAny, *AAny;

typedef struct _AStringAny {
    size_t size;
    TStringAny *arr;
} _AStringAny, *AStringAny;

// Map
typedef struct _Map {
    size_t size;
    Tuple *map;
} _Map, *Map;

typedef struct _MStringAny{
    size_t size;
    TStringAny *map;
} _MStringAny, *MStringAny;

#ifndef CBMC
#define assume assert
#else
#define assume __CPROVER_assume
#endif

#endif
