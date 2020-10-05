
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t2 = String_concat(constString("name:"), t1);
String t3 = String_concat(t2, constString("\\tage:"));
String t6 = String_fromint(t4);
String t5 = String_concat(t3, t6);""",
   'args': [("t1", "String"), ("t4", "long")],
   'ret': ("t5", "String"),
   'strings': ['"name:"', '"\tage:"'],
   'arg_map': ["$name", "$age"]
})
    