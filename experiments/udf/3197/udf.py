
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t9 = constString("1");
String t4 = String_fromdouble(t3);
String t10 = constString("2");
String t7 = String_fromdouble(t6);
String t11 = constString("3");""",
   'args': [("t1", "String"), ("t3", "double"), ("t6", "double")],
   'ret': [("t9", "String"), ("t1", "String"), ("t10", "String"), ("t4", "String"), ("t11", "String"), ("t7", "String")],
   'strings': ['"3"', '"1"', '"2"'],
   'arg_map': ["$EmpId", "$Experience", "$Salary"]
})
    