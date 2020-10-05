
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(a, constString("Brand#23"));
_Bool t2 = String_equals(b, constString("MED BOX"));
_Bool t3 = t1 && t2;
_Bool t4 = c < d;
_Bool t5 = t3 && t4;""",
   'args': [("a", "String"), ("b", "String"), ("c", "double"), ("d", "double")],
   'ret': ("t5", "_Bool"),
   'strings': ['"MED BOX"', '"Brand#23"'],
})
    