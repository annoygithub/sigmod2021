
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t2 = String_forall(t1, char_isDigit);""",
   'args': [("t1", "String")],
   'ret': ("t2", "_Bool"),
   'arg_map': ["$_unit_id"]
})
    