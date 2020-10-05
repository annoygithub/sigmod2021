
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t3 = String_equals(t2, constString(""));
_Bool t4 = ! t3;
String t6 = t4 ? t5 : constString("0");
_Bool t9 = String_equals(t8, constString(""));
_Bool t10 = ! t9;
String t12 = t10 ? t11 : constString("0");
_Bool t16 = String_equals(t15, constString(""));
_Bool t17 = ! t16;
String t19 = t17 ? t18 : constString("0");""",
   'args': [("t1", "String"), ("t2", "String"), ("t5", "String"), ("t7", "String"), ("t8", "String"), ("t11", "String"), ("t13", "String"), ("t14", "String"), ("t15", "String"), ("t18", "String"), ("t20", "String"), ("t21", "String"), ("t22", "String"), ("t23", "String"), ("t24", "String"), ("t25", "String")],
   'ret': [("t1", "String"), ("t6", "String"), ("t7", "String"), ("t12", "String"), ("t13", "String"), ("t14", "String"), ("t19", "String"), ("t20", "String"), ("t21", "String"), ("t22", "String"), ("t23", "String"), ("t24", "String"), ("t25", "String")],
   'strings': ['""', '"0"'],
   'arg_map': ["$_1", "$_2", "$_2", "$_3", "$_4", "$_4", "$_5", "$_6", "$_7", "$_7", "$_8", "$_9", "$_10", "$_11", "$_12", "$_13"]
})
    