
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """double t1 = degreesCelcius * 9.0;
double t2 = t1 / 5.0;
double t3 = t2 + 32.0;""",
   'args': [("degreesCelcius", "double")],
   'ret': ("t3", "double"),
   'doubles': ['"9.0"', '"5.0"', '"32.0"'],
})
    