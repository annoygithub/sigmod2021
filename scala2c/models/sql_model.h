#ifndef _SQL_MODEL_H_
#define _SQL_MODEL_H_

#include "typedef.h"

int SQL_constInt(int a);
String SQL_constString(char* str);
double SQL_constDouble(double str);

int SQL_add(int a, int b);
double SQL_addD(double a, double b);

int SQL_min(int a, int b);
int SQL_mod(int a, int b);

_Bool SQL_and(_Bool a, _Bool b);

AAny SQL_any_array1_any(Any a1);
AAny SQL_any_array2_any_any(Any a1, Any a2);
AAny SQL_any_array2_any_int(Any a1, int a2);
AAny SQL_any_array2_int_any(int a1, Any a2);
AAny SQL_any_array_concat(AAny aa1, AAny aa2);

String SQL_astring_get(AString astr, int i);
int SQL_astring_len(AString astr);

String SQL_cast_int2str(int i);
String SQL_cast_double2str(double d);
int SQL_cast_str2int(String str);
double SQL_cast_str2double(String str);

String SQL_concat(String a, String b);

int SQL_div(int a, int b);
double SQL_divD(double a, double b);

_Bool SQL_eq_double(double a, double b);
_Bool SQL_eq_str(String a, String b);

_Bool SQL_eq(int a, int b);

String SQL_format_string_ss(String fmt, String s1, String s2);

AString SQL_if_astr(_Bool b, AString a1, AString a2);
_Bool SQL_if_bool(_Bool b, _Bool b1, _Bool b2);
int SQL_if_int(_Bool b, int i1, int i2);
String SQL_if_str(_Bool b, String s1, String s2);
double SQL_if_double(_Bool b, double d1, double d2);

_Bool SQL_le(int a, int b);
_Bool SQL_le_double(double a, double b);

String SQL_lower(String a);

_Bool SQL_lt(int a, int b);
_Bool SQL_lt_double(double a, double b);

int SQL_length(String s);

int SQL_locate(String substr, String str);
int SQL_locate2(String substr, String str, int start);

MStringAny SQL_map_string_any_concat(MStringAny m1, MStringAny m2);
MStringAny SQL_map_string_any_from_arrays(AString as, AAny aa);
MStringAny SQL_map_string_any2_any(String s, Any a);
MStringAny SQL_map_string_any2_int(String s, int i);

int SQL_mul(int a, int b);
double SQL_mulD(double a, double b);

int SQL_neg(int a);

_Bool SQL_neq(int a, int b);
_Bool SQL_not(_Bool b);
_Bool SQL_or(_Bool a, _Bool b);

long SQL_pow(long a, long b);

String SQL_replace2(String str, String search, String replace);

AString SQL_split(String str, String delim);

AStringAny SQL_string_any_array_zip(AString as, AAny aa);

AString SQL_string_array0(int _);
AString SQL_string_array1(String a);
AString SQL_string_array2(String a, String b);
AString SQL_string_array_concat(AString a, AString b);
_Bool SQL_string_array_contains(AString a, String b);
AString SQL_string_array_intersect(AString a1, AString a2);

int SQL_sub(int a, int b);
double SQL_subD(double a, double b);

String SQL_substring(String str, int startIndex);
String SQL_substring2(String str, int startIndex, int endIndex);

String SQL_substring_index(String str, String delim, int index);

String SQL_trim(String str);

#endif
