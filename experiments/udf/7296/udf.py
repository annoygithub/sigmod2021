
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString fields = String_split(line, constString(","));
String id = AString_get(fields, 0);
String name = AString_get(fields, 1);
String nationCode = AString_get(fields, 2);""",
   'args': [("line", "String")],
   'ret': [("id", "String"), ("name", "String"), ("nationCode", "String")],
   'ints': ['"0"', '"1"', '"2"'], 
   'strings': ['","'],
})
    