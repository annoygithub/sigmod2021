
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString t1_0 = AString2(constString("totalnum"), constString("totaltime"));
AString t1_1 = AString2(constString("maxtime"), constString("mintime"));
AString t1_2 = AString1(constString("create_time"));
AString t1_c0 = AString_concat(t1_0, t1_1);
AString t1 = AString_concat(t1_c0, t1_2);
AAny t7_0 = AAny2(t2, t3);
AAny t7_1 = AAny2(t4, t5);
AAny t7_2 = AAny1(t6);
AAny t7_c0 = AAny_concat(t7_0, t7_1);
AAny t7 = AAny_concat(t7_c0, t7_2);
AStringAny t8 = AStringAny_zip(t1, t7);
MStringAny t9 = AStringAny_toMap(t8);""",
   'args': [("t2", "Any"), ("t3", "Any"), ("t4", "Any"), ("t5", "Any"), ("t6", "Any")],
   'ret': ("t9", "MStringAny"),
   'strings': ['"maxtime"', '"totaltime"', '"mintime"', '"totalnum"', '"create_time"'],
   'arg_map': ["$totalnum", "$totaltime", "$maxtime", "$mintime", "$create_time"]
})
    