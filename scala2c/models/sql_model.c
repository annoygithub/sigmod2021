#include <stdlib.h>
#include "sql_model.h"
#include "String.h"
#include "Array.h"
#include "Tuple.h"
#include "Any.h"
#include "Array.h"
#include "Map.h"
#include "box.h"

int SQL_constInt(int a){
    return a;
}


String SQL_constString(char* str) {
    return constString(str);
}


double SQL_constDouble(double d) {
    return d;
}


int SQL_add(int a, int b) {
    return a + b;
}


double SQL_addD(double a, double b) {
    return a + b;
}


int SQL_min(int a, int b) {
    return a > b ? b : a;
}


_Bool SQL_and(_Bool a, _Bool b) {
    return a && b;
}


String SQL_concat(String a, String b) {
    return String_concat(a, b);
}


int SQL_div(int a, int b) {
    assume(b != 0);
    return a / b;
}


double SQL_divD(double a, double b) {
    assume(b != 0.0);
    return a / b;
}


_Bool SQL_eq_str(String a, String b) {
    return String_equals(a, b);
}


_Bool SQL_eq_double(double a, double b) {
    return a == b;
}


_Bool SQL_eq(int a, int b) {
    return a == b;
}


String SQL_format_string_ss(String fmt, String s1, String s2) {
    return String_format_ss(fmt, s1, s2);
}


_Bool SQL_le(int a, int b) {
    return a <= b;
}


_Bool SQL_le_double(double a, double b) {
    return a <= b;
}


_Bool SQL_lt(int a, int b) {
    return a < b;
}


_Bool SQL_lt_double(double a, double b) {
    return a < b;
}


int SQL_locate(String substr, String str) {
    return String_indexOf(str, substr);
}


int SQL_locate2(String substr, String str, int start) {
    return String_indexOf2(str, substr, start);
}


int SQL_length(String s) {
    return s->size;
}


int SQL_mod(int a, int b) {
    assume(b != 0);
    return a % b;
}


int SQL_mul(int a, int b) {
    return a * b;
}


double SQL_mulD(double a, double b) {
    return a * b;
}


int SQL_neg(int a) {
    return -a;
}


_Bool SQL_neq(int a, int b) {
    return a != b;
}


String SQL_replace2(String str, String search, String replace){
    return String_replace(str, search, replace);
}


int SQL_sub(int a, int b) {
    return a - b;
}


double SQL_subD(double a, double b) {
    return a - b;
}


String SQL_substring(String str, int startIndex) {
    return String_substring(str, startIndex-1);
}


String SQL_substring2(String str, int startIndex, int len) {
    if (len <= 0) return constString("");
    if (startIndex < 0) startIndex = str->size + startIndex;
    return String_substring2(str, startIndex, startIndex+len);
}


String SQL_trim(String str) {
    return String_trim(str);
}


int SQL_cast_str2int(String str) {
    return String_toint(str);
}


double SQL_cast_str2double(String str) {
    return String_todouble(str);
}


String SQL_cast_int2str(int i) {
    return String_fromint(i);
}


String SQL_cast_double2str(double d) {
    return String_fromdouble(d);
}


long SQL_pow(long a, long b) {
    return math_pow(a, b);
}


String SQL_astring_get(AString astr, int i) {
    return AString_get(astr, i);
}


AString SQL_split(String str, String delim) {
    return String_split(str, delim);
}


int SQL_astring_len(AString astr) {
    return AString_len(astr);
}


_Bool SQL_or(_Bool a, _Bool b) {
    return a || b;
}


AString SQL_if_astr(_Bool b, AString a1, AString a2) {
    return b ? a1 : a2;
}


_Bool SQL_if_bool(_Bool b, _Bool b1, _Bool b2) {
    return b ? b1 : b2;
}


int SQL_if_int(_Bool b, int i1, int i2) {
    return b ? i1 : i2;
}


String SQL_if_str(_Bool b, String s1, String s2) {
    return b ? s1 : s2;
}


double SQL_if_double(_Bool b, double d1, double d2) {
    return b ? d1 : d2;
}


String SQL_lower(String s) {
    return String_lower(s);
}


_Bool SQL_not(_Bool b) {
    return !b;
}


AString SQL_string_array0(int _) {
    return AString0();
}


AString SQL_string_array1(String a) {
    return AString1(a);
}


AString SQL_string_array2(String a, String b) {
    return AString2(a, b);
}


AString SQL_string_array_concat(AString a, AString b){
    return AString_concat(a, b);
}


_Bool SQL_string_array_contains(AString a, String b) {
    return AString_contains(a, b);
}


AString SQL_string_array_intersect(AString a1, AString a2) {
    return AString_intersect(a1, a2);
}


static String _revert_string(String str) {
    String ret = malloc(sizeof(_String));
    ret->size = str->size;
    ret->buf = malloc(sizeof(ret->size));
    for (int i=0; i<ret->size; i ++) {
        ret->buf[i] = str->buf[ret->size-i-1];
    }
    return ret;
}


String SQL_substring_index(String str, String delim, int index) {
    // if (index == 0) {
    //     return constString("");
    // }

    String ret = malloc(sizeof(_String));

    if (index >= 0) {
        int pos = -1 * delim->size;
        while (index >= 0) {
            pos = String_indexOf2(str, delim, pos+delim->size);
            if (pos == -1) return str;
            index --;
        }

        ret->buf = str->buf;
        ret->size = pos;
        return ret;
    } else {
        int start  = 0;
        int pos = -1 * delim->size;
        while (1) {
            pos = String_indexOf2(str, delim, pos+delim->size);
            if (pos == -1) break;
            index ++;
            if (index >= 0) {
                start = String_indexOf2(str, delim, start) + delim->size;
            }
        }
        ret->buf = str->buf + start;
        ret->size = str->size - start;
        return ret;
        // return _revert_string(SQL_substring_index(_revert_string(str), _revert_string(delim), -index-1));
    }
}


AAny SQL_any_array2_any_any(Any a1, Any a2) {
    return AAny2(a1, a2);
}


AStringAny SQL_string_any_array_zip(AString as, AAny aa) {
    return AStringAny_zip(as, aa);
}


MStringAny SQL_map_string_any_concat(MStringAny m1, MStringAny m2) {
    return MStringAny_concat(m1, m2);
}


MStringAny SQL_map_string_any_from_arrays(AString as, AAny aa) {
    return MStringAny_from_arrays(as, aa);
}


MStringAny SQL_map_string_any2_any(String s, Any a) {
    return MStringAny_from_arrays(AString1(s), AAny1(a));
}


MStringAny SQL_map_string_any2_int(String s, int i) {
    return MStringAny_from_arrays(AString1(s), AAny1(toAny(TYPE_INT, boxInteger(i))));
}


AAny SQL_any_array1_any(Any a1) {
    return AAny1(a1);
}


AAny SQL_any_array2_any_int(Any a1, int a2) {
    return AAny2(a1, toAny(TYPE_INT, boxInteger(a2)));
}


AAny SQL_any_array2_int_any(int a1, Any a2) {
    return AAny2(toAny(TYPE_INT, boxInteger(a1)), a2);
}


AAny SQL_any_array_concat(AAny aa1, AAny aa2) {
    return AAny_concat(aa1, aa2);
}


