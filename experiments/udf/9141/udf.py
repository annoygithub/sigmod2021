
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t2 = String_concat(constString("code: "), t1);
String t3 = String_concat(t2, constString(",name:"));
String t5 = String_concat(t3, t4);""",
   'args': [("t1", "String"), ("t4", "String")],
   'ret': ("t5", "String"),
   'strings': ['"code: "', '",name:"'],
   'arg_map': ["$_1", "$_2"]
})
    