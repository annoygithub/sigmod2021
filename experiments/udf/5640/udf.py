
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t2 = 1;
_Bool t4 = 1;
_Bool t5 = t2 && t4;""",
   'args': [("t1", "long"), ("t3", "long")],
   'ret': ("t5", "_Bool"),
   'arg_map': ["$id", "$generated_id"]
})
    