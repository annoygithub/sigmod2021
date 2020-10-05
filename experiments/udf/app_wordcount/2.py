
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t1 = String_lower(x);""",
   'args': [("x", "String")],
   'ret': ("t1", "String"),
})
    