
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """_Bool t1 = 0;
int orderId = t1 ? unboxInteger(NULL) : t2;
_Bool t3 = 0;
int orderCustomerId = t3 ? unboxInteger(NULL) : t4;
_Bool t5 = 0;
double orderAmount = t5 ? unboxDouble(NULL) : t6;
_Bool t7 = 0;
int customerId = t7 ? unboxInteger(NULL) : t8;
_Bool t9 = 0;
String customerName = t9 ? constString(NULL) : t10;
String t12 = String_fromint(orderId);
String t13 = String_fromint(orderCustomerId);
String t14 = String_fromdouble(orderAmount);
String t15 = String_fromint(customerId);
String t16 = String_concat(t12, constString(","));
String t17 = String_concat(t16, t13);
String t18 = String_concat(t17, constString(","));
String t19 = String_concat(t18, t14);
String t20 = String_concat(t19, constString(","));
String t21 = String_concat(t20, t15);
String t22 = String_concat(t21, constString(","));
String t11 = String_concat(t22, customerName);""",
   'args': [("t2", "int"), ("t4", "int"), ("t6", "double"), ("t8", "int"), ("t10", "String")],
   'ret': ("t11", "String"),
   'strings': ['","'],
   'arg_map': ["$_1", "$_2", "$_3", "$_4", "$_5"]
})
    