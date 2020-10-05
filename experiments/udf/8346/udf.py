
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t2 = String_equals(state, t1);
_Bool t4 = discount > t3;
_Bool t5 = t2 && t4;""",
   'args': [("t1", "String"), ("t3", "double"), ("state", "String"), ("discount", "double")],
   'ret': ("t5", "_Bool"),
   'arg_map': ["$_1", "$_2", "$_3", "$_4"]
})
    