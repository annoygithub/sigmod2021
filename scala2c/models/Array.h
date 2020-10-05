#ifndef __ARRAY_H__
#define __ARRAY_H__

#include "typedef.h"

AString AString0();
AString AString1(String s1);
AString AString2(String s1, String s2);
AString AString4(String s1, String s2, String s3, String s4);
AString AString_concat(AString a, AString b);
_Bool AString_contains(AString astr, String s);
_Bool AString_equals(AString a, AString b);
String AString_get(AString astr, int i);
AString AString_intersect(AString a1, AString a2);
int AString_len(AString astr);
AString AString_map(AString astr, String (*func)(String s));

AAny AAny1(Any a1);
AAny AAny2(Any a1, Any a2);
AAny AAny_concat(AAny aa1, AAny aa2);
_Bool AAny_equals(AAny aa1, AAny aa2);

AStringAny AStringAny_zip(AString a1, AAny a2);
_Bool AStringAny_equals(AStringAny a1, AStringAny a2);
MStringAny AStringAny_toMap(AStringAny asa);

#endif
