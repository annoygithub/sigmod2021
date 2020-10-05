
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t1 = String_concat(first, constString(" "));
String t2 = String_concat(t1, second);""",
   'args': [("first", "String"), ("second", "String")],
   'ret': ("t2", "String"),
   'strings': ['" "'],
})
    