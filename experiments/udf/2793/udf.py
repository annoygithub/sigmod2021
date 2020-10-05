
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = 1;
String t2 = String_trim(line);
AString t3 = String_split(t2, constString("[/]"));
int t4 = AString_len(t3);
_Bool t5 = t4 > 0;
_Bool t6 = t1 && t5;""",
   'args': [("line", "String")],
   'ret': ("t6", "_Bool"),
   'ints': ['"0"'], 
   'strings': ['"[/]"'],
})
    