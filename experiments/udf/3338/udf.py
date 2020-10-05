
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """""",
   'args': [("guid", "String"), ("first", "int"), ("second", "int"), ("weight", "double")],
   'ret': [("guid", "String"), ("first", "int"), ("second", "int"), ("weight", "double")],
   'arg_map': ["$_1", "$_2", "$_3", "$_4"]
})
    