
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1 = String_split(value, constString("\\\\s+"));""",
   'args': [("value", "String")],
   'ret': ("t1", "AString"),
   'strings': ['"\\s+"'],
})
    