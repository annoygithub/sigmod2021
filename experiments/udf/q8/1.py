
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = String_equals(nation, constString("BRAZIL"));
double t2 = t1 ? volume : 0.0;""",
   'args': [("nation", "String"), ("volume", "double")],
   'ret': ("t2", "double"),
   'doubles': ['"0.0"'],
   'strings': ['"BRAZIL"'],
})
    