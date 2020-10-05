
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString line = String_split(t1, constString("\\t"));
int dataSource = dataType;
String URL = AString_get(line, 0);
int URL_Time = 1;
_Bool t2 = String_startsWith(filename, constString("lte_cdpi_url"));
_Bool t3 = String_startsWith(filename, constString("3g_cdpi_url"));
_Bool t4 = t2 || t3;
String t5 = AString_get(line, 1);
String t7 = AString_get(line, 1);
long t6 = String_toint(t7);
String t8 = t4 ? t5 : URL;
int t9 = t4 ? URL_Time : t6;
String Id = constString("");
String dt = d;""",
   'args': [("t1", "String"), ("dataType", "int"), ("filename", "String"), ("d", "String")],
   'ret': [("dataSource", "int"), ("t8", "String"), ("Id", "String"), ("t9", "int"), ("dt", "String")],
   'ints': ['"0"', '"1"'], 
   'strings': ['""', '"\t"', '"lte_cdpi_url"', '"3g_cdpi_url"'],
   'arg_map': ["$_1", "$_2", "$_3", "$_4"]
})
    