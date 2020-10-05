
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """int t2 = 103;
long t3 = math_mod(t1, t2);
_Bool t4 = t3 != 0;""",
   'args': [("t1", "long")],
   'ret': ("t4", "_Bool"),
   'ints': ['"0"', '"103"'], 
   'arg_map': ["$id"]
})
    