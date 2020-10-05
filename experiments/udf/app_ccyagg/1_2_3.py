
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1 = String_split(r, constString(","));
AString fields = AString_map(t1, String_trim);
String t2 = AString_get(fields, 0);
String t3 = AString_get(fields, 1);
long t4 = String_toint(t3);
String t5 = AString_get(fields, 2);
String t6 = AString_get(fields, 3);
String t7 = AString_get(fields, 4);
String t8 = AString_get(fields, 5);
String t9 = AString_get(fields, 6);
long t10 = String_toint(t9);""",
   'args': [("r", "String")],
   'ret': [("t2", "String"), ("t4", "int"), ("t5", "String"), ("t6", "String"), ("t7", "String"), ("t8", "String"), ("t10", "int")],
   'ints': ['"6"', '"3"', '"2"', '"5"', '"4"', '"0"', '"1"'], 
   'strings': ['","'],
})
    