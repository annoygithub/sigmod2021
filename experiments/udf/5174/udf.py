
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t3 = String_fromint(age);
String t4 = String_concat(constString("Pet(name="), name);
String t5 = String_concat(t4, constString(", age="));
String t6 = String_concat(t5, t3);
String t1 = String_concat(t6, constString(")"));
String t2 = String_concat(t1, constString(" is cute"));""",
   'args': [("name", "String"), ("age", "int")],
   'ret': ("t2", "String"),
   'strings': ['"Pet(name="', '", age="', '" is cute"', '")"'],
   'arg_map': ["$name", "$age"]
})
    