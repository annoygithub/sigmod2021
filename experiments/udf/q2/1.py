
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(r_name, constString("EUROPE"));
int t2 = 15;
_Bool t3 = p_size == t2;
_Bool t4 = t1 && t3;
int t5 = String_length(p_type);
int t6 = t5 - 5;
int t7 = String_length(p_type);
String t8 = String_substring2(p_type, t6, t7);
_Bool t9 = String_equals(t8, constString("BRASS"));
_Bool t10 = t4 && t9;""",
   'args': [("p_size", "long"), ("r_name", "String"), ("p_type", "String")],
   'ret': ("t10", "_Bool"),
   'ints': ['"15"', '"5"'], 
   'strings': ['"BRASS"', '"EUROPE"'],
})
    