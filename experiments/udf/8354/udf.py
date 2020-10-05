
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1_0 = AString2(constString("CA"), constString("OR"));
AString t1_1 = AString2(constString("WA"), constString("AK"));
AString t1 = AString_concat(t1_0, t1_1);
_Bool t2 = AString_contains(t1, state);""",
   'args': [("state", "String")],
   'ret': ("t2", "_Bool"),
   'strings': ['"CA"', '"OR"', '"AK"', '"WA"'],
})
    