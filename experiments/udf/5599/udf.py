
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t5 = String_fromint(t2);
String t6 = String_fromint(t3);
String t7 = String_concat(t1, constString("-"));
String t8 = String_concat(t7, t5);
String t9 = String_concat(t8, constString("-"));
String t4 = String_concat(t9, t6);""",
   'args': [("t1", "String"), ("t2", "int"), ("t3", "int")],
   'ret': ("t4", "String"),
   'strings': ['"-"'],
   'arg_map': ["$letter", "$nr", "$a_flag"]
})
    