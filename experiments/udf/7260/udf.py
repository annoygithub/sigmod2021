
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """int t1 = 11;
String t2 = String_substring2(line, 0, t1);
String id = String_trim(t2);
int t3 = 12;
int t4 = 20;
String t5 = String_substring2(line, t3, t4);
String t6 = String_trim(t5);
double lat = String_todouble(t6);
int t7 = 21;
int t8 = 30;
String t9 = String_substring2(line, t7, t8);
String t10 = String_trim(t9);
double lon = String_todouble(t10);
int t11 = 31;
int t12 = 37;
String t13 = String_substring2(line, t11, t12);
String t14 = String_trim(t13);
double elevation = String_todouble(t14);
int t15 = 38;
int t16 = 40;
String t17 = String_substring2(line, t15, t16);
String state = String_trim(t17);
int t18 = 41;
int t19 = 71;
String t20 = String_substring2(line, t18, t19);
String name = String_trim(t20);""",
   'args': [("line", "String")],
   'ret': [("id", "String"), ("lat", "double"), ("lon", "double"), ("elevation", "double"), ("state", "String"), ("name", "String")],
   'ints': ['"37"', '"41"', '"12"', '"11"', '"38"', '"31"', '"30"', '"20"', '"21"', '"0"', '"71"', '"40"'], 
})
    