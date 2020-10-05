import os, sys, re, time
from pprint import pprint
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + '/../../cegis/main/')

import os.path

import cegis
import composition
from count_cloc import collect_model_funcs
from trinity2spark import translate

def parse_options(args):
    debug = False
    gen_example = True
    for arg in args:
        if arg == '-d':
                debug = True
        elif arg == '-noex':
            gen_example = False
    # print(f"debug={debug}, gen_example={gen_example}")
    return (debug, gen_example)

def synth(udf):
    start_time = time.time()
    if len(sys.argv) >= 2 and sys.argv[1] in ('pbe', 'comp', 'LOC'):
        if sys.argv[1] == "pbe":
            print(os.getcwd())
            sql = cegis.pbe_from_example_file(udf, "examples")
            return

        if sys.argv[1] == "comp":
            (debug, gen_example) = parse_options(sys.argv[2:])
            sql = composition.synth(udf, debug=debug)

        if sys.argv[1] == "LOC":
            funcs = collect_model_funcs()
            words = re.findall('\w+', udf['body'])
            # pprint(funcs)
            calls = set()
            for w in words:
                if w in funcs:
                    calls.add(w)
                    calls = calls.union(funcs[w][1])
            pprint(calls)
            loc = 1 + len(udf['body'].split('\n')) + sum([funcs[c][0] for c in calls])
            print(loc)
            return
    else:
        (debug, gen_example) = parse_options(sys.argv[1:])
        cegis.init(debug)
        sql = cegis.c_cegis(udf, gen_example)
        if sql is not None:
            sql = str(sql).replace('@param', '@arg')

    print(f"Synthesis time: {time.time()-start_time}")
    if sql is None:
        print("Failed to find an answer!")
    else:
        print("Answer found:")
        if 'arg_map' in udf:
            arg_map = udf['arg_map']
        else:
            arg_map = ["$_1", "$_2", "$_3", "$_4", "$_5", "$_6", "$_7", "$_8", "$_9", "$_10", "$_11", "$_12", "$_13", "$_14", "$_15", "$_16", "$_17", "$_18", "$_19", "$_20"]
        print(translate(str(sql), *arg_map))
