
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t3 = t1 == 0.0;
int t2 = t3 ? -1 : 1;""",
   'args': [("t1", "double")],
   'ret': ("t2", "int"),
   'ints': ['"1"', '"-1"'], 
   'doubles': ['"0.0"'],
   'arg_map': ["${scoresColumnName}"]
})
    