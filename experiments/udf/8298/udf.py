
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString fields = String_split(str, constString("[\\t ]+"));
String t1 = AString_get(fields, 0);
long t2 = String_toint(t1);
String t3 = AString_get(fields, 1);
long t4 = String_toint(t3);
String t5 = AString_get(fields, 2);
double t6 = String_todouble(t5);
String t7 = AString_get(fields, 3);
long t8 = String_toint(t7);""",
   'args': [("str", "String")],
   'ret': [("t2", "int"), ("t4", "int"), ("t6", "double"), ("t8", "long")],
   'ints': ['"0"', '"1"', '"2"', '"3"'], 
   'strings': ['"[\t ]+"'],
})
    