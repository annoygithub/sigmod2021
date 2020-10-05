
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString splits = String_split(line, constString("\\t"));
String t1 = AString_get(splits, 1);
long t2 = String_toint(t1);
String t3 = AString_get(splits, 1);
double t4 = String_todouble(t3);
String t5 = AString_get(splits, 2);
double t6 = String_todouble(t5);""",
   'args': [("line", "String")],
   'ret': [("t2", "int"), ("t4", "double"), ("t6", "double")],
   'ints': ['"1"', '"2"'], 
   'strings': ['"\t"'],
})
    