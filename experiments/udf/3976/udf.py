
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t2 = String_concat(t1, constString(" -> "));
String t7 = String_concat(constString("("), t3);
String t8 = String_concat(t7, constString(", "));
String t9 = String_concat(t8, t4);
String t5 = String_concat(t9, constString(")"));
String t6 = String_concat(t2, t5);""",
   'args': [("t1", "String"), ("t3", "String"), ("t4", "String")],
   'ret': ("t6", "String"),
   'strings': ['" -> "', '", "', '"("', '")"'],
   'arg_map': ["$_1", "$_2", "$_3"]
})
    