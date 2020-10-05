
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1_1 = String_equals(a, constString("Brand#45"));
_Bool t1 = ! t1_1;
_Bool t2 = String_startsWith(b, constString("MEDIUM POLISHED"));
_Bool t3 = ! t2;
_Bool t4 = t1 && t3;
int t5 = 49;
_Bool t6 = c == t5;
int t7 = 14;
_Bool t8 = c == t7;
_Bool t9 = t6 || t8;
int t10 = 23;
_Bool t11 = c == t10;
_Bool t12 = t9 || t11;
int t13 = 45;
_Bool t14 = c == t13;
_Bool t15 = t12 || t14;
int t16 = 19;
_Bool t17 = c == t16;
_Bool t18 = t15 || t17;
_Bool t19 = c == 3;
_Bool t20 = t18 || t19;
int t21 = 36;
_Bool t22 = c == t21;
_Bool t23 = t20 || t22;
_Bool t24 = c == 9;
_Bool t25 = t23 || t24;
_Bool t26 = t4 && t25;
_Bool t27 = String_equals(d, e);
_Bool t28_1 = String_equals(d, e);
_Bool t28 = ! t28_1;
_Bool t29 = t27 || t28;
_Bool t30 = t26 && t29;""",
   'args': [("a", "String"), ("b", "String"), ("c", "long"), ("d", "String"), ("e", "String")],
   'ret': ("t30", "_Bool"),
   'ints': ['"3"', '"19"', '"49"', '"14"', '"45"', '"23"', '"36"', '"9"'], 
   'strings': ['"MEDIUM POLISHED"', '"Brand#45"'],
})
    