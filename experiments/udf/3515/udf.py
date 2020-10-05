
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t2 = String_fromint(key);
String t3 = String_concat(constString("Key: "), t2);
String t4 = String_concat(t3, constString(", Value: "));
String t1 = String_concat(t4, value);""",
   'args': [("key", "int"), ("value", "String")],
   'ret': ("t1", "String"),
   'strings': ['"Key: "', '", Value: "'],
})
    