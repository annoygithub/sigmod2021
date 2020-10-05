
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """double t1 = x - y;
double t2 = math_pow(t1, 2);""",
   'args': [("x", "double"), ("y", "double")],
   'ret': ("t2", "double"),
   'ints': ['"2"'], 
})
    