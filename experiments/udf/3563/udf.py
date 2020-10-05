
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """String t9 = String_fromint(t4);
String t10 = String_fromdouble(total);
String t11 = String_concat(t2, constString(" has ordered "));
String t12 = String_concat(t11, t9);
String t13 = String_concat(t12, constString(" units of "));
String t14 = String_concat(t13, t7);
String t15 = String_concat(t14, constString("s, for a total price of "));
String t8 = String_concat(t15, t10);""",
   'args': [("total", "double"), ("t2", "String"), ("t4", "int"), ("t7", "String")],
   'ret': ("t8", "String"),
   'strings': ['"s, for a total price of "', '" has ordered "', '" units of "'],
   'arg_map': ["_2", "_1.$_1.$name", "_1.$_2.$amount", "_1.$_2.$product.$name"]
})
    