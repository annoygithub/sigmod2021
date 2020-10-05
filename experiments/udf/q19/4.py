
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """double v = 1.0 - b;
double t1 = a * v;""",
   'args': [("a", "double"), ("b", "double")],
   'ret': ("t1", "double"),
   'doubles': ['"1.0"'],
})
    