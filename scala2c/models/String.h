#ifndef __STRING_MODEL_H__
#define __STRING_MODEL_H__

#include <stddef.h>
#include "typedef.h"

String constString(char *cstr);

String String_concat(String a, String b);

_Bool String_contains(String haystack, String needle);

_Bool String_equals(String s1, String s2);

String String_format_ss(String fmt, String s1, String s2);

String String_fromint(int i);
String String_fromdouble(double i);

int String_indexOf(String str, String substr);
int String_indexOf2(String str, String substr, int start);

int String_length(String s);

String String_lower(String s);

String String_replace(String str, String search, String replace);

AString String_split(String str, String delim);

_Bool String_startsWith(String s1, String s2);
_Bool String_endsWith(String s1, String s2);

String String_stripPrefix(String s, String prefix);
String String_stripSuffix(String s, String suffix);

String String_substring(String str, int s);
String String_substring2(String str, int s, int e);

int String_toint(String str);
double String_todouble(String str);

String String_trim(String str);

_Bool String_forall(String s, _Bool (*func)(char c));

// minimal atomic functions
String _empty_string(int buflen);
void _append_char(String s, char c);

#endif
