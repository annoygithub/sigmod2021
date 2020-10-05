
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """double v1 = 1.0 - l_discount;
double t1 = l_extendedprice * v1;""",
   'args': [("l_extendedprice", "double"), ("l_discount", "double")],
   'ret': ("t1", "double"),
   'doubles': ['"1.0"'],
})
    