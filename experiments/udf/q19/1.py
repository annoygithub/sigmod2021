
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(a, constString("Brand#12"));
_Bool t2 = String_equals(b, constString("SM CASE"));
_Bool t3 = String_equals(b, constString("SM BOX"));
_Bool t4 = t2 || t3;
_Bool t5 = String_equals(b, constString("SM PACK"));
_Bool t6 = t4 || t5;
_Bool t7 = String_equals(b, constString("SM PKG"));
_Bool t8 = t6 || t7;
_Bool t9 = t1 && t8;
_Bool t10 = c >= 1.0;
_Bool t11 = t9 && t10;
double t12 = 1.0 + 10.0;
_Bool t13 = c <= t12;
_Bool t14 = t11 && t13;
_Bool t15 = d >= 1;
_Bool t16 = t14 && t15;
_Bool t17 = d <= 5;
_Bool t18 = t16 && t17;
_Bool t19 = String_equals(e, constString("AIR"));
_Bool t20 = String_equals(e, constString("AIR REG"));
_Bool t21 = t19 || t20;
_Bool t22 = t18 && t21;
_Bool t23 = String_equals(f, constString("DELIVER IN PERSON"));
_Bool t24 = t22 && t23;""",
   'args': [("a", "String"), ("b", "String"), ("c", "double"), ("d", "long"), ("e", "String"), ("f", "String")],
   'ret': ("t24", "_Bool"),
   'ints': ['"1"', '"5"'], 
   'doubles': ['"1.0"', '"10.0"'],
   'strings': ['"SM PKG"', '"Brand#12"', '"DELIVER IN PERSON"', '"SM PACK"', '"SM BOX"', '"AIR REG"', '"SM CASE"', '"AIR"'],
})
    