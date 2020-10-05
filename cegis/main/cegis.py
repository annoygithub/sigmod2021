import os
import time
import logging
import json
from copy import deepcopy
import xml.dom.minidom as dom
import product
import synthesizer
import jbmc
import cbmc
from pathlib import Path
from tyrell.decider import Example

LOG = logging.getLogger("cegis")
DIR = os.path.dirname(os.path.realpath(__file__))
HOME = f"{DIR}/../../"
LIBMODELS_DIR = f"{HOME}/scala2c/models/"

SCAFFOLD_JAR=f"{DIR}/../product/target/scala-2.11/product_2.11-0.1.0-SNAPSHOT.jar"

def compile_prod():
    os.system("rm -fr .cegis")
    os.system(f"scalac product.scala -cp {SCAFFOLD_JAR}")

def unhex_str(s):
    if s in ("int", "String", "AString"):
        return s
    return bytes.fromhex(s).decode('latin1')

def hex_str(s):
    if s in ("int", "String", "AString"):
        return s
    return s.encode('latin1').hex()

def repr_input(input):
    for i in range(len(input)):
        if type(input[i]) == str:
            input[i] = f'"{hex_str(input[i])}"'
        elif type(input[i]) in (int, float):
            input[i] = str(input[i])
        elif type(input[i]) == bool:
            input[i] = 'true' if input[i] else 'false'
        elif type(input[i] == list):
            repr_input(input[i])
            input[i] = f"[{','.join(input[i])}]"
        else:
            raise Exception(f"Unknown type {type(input[i])} of {input[i]}")

def unhex_col(col):
    if type(col) == str:
        return unhex_str(col)
    elif type(col) == int or type(col) == bool or type(col) == float:
        return col
    elif type(col) == list:
        return [unhex_col(c) for c in col]
    elif type(col) == dict:
        return {unhex_col(k): unhex_col(v) for k, v in col.items()}
    else:
        raise Exception(f"Unknown type {type(col)} of {col}")

def unhex_example(example):
    example['input'] = unhex_col(example['input'])
    example['output'] = unhex_col(example['output'])
    # input = example['input']
    # for i in range(len(input)):
    #     if type(input[i]) == str:
    #         input[i] = unhex_str(input[i])
    # if type(example['output']) == str:
    #     example['output'] = unhex_str(example['output'])
    # if type(example['output']) == list: # Row
    #     def unhex_col
    #     example['output'] = [unhex_str(o) if type(o) == str else o for o in example['output']]
    return example

def gen_examples_from_prod():
    N = 3
    examples = os.popen(f"scala -cp .:{SCAFFOLD_JAR} cegis.product.Product gen {N}").read().strip()
    LOG.debug(f"initial examples: [{examples}]")
    if not examples:
        return []
    examples = [unhex_example(json.loads(l)) for l in examples.split('\n')]
    with open('../examples', 'w') as f:
        for e in examples:
            print(json.dumps(e), file=f)
    LOG.debug(f"{examples}")
    return [Example(input=e['input'], output=e['output']) for e in examples]

def complete_couterexample(counterexample):
    repr_input(counterexample)
    ce = " ".join([f"'{ce}'" for ce in counterexample])
    ce = os.popen(f"scala -cp .:{SCAFFOLD_JAR} cegis.product.Product run {ce}").read()
    ce = unhex_example(json.loads(ce))
    return Example(input=ce['input'], output=ce['output'])

def run_jbmc():
    JBMC=f"{Path.home()}/cbmc512/jbmc/src/jbmc/jbmc"
    JAVA_MODELS=f"{Path.home()}/cbmc512/jbmc/lib/java-models-library/target/core-models.jar"
    return os.popen(f"""{JBMC} cegis.product.Product \
                  --classpath .:{JAVA_MODELS}:{SCAFFOLD_JAR} \
                  --function 'cegis.product.Product.product' \
                  --java-assume-inputs-non-null \
                  --unwind 2 --max-nondet-string-length 16  --java-assume-inputs-interval [-17:17] \
                  --xml-ui """).read()


def translate_type(t):
    if t == "Boolean" or t == "_Bool":
        return "Bool"
    elif t == "Int" or t == "int":
        return "Int"
    elif t == "Long" or t == "long":
        return "Int"
    elif t == "Double" or t == "double":
        return "Double"
    elif t == "String":
        return "String"
    elif t == "AString":
        return "AString"
    elif t == "Any":
        return "Any"
    elif t == "AAny":
        return "AAny"
    elif t == "AStringAny":
        return "AStringAny"
    elif t == "MStringAny":
        return "MStringAny"
    else:
        raise Exception(f"Unknown type {t}")

def gen_program_type(udf):
    arg_types = [translate_type(a[1]) for a in udf["args"]]
    ret_type = "Row" if type(udf['ret']) == list else translate_type(udf["ret"][1])
    return f"({', '.join(arg_types)}) -> {ret_type}"

class STATS:
    @classmethod
    def reset(cls):
        cls.examples = None
        cls.pbe = []
        cls.synth_init_time = 0
        cls.decider_init_time = 0
        cls.gen_example_time = 0
        cls.model_checking_time = 0
        cls.test_time = 0
        cls.sql = None

    @classmethod
    def print_stats(cls):
        total_enumerator_init_time = sum([i[4] for i in cls.pbe])
        # total_decider_init_time = sum(i[5] for i in cls.pbe) + cls.decider_init_time
        total_synth_time = sum([i[3] for i in cls.pbe])
        total_synth_attempts = sum(i[2] for i in cls.pbe)
        total_synth_init_time = cls.synth_init_time + cls.decider_init_time + total_enumerator_init_time 
        total_pbe_time = total_synth_init_time + total_synth_time
        total_time = total_pbe_time + cls.test_time + cls.model_checking_time + cls.gen_example_time
        LOG.info(f"""
examples: {cls.examples}
stats:
  synth_init_time={cls.synth_init_time}
  decider_init_time={cls.decider_init_time}
  total_enumerator_init_time={total_enumerator_init_time}
  total_synth_init_time={total_synth_init_time}
  total_synth_time={total_synth_time}
  total_synth_attempts={total_synth_attempts}
  total_pbe_time={total_pbe_time}
  gen_example_time={cls.gen_example_time}
  test_time={cls.test_time}
  model_checking_time={cls.model_checking_time}
  total_time={total_time}
sql: {cls.sql}
""")

def pbe(udf, examples, last_loc=0, last_depth=0):
    K = 1 # search depth factor

    start_time = time.time()
    spec = f"{DIR}/spec.tyrell.jinja2"
    conststrings = udf.get("strings", None)
    if conststrings is not None:
        conststrings = ",".join(conststrings)
    constints = udf.get("ints", None)
    if constints:
        # constints.append('"0"')
        constints = set(constints).union({'"1"', '"-1"', '"0"'})
        constints = ",".join(constints)
    constdoubles = udf.get("doubles", None)
    if constdoubles:
        constdoubles = ",".join(constdoubles)
    columns = None
    if type(udf['ret']) == list:
        columns = [translate_type(r[1]) for r in udf['ret']]
    synth = synthesizer.SQLSynth(spec,
                                 program_type=gen_program_type(udf),
                                 const_string=conststrings,
                                 const_int=constints,
                                 const_double=constdoubles,
                                 columns=columns)
    STATS.synth_init_time = time.time() - start_time

    start_time = time.time()
    if examples:
        synth.set_examples(examples)
    STATS.decider_init_time = time.time() - start_time

    if "depth" in udf:
        maxloc = udf['depth']
    else:
        maxloc = K * (len(udf['body'].split('\n')) + len(udf['args']) + len(udf['ret']))
    STATS.pbe = []
    for loc in range(0, maxloc+1):
        if loc < last_loc:
            continue
        for depth in range(loc+2, loc+3):
            if depth < last_depth:
                continue
            last_depth = 0
            LOG.info(f"trying loc={loc}, depth={depth}")
            sql = synth.synthesize(loc=loc, depth=depth)
            STATS.pbe.append((loc, depth, synth.num_attempts, synth.time_elapsed, synth.enumerator_init_time))
            if sql:
                # print_stats(stats, examples, sql)
                return (sql, loc, depth)

    # print_stats(stats, examples, sql)
    return None

def cegis(udf, gen_example=True):
    LOG.info("Generating initial examples")
    os.system("rm -f product.scala")
    with open('product.scala', 'w') as f:
        f.write(product.gen_product_prog(udf))
    compile_prod()
    examples = gen_examples_from_prod() if gen_example else []

    last_loc = 0
    last_depth = 0
    while True:
        LOG.info("Synthesizing sql")
        if examples:
            ret = pbe(udf, examples, last_loc=last_loc, last_depth=last_depth)
            if ret is None:
                return None
            (sql, last_loc, last_depth) = ret
        else:
            sql = None
        
        scala_sql = product.gen_sql_from_trinity(sql) if sql else None
        LOG.info("Generating the product program")
        os.system("rm -f product.scala")
        with open('product.scala', 'w') as f:
            f.write(product.gen_product_prog(udf, scala_sql))
        compile_prod()

        LOG.info("Verifying the product program using jbmc")
        res = run_jbmc()
        with open('jbmc.xml', 'w') as f:
            f.write(res)
        counterexample = jbmc.parse_jbmc_xml_result(dom.parseString(res))
        if counterexample is None:
            LOG.info("No counterexample found. We are done!!! (or something unexpected happened)")
            return sql

        LOG.info(f"Found new counter example {counterexample}")
        examples.append(complete_couterexample(counterexample))

def compile_c_udf_prog():
    os.system("rm -f udf")
    os.system(f"gcc -g main.c -I{LIBMODELS_DIR} {LIBMODELS_DIR}/libmodels.a -o udf")

def gen_examples_from_c_udf_prog():
    N = 1
    examples = os.popen(f"./udf gen {N}").read().strip()
    LOG.debug(f"initial examples: [{examples}]")
    if not examples:
        return []
    examples = [unhex_example(json.loads(l)) for l in examples.split('\n')]
    with open('../examples', 'w') as f:
        for e in examples:
            print(json.dumps(e), file=f)
    LOG.debug(f"{examples}")
    return [Example(input=e['input'], output=e['output']) for e in examples]

def run_cbmc(udf):
    MAX_UNWIND = 17
    if "unwind" in udf:
        unwind = udf["unwind"]
    elif "strings" or "ints" in udf:
        max_str = 1
        if "strings" in udf and len(udf["strings"]) > 0:
            max_str = max([len(s) for s in udf["strings"]])
        max_int = 1
        if "ints" in udf:
            max_int = max([int(i[1:-1]) for i in udf["ints"]])
        max_split = 1
        if "String_split" in udf["body"]:
            max_split = (max_int+1)*(max_str-2) + 2
        unwind = max(4, max_str, max_int+1, max_split)
    else:
        unwind = 4
    unwind = min(unwind, MAX_UNWIND)
    CBMC=f"{HOME}/third_party/cbmc/src/cbmc/cbmc"
    cmd = f"""{CBMC} product.c {LIBMODELS_DIR}/*.c \
-I. -I {LIBMODELS_DIR} -DCBMC \
--function 'product' \
--unwind {unwind} \
--json-ui """
    LOG.debug(cmd)
    return os.popen(cmd).read()

def complete_c_couterexample(counterexample):
    repr_input(counterexample)
    ce = " ".join([f"'{ce}'" for ce in counterexample])
    LOG.debug(f"Running udf with {ce}")
    ce = os.popen(f"./udf run {ce}").read()
    ce = unhex_example(json.loads(ce))
    LOG.debug(f"Nex example {ce}")
    return Example(input=ce['input'], output=ce['output'])

def test_sql(udf, sql, examples):
    with open('sqlmain.c', 'w') as f:
        f.write(product.gen_c_sql_prog(udf))
    os.system("rm -f sql")
    os.system(f"gcc sqlmain.c -g -I{LIBMODELS_DIR} {LIBMODELS_DIR}/libmodels.a -o sql")
    if not os.path.exists("sql"):
        raise Exception("program sql not found, probably compilation failed")
    for ex in examples:
        inp = deepcopy(ex.input)
        repr_input(inp)
        inp = " ".join([f"'{ce}'" for ce in inp])
        LOG.debug(f"Running sql with {inp}")
        oup = os.popen(f"./sql run {inp}").read()
        if not oup:
            LOG.warn(f"Run failed with input {inp}")
            continue
        oup = unhex_example(json.loads(oup))
        assert ex.output == oup["output"], f"input={inp}, udfOutput={ex.output}, sqlOutput={oup['output']}"


def c_cegis(udf, gen_example=True):
    LOG.info("Generating initial examples")
    STATS.reset()
    start_time = time.time()

    os.system("rm -f udf.c sql.c main.c product.c")
    with open('udf.c', 'w') as f:
        f.write(product.gen_c_udf(udf))
    with open('main.c', 'w') as f:
        f.write(product.gen_c_udf_prog(udf))
    compile_c_udf_prog()
    examples = gen_examples_from_c_udf_prog() if gen_example else []
    
    STATS.gen_example_time = time.time() - start_time

    last_loc = 0
    last_depth = 0
    while True:
        LOG.info("Synthesizing sql")

        if examples:
            ret = pbe(udf, examples, last_loc=last_loc, last_depth=last_depth)
            if ret is None:
                return None
            (sql, last_loc, last_depth) = ret
        else:
            sql = None
        
        LOG.info("Testing synthesized sql")
        start_time = time.time()
        with open('sql.c', 'w') as f:
            f.write(product.gen_c_sql(udf, sql))
        test_sql(udf, sql, examples)
        STATS.test_time = time.time() - start_time

        LOG.info("Generating the product program")
        start_time = time.time()
        os.system("rm -f product.c")
        with open('product.c', 'w') as f:
            f.write(product.gen_c_product_prog(udf))

        LOG.info("Verifying the product program using cbmc")
        res = run_cbmc(udf)
        with open('cbmc.json', 'w') as f:
            f.write(res)
        counterexample = cbmc.parse_cbmc_result('cbmc.json')
        STATS.model_checking_time = time.time() - start_time

        STATS.examples = examples
        STATS.sql = sql
        STATS.print_stats()
        STATS.reset()

        if counterexample is None:
            LOG.info("No counterexample found. We are done!!! (or something unexpected happened)")
            return sql

        LOG.info(f"Found new counter example {counterexample}")
        start_time = time.time()
        examples.append(complete_c_couterexample(counterexample))
        STATS.gen_example_time = time.time() - start_time

def pbe_from_example_file(udf, f):
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    examples = open(f).read().strip()
    LOG.debug(f"loaded examples: {examples}")
    examples = [json.loads(l) for l in examples.split('\n')]
    examples = [Example(input=e['input'], output=e['output']) for e in examples]
    return pbe(udf, examples)

def init(debug=False):
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG if debug else logging.INFO)
    os.system("rm -fr .cegis")
    os.system("mkdir .cegis")
    os.chdir(f"{os.getcwd()}/.cegis")

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    os.system("rm -fr .cegis")
    os.system("mkdir .cegis")
    os.chdir(f"{os.getcwd()}/.cegis")
    udf = {    "body": """int startIndex=String_indexOf(name, constString(", "));""",
    "args": [("name", "String")],
    "ret": ("startIndex", "int"),
    "strings": ['", "']}
    print(c_cegis(udf))
