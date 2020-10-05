
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t4 = String_concat(t1, constString(","));
String t5 = String_concat(t4, t2);
String t6 = String_concat(t5, constString(","));
String pack = String_concat(t6, t3);""",
   'args': [("t1", "String"), ("t2", "String"), ("t3", "String"), ("command", "String")],
   'ret': [("pack", "String"), ("command", "String")],
   'strings': ['","'],
   'arg_map': ["$_1", "$_2", "$_3", "$_4"]
})
    