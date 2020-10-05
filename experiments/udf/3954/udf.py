
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t1 = String_trim(line);
String t2 = String_stripPrefix(t1, constString("|"));
String t3 = String_stripSuffix(t2, constString("|"));""",
   'args': [("line", "String")],
   'ret': ("t3", "String"),
   'strings': ['"|"'],
})
    