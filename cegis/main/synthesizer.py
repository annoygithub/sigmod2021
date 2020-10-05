import base64
import time
import hashlib
from jinja2 import Template

from tyrell.spec import parse
from tyrell.enumerator import SmtEnumerator
from tyrell.interpreter import PostOrderInterpreter
from tyrell.decider import Example, ExampleConstraintDecider
from tyrell.synthesizer import Synthesizer
from tyrell.dsl import Builder
from tyrell.logger import get_logger

logger = get_logger('SQLSynth')

lowercases="abcdefghijklmnopqrstuvwxyz"
uppercases="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

tolower=str.maketrans(uppercases, lowercases)

class Interpreter(PostOrderInterpreter):
    def eval_ConstString(self, v):
        return v

    def eval_constString(sefl, node, args):
        return args[0]

    def eval_ConstBool(self, v):
        return v == "True"

    def eval_constBool(self, node, args):
        return args[0]

    def eval_ConstInt(self, v):
        return int(v)

    def eval_constInt(self, node, args):
        return int(args[0])

    def eval_ConstDouble(self, v):
        return float(v)

    def eval_constDouble(self, node, args):
        return float(args[0])

    def eval_ConstAString(self, v):
        return eval(v)

    def eval_constAString(self, node, args):
        return args[0]

    def eval_ConstAAny(self, v):
        return eval(v)

    def eval_constAAny(self, node, args):
        return args[0]

    def eval_ConstAStringAny(self, v):
        return eval(v)

    def eval_constAStringAny(self, node, args):
        return args[0]

    def eval_ConstMStringAny(self, v):
        return eval(v)

    def eval_constMStringAny(self, node, args):
        return args[0]

    def eval_row(self, node, args):
        return list(args)

    def eval_abs(self, node, args):
        return abs(args[0])

    def eval_add(self, node, args):
        return args[0] + args[1]

    def eval_addD(self, node, args):
        return args[0] + args[1]
    
    def eval_and(self, node, args):
        return args[0] and args[1]

    def eval_any_array1_any(self, node, args):
        return [args[0]]

    def eval_any_array1_int(self, node, args):
        return [[1, args[0]]]

    def eval_any_array1_string(self, node, args):
        return [[2, args[0]]]

    def eval_any_array1_astring(self, node, args):
        return [[3, args[0]]]

    def eval_any_array2_any_any(self, node, args):
        return [args[0], args[1]]

    def eval_any_array2_any_int(self, node, args):
        return [args[0], [1, args[1]]]

    def eval_any_array2_any_string(self, node, args):
        return [args[0], [2, args[1]]]
    
    def eval_any_array2_any_astring(self, node, args):
        return [args[0], [3, args[1]]]

    def eval_any_array2_int_any(self, node, args):
        return [[1, args[0]], args[1]]

    def eval_any_array2_int_int(self, node, args):
        return [[1, args[0]], [1, args[1]]]

    def eval_any_array2_int_string(self, node, args):
        return [[1, args[0]], [2, args[1]]]
    
    def eval_any_array2_int_astring(self, node, args):
        return [[1, args[0]], [3, args[1]]]

    def eval_any_array2_string_any(self, node, args):
        return [[2, args[0]], args[1]]

    def eval_any_array2_string_int(self, node, args):
        return [[2, args[0]], [1, args[1]]]

    def eval_any_array2_string_string(self, node, args):
        return [[2, args[0]], [2, args[1]]]
    
    def eval_any_array2_string_astring(self, node, args):
        return [[2, args[0]], [3, args[1]]]

    def eval_any_array2_astring_any(self, node, args):
        return [[3, args[0]], args[1]]

    def eval_any_array2_astring_int(self, node, args):
        return [[3, args[0]], [1, args[1]]]

    def eval_any_array2_astring_string(self, node, args):
        return [[3, args[0]], [2, args[1]]]
    
    def eval_any_array2_astring_astring(self, node, args):
        return [[3, args[0]], [3, args[1]]]

    def eval_any_array_concat(self, node, args):
        return args[0] + args[1]

    def eval_ascii(self, node, args):
        if not args[0]:
            return None
        return ord(args[0][0])
    
    def eval_astring_get(self, node, args):
        if args[1] < 0 or args[1] >= len(args[0]):
            return None
        return args[0][args[1]]

    def eval_astring_len(self, node, args):
        return len(args[0])

    def eval_cast_astring2any(self, node, args):
        return [3, args[0]]

    def eval_cast_int2any(self, node, args):
        return [1, args[0]]

    def eval_cast_int2str(self, node, args):
        return str(args[0])

    def eval_cast_double2str(self, node, args):
        return "%.3f" % args[0]

    def eval_cast_str2any(self, node, args):
        return [2, args[0]]
        
    def eval_cast_str2int(self, node, args):
        try:
            return int(args[0])
        except:
            return None

    def eval_cast_str2double(self, node, args):
        try:
            return float(args[0])
        except:
            return None

    def eval_concat(self, node, args):
        return args[0] + args[1]
    
    def eval_concat_ws(self, node, args):
        return args[1] + args[0] + args[2]

    def eval_div(self, node, args):
        if args[1] == 0:
            return None
        if args[0] < 0 and args[1] < 0:
            return (-args[0]) // (-args[1])
        if args[0] < 0:
            return -( (-args[0]) // args[1])
        if args[1] < 0:
            return - (args[0] // (-args[1]))
        return args[0] // args[1]

    def eval_divD(self, node, args):
        if args[1] == 0.0:
            return None
        return args[0] / args[1]

    def eval_eq(self, node, args):
        return args[0] == args[1]
    
    def eval_eq_str(self, node, args):
        return args[0] == args[1]

    def eval_eq_double(self, node, args):
        return args[0] == args[1]

    def eval_format_string_ss(sefl, node, args):
        try:
            return args[0] % (args[1], args[2])
        except:
            return None

    def eval_if_astr(self, node, args):
        return args[1] if args[0] else args[2]

    def eval_if_bool(self, node, args):
        return args[1] if args[0] else args[2]

    def eval_if_int(self, node, args):
        return args[1] if args[0] else args[2]

    def eval_if_str(self, node, args):
        return args[1] if args[0] else args[2]

    def eval_if_double(self, node, args):
        return args[1] if args[0] else args[2]

    # def eval_ge(self, node, args):
    #     return args[0] >= args[1]

    # def eval_gt(self, node, args):
    #     return args[0] > args[1]

    def eval_initcap(self, node, args):
        return " ".join([s.capitalize() for s in args[0].split(" ")])

    def eval_int(self, node, args):
        try:
            return int(args[0])
        except:
            return None

    def eval_int2char(self, node, args):
        return chr(args[0] % 256)

    def eval_le(self, node, args):
        return args[0] <= args[1]

    def eval_le_double(self, node, args):
        return args[0] <= args[1]

    def eval_length(self, node, args):
        return len(args[0])

    # def eval_levenshtein(self, node, args):
    #     return jellyfish.levenshtein_distance(args[0], args[1])

    def eval_locate(self, node, args):
        return args[1].find(args[0])

    def eval_locate2(self, node, args):
        start = args[2] if args[2] >= 0 else 0
        return args[1].find(args[0], start)

    def eval_lower(self, node, args):
        return args[0].translate(tolower)

    def eval_lpad(self, node, args):
        if args[1] <= len(args[0]):
            return args[0][:args[1]]
        return (" " * args[1] + args[0])[-args[1]:]

    def eval_lpad2(self, node, args):
        if args[1] <= len(args[0]):
            return args[0][:args[1]]
        return (args[2] * args[1] + args[0])[-args[1]:]

    def eval_lt(self, node, args):
        return args[0] < args[1]

    def eval_lt_double(self, node, args):
        return args[0] < args[1]
    
    def eval_ltrim(self, node, args):
        return args[0].lstrip()

    def eval_ltrim2(self, node, args):
        return args[0].lstrip(args[1])

    def eval_map_string_any2_any(self, node, args):
        return {args[0] : args[1]}

    def eval_map_string_any2_int(self, node, args):
        return {args[0] : [1, args[1]]}

    def eval_map_string_any2_string(self, node, args):
        return {args[0] : [2, args[1]]}

    def eval_map_string_any2_astring(self, node, args):
        return {args[0] : [3, args[1]]}

    def eval_map_string_any_concat(self, node, args):
        return {**args[0], **args[1]}

    def eval_map_string_any_from_arrays(self, node, args):
        if len(args[0]) != len(args[1]):
            return None
        return {a: b for a, b in zip(args[0], args[1])}

    def eval_map_string_any_keys(self, node, args):
        return list(args[0].keys())

    def eval_map_string_any_values(self, node, args):
        return list(args[0].values())

    def eval_max(self, node, args):
        return max(args[0],args[1])

    def eval_min(self, node, args):
        return min(args[0],args[1])

    def eval_mod(self, node, args):
        if args[1] == 0:
            return None
        if args[0] < 0:
            mod = args[0] % args[1]
            return mod - args[1] if mod != 0 else 0
        return args[0] % args[1]

    def eval_mul(self, node, args):
        return args[0] * args[1]

    def eval_mulD(self, node, args):
        return args[0] * args[1]

    def eval_neg(self, node, args):
        return -args[0]

    def eval_neq(self, node, args):
        return args[0] != args[1]

    def eval_not(self, node, args):
        return not args[0]

    def eval_or(self, node, args):
        return args[0] or args[1]

    def eval_overlay(self, node, args):
        return args[0][:args[2]-1] + args[1] + args[0][args[2]+len(args[1])-1:]

    def eval_overlay2(self, node, args):
        return args[0][:args[2]-1] + args[1] + args[0][args[2]+args[3]-1:]

    def eval_pow(self, node, args):
        if args[1] < 0 or args[1] > 100:
            return None
        return int(args[0] ** args[1])

    def eval_repeat(self, node, args):
        return args[0] * args[1]

    def eval_replace(self, node, args):
        return args[0].replace(args[1], "")

    def eval_replace2(self, node, args):
        if args[0] == "":
            return ""
        if args[1] == "":
            return args[0]
        return args[0].replace(args[1], args[2])

    def eval_reverse(self, node, args):
        return args[0][::-1]

    def eval_right(self, node, args):
        if args[1] <= 0:
            return ""
        return args[0][-args[1]:]

    def eval_rpad(self, node, args):
        return (args[0] + " " * args[1])[:args[1]]

    def eval_rpad2(self, node, args):
        return (args[0] + args[2] * args[1])[:args[1]]
    
    def eval_rtrim(self, node, args):
        return args[0].rstrip()

    def eval_rtrim2(self, node, args):
        return args[0].rstrip(args[1])

    # def eval_soundex(self, node, args):
    #     return jellyfish.soundex(args[0])

    def eval_split(self, node, args):
        if len(args[1]) == 0:
            return None
        return args[0].split(args[1])

    def eval_string_any_array_zip(self, node, args):
        if len(args[0]) != len(args[1]):
            return None
        return [[_1, _2] for _1, _2 in zip(args[0], args[1])]
    
    def eval_string_array0(self, node, args):
        return []

    def eval_string_array1(self, node, args):
        return [args[0]]

    def eval_string_array2(self, node, args):
        return [args[0], args[1]]

    def eval_string_array_concat(self, node, args):
        return args[0] + args[1]

    def eval_string_array_contains(self, node, args):
        return args[1] in args[0]

    def eval_string_array_intersect(self, node, args):
        r = []
        for a in args[0]:
            for b in args[1]:
                if a == b:
                    if a not in r:
                        r.append(a)
                    break
        return r


    def eval_string_array_join(self, node, args):
        return args[1].join(args[0])

    def eval_sub(self, node, args):
        return args[0] - args[1]
    
    def eval_subD(self, node, args):
        return args[0] - args[1]

    def eval_substring(self, node, args):
        l = args[1] - 1 if args[1] > 0 else args[1]
        return args[0][l:]
    
    def eval_substring2(self, node, args):
        if args[2] <= 0:
            return ""
        l = args[1] if args[1] >= 0 else len(args[0]) + args[1]
        e = l + args[2]
        if l < 0 or l > len(args[0]) or e < 0 or e > len(args[0]):
            return None
        return args[0][l:e]

    def eval_substring_index(self, node, args):
        if not args[1]:
            return None
        subs = args[0].split(args[1])
        if args[2] >= 0:
            subs = subs[:args[2]+1]
        else:
            subs = subs[args[2]:]
        return args[1].join(subs)

    def eval_translate(self, node, args):
        if len(args[1]) != len(args[2]):
            return None
        return args[0].translate(str.maketrans(args[1], args[2]))

    def eval_trim(self, node, args):
        return args[0].strip("\t ")

    def eval_trim2(self, node, args):
        return args[1].strip(args[0])

    def eval_upper(self, node, args):
        return args[0].upper()

    def apply_strlen(self, v):
        return len(v)

    def apply_True(self, v):
        return v

    def apply_size(self, v):
        return len(v)

    def apply_is_positive(self, v):
        return v > 0

    def apply_is_zero(self, v):
        return v == 0
    
    def apply_value(self, v):
        return v

g_enumerator_cache = {}

class SQLSynth:
    def __init__(self, spec_file, program_type=None, const_string=None, const_int=None, const_double=None, columns=None):
        with open(spec_file) as f:
            template = Template(f.read())
            column_type = None
            if columns:
                column_type = ", ".join([f"{t} c{i+1}" for (i, t) in enumerate(columns)])
            spec = template.render(
                program_type=program_type,
                const_string=const_string,
                const_int=const_int,
                const_double=const_double,
                columns=column_type)
            # print(spec)
            self.spectext = spec
            self.spec = parse(spec)
            self.decider = None

    def eval(self, prog, input):
        p = Builder(self.spec).from_sexp_string(prog)
        return Interpreter().eval(p, input)

    def set_examples(self, examples):
        logger.debug("creating decider in set_examples()")
        self.decider = ExampleConstraintDecider(
                spec=self.spec,  # spec is needed for this decider
                interpreter=Interpreter(),
                examples=examples
            )
        logger.debug("decider created")

    def synthesize(self, depth, loc, examples=None):
        global g_enumerator_cache
        logger.debug("creating synthesizer")
        start_time = time.time()
        if (self.spectext, depth, loc) in g_enumerator_cache:
            enumerator = g_enumerator_cache[(self.spectext, depth, loc)]
        else:
            enumerator = SmtEnumerator(self.spec, depth=depth, loc=loc)  # loc is the number of function calls in the synthesized program
            # g_enumerator_cache[(self.spectext, depth, loc)] = enumerator
            # print(len(g_enumerator_cache), hashlib.md5(self.spectext).hexdigest(), depth, loc)
        enumerator_init_time = time.time() - start_time

        start_time = time.time()
        if examples:
            logger.debug("creating decider in synthesize()")
            decider = ExampleConstraintDecider(
                spec=self.spec,  # spec is needed for this decider
                interpreter=Interpreter(),
                examples=examples
            )
            logger.debug("decider created")
        else:
            decider = self.decider 
        synthesizer = Synthesizer(
            enumerator=enumerator,
            decider=decider
        )
        decider_init_time = time.time() - start_time

        logger.debug("synthesizer created")
        start_synth_time = time.time()

        # Do synthesis
        res = synthesizer.synthesize()

        self.enumerator_init_time = enumerator_init_time
        self.decider_init_time = decider_init_time
        self.time_elapsed = time.time() - start_synth_time
        self.num_attempts = synthesizer.num_attempts
        if res:
            logger.debug(f"synthesized program {res}, time_elapsed: {self.time_elapsed}")
        else:
            logger.debug(f"synthesis failed, time_elapsed: {self.time_elapsed}")
        return res

if __name__ == '__main__':
    import argparse
    import logging
    import sys
    import json
    import os

    directory = os.path.dirname(os.path.realpath(__file__))
    mlogger = get_logger('main')

    def get_type(c):
        if c == "s":
            return "String"
        elif c == "S":
            return "AString"
        elif c == "b":
            return "Bool"
        elif c == "i":
            return "Int"
        elif c == "R":
            return "Row"
        elif c == "a":
            return "Any"
        elif c == "A":
            return "AAny"
        elif c == "0":
            return "AStringAny"
        else:
            raise Execption()

    def gen_program_type(S):
        types = [get_type(c) for c in S]
        return f"({', '.join(types[:-1])}) -> {types[-1]}"

    def load_examples(f):
        return [json.loads(l) for l in open(f)]

    parser = argparse.ArgumentParser(description='Synthesize an SQL functional program.')
    parser.add_argument("signature", nargs='?', help='Input types followed by output type (e.g. SSB)')
    parser.add_argument("examples", nargs='*', help='(input, output)')
    parser.add_argument("--ex", help='load examples from file')
    parser.add_argument("--udf", help='load infomation from udf')
    parser.add_argument("-o", help='output synthesized program to a file')
    parser.add_argument("-d", action='store_true', help='debug')
    parser.add_argument("-cs", action='append', help='const string')
    parser.add_argument("-col", action='append')
    parser.add_argument("-e", help='evaluate expression')
    parser.add_argument("--loc", type=int, help='number of calls')
    parser.add_argument("--depth", type=int, help='maximum of depth')
    args = parser.parse_args()

    print(args)
    if args.d:
        logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s %(message)s")
    examples = [eval(e) for e in args.examples]
    if args.ex:
        for ex in load_examples(args.ex):
            examples.append((ex['input'], ex['output']))
    print(examples)
    examples = [Example(input=e[0], output=e[1]) for e in examples]

    constrings = None
    if args.cs:
        constrings = ', '.join([f'"{cs}"' for cs in args.cs])
    synth = SQLSynth(f"{directory}/spec.tyrell.jinja2",
                    program_type=gen_program_type(args.signature),
                    const_string=constrings,
                    columns = args.col)

    if args.e:
        for ex in examples:
            output=synth.eval(args.e, ex.input)
            print(f"evaluated {ex.input}, return {output}, expect {ex.output}")
        sys.exit()


    synth.set_examples(examples)

    if args.loc:
        minloc, maxloc = args.loc, args.loc
    else:
        minloc, maxloc = 1, 5 

    for loc in range(minloc, maxloc+1):
        if args.depth:
            mindepth, maxdepth = args.depth, args.depth
        else:
            mindepth, maxdepth = 1, loc+1,
        for depth in range(mindepth, maxdepth+1):
            mlogger.debug(f"try synthesizing loc={loc} depth={depth}")
            res = synth.synthesize(loc=loc, depth=depth)
            if res:
                if args.o:
                    from product import gen_sql_from_trinity
                    f = open(args.o, 'w')
                    print(res, file=f)
                    print(gen_sql_from_trinity(res), file=f)
                # import code
                # code.InteractiveConsole(locals=globals()).interact()
                sys.exit()
            
