
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t2 = t1 != 6;
_Bool t4 = t3 != 6;
_Bool t5 = t2 || t4;""",
   'args': [("t1", "int"), ("t3", "int")],
   'ret': ("t5", "_Bool"),
   'ints': ['"6"'], 
   'arg_map': ["$label1", "$label2"]
})
    