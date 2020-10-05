
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """Tuple t5 = Tuple_construct(boxLong(t2), t4);
Tuple a = Tuple_swap(t5);
String t6 = a->_1;
long t7 = unboxLong(a->_2);""",
   'args': [("t2", "long"), ("t4", "String")],
   'ret': [("t6", "String"), ("t7", "long")],
   'arg_map': ["$_2.$_1", "$_2.$_2"]
})
    