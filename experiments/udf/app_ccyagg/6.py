
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """int t1 = a + b;""",
   'args': [("a", "int"), ("b", "int")],
   'ret': ("t1", "int"),
})
    