
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1 = AString1(rawValue);
String t3 = constString("confCastError");
String t4 = constString("Conformance Error - Null returned by casting conformance rule");""",
   'args': [("errCol", "String"), ("rawValue", "String"), ("code", "String")],
   'ret': [("t3", "String"), ("code", "String"), ("t4", "String"), ("errCol", "String"), ("t1", "AString")],
   'strings': ['"confCastError"', '"Conformance Error - Null returned by casting conformance rule"'],
})
    