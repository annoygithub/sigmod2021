
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1 = String_split(love, constString(","));
int t2 = AString_len(t1);""",
   'args': [("love", "String")],
   'ret': ("t2", "int"),
   'strings': ['","'],
})
    