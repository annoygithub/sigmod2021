
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = 1;
_Bool t2 = 1;
_Bool t3 = t1 && t2;
AString t4 = AString_intersect(arr1, arr2);
AString t6 = AString0();
AString t7 = t3 ? t4 : t6;""",
   'args': [("arr1", "AString"), ("arr2", "AString")],
   'ret': ("t7", "AString"),
})
    