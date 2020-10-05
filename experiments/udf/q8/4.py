
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(a, constString("AMERICA"));
_Bool t2 = String_equals(b, constString("ECONOMY ANODIZED STEEL"));
_Bool t3 = t1 && t2;""",
   'args': [("a", "String"), ("b", "String")],
   'ret': ("t3", "_Bool"),
   'strings': ['"ECONOMY ANODIZED STEEL"', '"AMERICA"'],
})
    