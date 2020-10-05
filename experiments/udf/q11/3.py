
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = a > b;""",
   'args': [("a", "double"), ("b", "double")],
   'ret': ("t1", "_Bool"),
})
    