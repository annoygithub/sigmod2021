
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t2 = AString_contains(value, t1);
_Bool t3 = ! t2;""",
   'args': [("value", "AString"), ("t1", "String")],
   'ret': ("t3", "_Bool"),
   'arg_map': ["_2", "_1.$user"]
})
    