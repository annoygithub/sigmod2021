
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(r_name, constString("EUROPE"));""",
   'args': [("r_name", "String")],
   'ret': ("t1", "_Bool"),
   'strings': ['"EUROPE"'],
})
    