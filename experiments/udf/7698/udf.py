
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1 = AString1(constString("totalnum"));
AAny t3 = AAny1(t2);
AStringAny t4 = AStringAny_zip(t1, t3);
MStringAny t5 = AStringAny_toMap(t4);""",
   'args': [("t2", "Any")],
   'ret': ("t5", "MStringAny"),
   'strings': ['"totalnum"'],
   'arg_map': ["$totalnum"]
})
    