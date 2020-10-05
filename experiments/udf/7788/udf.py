
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString keys = String_split(t1, constString("_"));
String adname = AString_get(keys, 0);
String website = AString_get(keys, 1);""",
   'args': [("t1", "String"), ("t2", "int")],
   'ret': [("adname", "String"), ("t2", "int"), ("website", "String")],
   'ints': ['"0"', '"1"'], 
   'strings': ['"_"'],
   'arg_map': ["$_1", "$_2"]
})
    