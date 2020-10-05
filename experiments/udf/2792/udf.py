
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = 1;
String t2 = String_trim(line);
int t3 = String_length(t2);
_Bool t4 = t3 > 0;
_Bool t5 = t1 && t4;""",
   'args': [("line", "String")],
   'ret': ("t5", "_Bool"),
   'ints': ['"0"'], 
})
    