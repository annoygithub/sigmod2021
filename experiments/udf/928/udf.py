
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = 0;
int t3 = t1 ? -99 : t2;
_Bool t4 = 0;
int t6 = t4 ? 0 : t5;""",
   'args': [("t2", "long"), ("t5", "long")],
   'ret': [("t3", "int"), ("t6", "int")],
   'ints': ['"0"', '"-99"'], 
   'arg_map': ["$_1", "$_2"]
})
    