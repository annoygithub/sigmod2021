
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(a, constString("Brand#23"));
_Bool t2 = String_equals(b, constString("MED CASE"));
_Bool t3 = String_equals(b, constString("MED BOX"));
_Bool t4 = t2 || t3;
_Bool t5 = String_equals(b, constString("MED PACK"));
_Bool t6 = t4 || t5;
_Bool t7 = String_equals(b, constString("MED PKG"));
_Bool t8 = t6 || t7;
_Bool t9 = t1 && t8;
_Bool t10 = c >= 10.0;
_Bool t11 = t9 && t10;
double t12 = 10.0 + 10.0;
_Bool t13 = c <= t12;
_Bool t14 = t11 && t13;
_Bool t15 = d >= 1;
_Bool t16 = t14 && t15;
int t17 = 10;
_Bool t18 = d <= t17;
_Bool t19 = t16 && t18;
_Bool t20 = String_equals(e, constString("AIR"));
_Bool t21 = String_equals(e, constString("AIR REG"));
_Bool t22 = t20 || t21;
_Bool t23 = t19 && t22;
_Bool t24 = String_equals(f, constString("DELIVER IN PERSON"));
_Bool t25 = t23 && t24;""",
   'args': [("a", "String"), ("b", "String"), ("c", "double"), ("d", "long"), ("e", "String"), ("f", "String")],
   'ret': ("t25", "_Bool"),
   'ints': ['"1"', '"10"'], 
   'doubles': ['"10.0"'],
   'strings': ['"MED BOX"', '"DELIVER IN PERSON"', '"MED CASE"', '"MED PACK"', '"AIR REG"', '"MED PKG"', '"Brand#23"', '"AIR"'],
})
    