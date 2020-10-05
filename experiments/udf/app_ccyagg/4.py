
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../')

import synth

synth.synth({
   'body': """""",
   'args': [("t1", "String")],
   'ret': ("t1", "String"),
   'arg_map': ["$category"]
})
    