
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1_0 = AString2(constString("totalnum"), constString("totaltime"));
AString t1_1 = AString2(constString("maxtime"), constString("mintime"));
AString t1 = AString_concat(t1_0, t1_1);
AAny t6_0 = AAny2(t2, t3);
AAny t6_1 = AAny2(t4, t5);
AAny t6 = AAny_concat(t6_0, t6_1);
AStringAny t7 = AStringAny_zip(t1, t6);
MStringAny t8 = AStringAny_toMap(t7);""",
   'args': [("t2", "Any"), ("t3", "Any"), ("t4", "Any"), ("t5", "Any")],
   'ret': ("t8", "MStringAny"),
   'strings': ['"maxtime"', '"totaltime"', '"totalnum"', '"mintime"'],
   'arg_map': ["$totalnum", "$totaltime", "$maxtime", "$mintime"]
})
    