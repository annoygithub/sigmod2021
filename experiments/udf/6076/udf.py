
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t5 = t2 == -1;
_Bool t6 = t4 == -1;
_Bool t8 = t5 && t6;""",
   'args': [("t2", "long"), ("t4", "long")],
   'ret': ("t8", "_Bool"),
   'ints': ['"-1"'], 
   'arg_map': ["$in.$_1", "$in.$_2"]
})
    