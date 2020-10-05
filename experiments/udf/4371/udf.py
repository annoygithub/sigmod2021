
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(each, constString(""));
_Bool t2 = ! t1;""",
   'args': [("each", "String")],
   'ret': ("t2", "_Bool"),
   'strings': ['""'],
})
    