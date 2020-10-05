
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """int t1 = String_indexOf(r_name, constString("Customer"));
_Bool t2 = t1 >= 0;
int t3 = String_indexOf(r_name, constString("Customer"));
int t4 = String_indexOf2(r_name, constString("Complaints"), t3);
_Bool t5 = t4 > 0;
_Bool t6 = t2 && t5;""",
   'args': [("r_name", "String")],
   'ret': ("t6", "_Bool"),
   'ints': ['"0"'], 
   'strings': ['"Customer"', '"Complaints"'],
})
    