
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """""",
   'args': [("t1", "int")],
   'ret': ("t1", "int"),
   'arg_map': ["$customerId"]
})
    