
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t2 = 1;
_Bool t4_1 = String_equals(t3, constString("null"));
_Bool t4 = ! t4_1;
_Bool t5 = t2 && t4;""",
   'args': [("t1", "String"), ("t3", "String")],
   'ret': ("t5", "_Bool"),
   'strings': ['"null"'],
   'arg_map': ["$createdAt", "$createdAt"]
})
    