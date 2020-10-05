
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString line = String_split(input, constString(","));
String t1 = AString_get(line, 0);
_Bool t2_1 = String_equals(t1, constString("NA"));
_Bool t2 = ! t2_1;
String t3 = AString_get(line, 0);
long t4 = String_toint(t3);
int dayOfMonth = t2 ? t4 : 0;
String t5 = AString_get(line, 1);
_Bool t6_1 = String_equals(t5, constString("NA"));
_Bool t6 = ! t6_1;
String t7 = AString_get(line, 1);
long t8 = String_toint(t7);
int dayOfWeek = t6 ? t8 : 0;
String t9 = AString_get(line, 2);
_Bool t10_1 = String_equals(t9, constString("NA"));
_Bool t10 = ! t10_1;
String t11 = AString_get(line, 2);
double t12 = String_todouble(t11);
double crsDepTime = t10 ? t12 : 0.0;
String t13 = AString_get(line, 3);
_Bool t14_1 = String_equals(t13, constString("NA"));
_Bool t14 = ! t14_1;
String t15 = AString_get(line, 3);
double t16 = String_todouble(t15);
double crsArrTime = t14 ? t16 : 0.0;
String t17 = AString_get(line, 5);
_Bool t18_1 = String_equals(t17, constString("NA"));
_Bool t18 = ! t18_1;
String t19 = AString_get(line, 5);
double t20 = String_todouble(t19);
double crsElapsedTime = t18 ? t20 : 0.0;
String t21 = AString_get(line, 8);
_Bool t22_1 = String_equals(t21, constString("NA"));
_Bool t22 = ! t22_1;
String t23 = AString_get(line, 8);
long t24 = String_toint(t23);
int arrDelay = t22 ? t24 : 0;
String t25 = AString_get(line, 9);
_Bool t26_1 = String_equals(t25, constString("NA"));
_Bool t26 = ! t26_1;
String t27 = AString_get(line, 9);
long t28 = String_toint(t27);
int depDelay = t26 ? t28 : 0;
int t29 = 30;
_Bool t30 = arrDelay > t29;
int t31 = 30;
_Bool t32 = depDelay > t31;
_Bool t33 = t30 || t32;
int delayFlag = t33 ? 1 : 0;
String t34 = AString_get(line, 4);
String t35 = AString_get(line, 6);
String t36 = AString_get(line, 7);""",
   'args': [("input", "String")],
   'ret': [("dayOfMonth", "int"), ("dayOfWeek", "int"), ("crsDepTime", "double"), ("crsArrTime", "double"), ("t34", "String"), ("crsElapsedTime", "double"), ("t35", "String"), ("t36", "String"), ("arrDelay", "int"), ("depDelay", "int"), ("delayFlag", "int")],
   'ints': ['"6"', '"3"', '"2"', '"5"', '"8"', '"30"', '"4"', '"0"', '"7"', '"9"', '"1"'], 
   'doubles': ['"0.0"'],
   'strings': ['"NA"', '","'],
})
    