
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString split = String_split(t, constString("\\\\|"));
String t1 = AString_get(split, 2);
long t2 = String_toint(t1);
String t3 = AString_get(split, 3);
long t4 = String_toint(t3);
String t5 = AString_get(split, 6);""",
   'args': [("t", "String")],
   'ret': [("t2", "long"), ("t4", "long"), ("t5", "String")],
   'ints': ['"2"', '"6"', '"3"'], 
   'strings': ['"\\|"'],
})
    