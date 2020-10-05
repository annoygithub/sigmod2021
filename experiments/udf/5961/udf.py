
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = 0;
int t2 = math_signum(d);
int t3 = t1 ? unboxInteger(NULL) : t2;""",
   'args': [("d", "double")],
   'ret': ("t3", "int"),
})
    