
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString columns = String_split(t1, constString(","));
String t2 = AString_get(columns, 0);
String t3 = AString_get(columns, 1);
String t4 = AString_get(columns, 2);""",
   'args': [("t1", "String")],
   'ret': [("t2", "String"), ("t3", "String"), ("t4", "String")],
   'ints': ['"0"', '"1"', '"2"'], 
   'strings': ['","'],
   'arg_map': ["$_2"]
})
    