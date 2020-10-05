
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """AString rectangle_dataStringArray = String_split(rectangleData, constString(","));
String rectangle_point1_xInput = AString_get(rectangle_dataStringArray, 0);
String rectangle_point1_yInput = AString_get(rectangle_dataStringArray, 1);
String rectangle_point2_xInput = AString_get(rectangle_dataStringArray, 2);
String rectangle_point2_yInput = AString_get(rectangle_dataStringArray, 3);
String t1 = String_trim(rectangle_point1_xInput);
double rectangle_point1_x = String_todouble(t1);
String t2 = String_trim(rectangle_point2_xInput);
double rectangle_point2_x = String_todouble(t2);
_Bool t3 = rectangle_point1_x < rectangle_point2_x;
double rectangle_lowerBound_x = t3 ? rectangle_point1_x : rectangle_point2_x;
String t4 = String_trim(rectangle_point1_xInput);
double rectangle_point1_x1 = String_todouble(t4);
String t5 = String_trim(rectangle_point2_xInput);
double rectangle_point2_x1 = String_todouble(t5);
_Bool t6 = rectangle_point1_x1 > rectangle_point2_x1;
double rectangle_higherBound_x = t6 ? rectangle_point1_x1 : rectangle_point2_x1;
String t7 = String_trim(rectangle_point1_yInput);
double rectangle_point1_y = String_todouble(t7);
String t8 = String_trim(rectangle_point2_yInput);
double rectangle_point2_y = String_todouble(t8);
_Bool t9 = rectangle_point1_y < rectangle_point2_y;
double rectangle_lowerBound_y = t9 ? rectangle_point1_y : rectangle_point2_y;
String t10 = String_trim(rectangle_point1_yInput);
double rectangle_point1_y1 = String_todouble(t10);
String t11 = String_trim(rectangle_point2_yInput);
double rectangle_point2_y1 = String_todouble(t11);
_Bool t12 = rectangle_point1_y1 > rectangle_point2_y1;
double rectangle_higherBound_y = t12 ? rectangle_point1_y1 : rectangle_point2_y1;
AString pointStringArray = String_split(pointData, constString(","));
String point_xInput = AString_get(pointStringArray, 0);
String point_yInput = AString_get(pointStringArray, 1);
String t13 = String_trim(point_xInput);
double point_x = String_todouble(t13);
String t14 = String_trim(point_xInput);
double point_x1 = String_todouble(t14);
_Bool t15 = point_x < rectangle_lowerBound_x;
_Bool t16 = point_x1 > rectangle_higherBound_x;
_Bool t17 = t15 || t16;
_Bool t18 = 0;
String t19 = String_trim(point_yInput);
double point_y = String_todouble(t19);
String t20 = String_trim(point_yInput);
double point_y1 = String_todouble(t20);
_Bool t21 = point_y > rectangle_lowerBound_y;
_Bool t22 = point_y1 < rectangle_higherBound_y;
_Bool t23 = t21 || t22;
_Bool t24 = 0;
_Bool t25 = 1;
_Bool t26 = t23 ? t24 : t25;
_Bool t27 = t17 ? t18 : t26;""",
   'args': [("rectangleData", "String"), ("pointData", "String")],
   'ret': ("t27", "_Bool"),
   'ints': ['"0"', '"1"', '"2"', '"3"'], 
   'strings': ['","'],
})
    