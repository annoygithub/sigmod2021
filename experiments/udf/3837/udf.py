
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t1 = String_replace(string, constString("("), constString(""));
String t2 = String_replace(t1, constString(")"), constString(""));""",
   'args': [("string", "String")],
   'ret': ("t2", "String"),
   'strings': ['""', '"("', '")"'],
})
    