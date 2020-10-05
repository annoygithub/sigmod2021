
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t2 = String_fromint(id);
String t3 = String_concat(t2, constString(":"));
String t1 = String_concat(t3, name);""",
   'args': [("id", "int"), ("name", "String")],
   'ret': ("t1", "String"),
   'strings': ['":"'],
})
    