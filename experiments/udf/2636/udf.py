
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t2 = String_concat(t1, constString("|"));
String t4 = String_concat(t2, t3);""",
   'args': [("t1", "String"), ("t3", "String")],
   'ret': ("t4", "String"),
   'strings': ['"|"'],
   'arg_map': ["$_1", "$_2"]
})
    