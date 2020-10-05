from synthesizer import SQLSynth
from tyrell.decider import Example
import re, pytest
import logging

LOG_FORMAT="%(asctime)-15s %(message)s"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)

@pytest.fixture(scope="module")
def synth_ssss():
    return SQLSynth("spec.tyrell.jinja2", program_type="(String, String, String) -> String")

@pytest.fixture(scope="module")
def synth_ss():
    return SQLSynth("spec.tyrell.jinja2", program_type="(String) -> String")

component_tests=[
    ("abs", "II", [([10], 10),
                   ([-10], 10)]),
    ("add", "III", [([10, 3], 13)]),
    ("and", "BBB", [([True, True], True),
                    ([True, False], False)]),
    ("ascii", "SI", [(["222"], 50)]),
    ("char", "IS", [([50], "2")]),
    ("concat", "SSS", [(["foo", "bar"], "foobar")]),
    ("concat_ws", "SSSS", [(["-", "foo", "bar"], "foo-bar")]),
    ("eq", "IIB", [([10, 3], False),
                   ([10, 10], True),
                   ([3, 10], False)]),
    ("eq_str", "SSB", [(["foo", "foo"], True),
                       (["foo", "bar"], False)]),
    ("if_str", "BSSS", [([True, "foo", "bar"], "foo"),
                        ([False, "foo", "bar"], "bar")]),
    # ("ge", "IIB", [([10, 3], True),
    #                ([10, 10], True),
    #                ([3, 10], False)]),
    # ("gt", "IIB", [([10, 3], True),
    #                ([10, 10], False),
    #                ([3, 10], False)]),
    ("initcap", "SS", [(["heLLo worLD"], "Hello World")]),
    ("int", "SI", [(["10"], 10)]),
    ("le", "IIB", [([10, 3], False),
                   ([10, 10], True),
                   ([3, 10], True)]),
    ("length", "SI", [(['Spark SQL '], 10)]),
    ("levenshtein", "SSI", [(["kitten", "sitting"], 3)]),
    ("locate", "SSI", [(["bar", "foobarbar"], 4),
                       (["bar1", "foobarbar"], 0)]),
    ("locate2", "SSII", [(["bar", "foobarbar", 5], 7),
                       (["bar1", "foobarbar", 5], 0)]),
    ("lower", "SS", [(["FOO"], "foo")]),
    ("lpad", "SIS", [(["hi", 5], "   hi")]),
    ("lpad2", "SISS", [(["hi", 5, "??"], "???hi"),
                       (["hi", 1, "??"], "h")]),
    ("lt", "IIB", [([10, 3], False),
                   ([10, 10], False),
                   ([3, 10], True)]),
    ("ltrim", "SS", [(["    SparkSQL   "], "SparkSQL   ")]),
    ("ltrim2", "SSS", [(["SSparkSQLS", "SQLS"], "parkSQLS")]),
    ("max", "III", [([10, 3], 10)]),
    ("min", "III", [([10, 3], 3)]),
    ("mod", "III", [([10, 3], 1)]),
    ("mul", "III", [([10, 3], 30)]),
    ("neg", "II", [([3], -3)]),
    ("not", "BB", [([False], True),
                   ([True], False)]),
    ("or", "BBB", [([True, True], True),
                    ([True, False], True)]),
    ("overlay", "SSIS", [(["Spark SQL", "CORE", 7], "Spark CORE"),
                         (["Spark SQL", "_", 6], "Spark_SQL")]),
    ("overlay2", "SSIIS", [(["Spark SQL", "ANSI ", 7, 0], "Spark ANSI SQL"),
                         (["Spark SQL", "tructured", 2, 4], "Structured SQL")]),
    ("repeat", "SIS", [(["123", 2], "123123"),
                       (["123", -2], "")]),
    ("replace", "SSS", [(["foobarbarb", "bar"], "foob")]),
    ("replace2", "SSSS", [(["foobarbarb", "bar", "foo"], "foofoofoob")]),
    ("reverse", "SS", [(["foobar"], "raboof")]),
    ("right", "SIS", [(["    SparkSQL", 3], "SQL")]),
    ("rtrim", "SS", [(["    SparkSQL   "], "    SparkSQL")]),
    ("rtrim2", "SSS", [(["SSparkSQLS", "SQLS"], "SSpark")]),
    ("rpad", "SIS", [(["hi", 5], "hi   ")]),
    ("rpad2", "SISS", [(["hi", 5, "??"], "hi???"),
                       (["hi", 1, "??"], "h")]),
    ("soundex", "SS", [(["Miller"], "M460")]),
    ("sub", "III", [([10, 3], 7)]),
    ("substring", "SIS", [(["Spark SQL", 5], "k SQL"),
                          (["Spark SQL", -3], "SQL")]),
    ("substring2", "SIIS", [(["Spark SQL", 5, 1], "k")]),
    ("substring_index", "SSIS", [(["www.apache.org", ".", 2], "www.apache")]),
    ("translate", "SSSS", [(["foo", "fo", "ba"], "baa")]),
    ("trim", "SS", [([" foo "], "foo")]),
    ("trim2", "SSS", [(["_-", "_foo-"], "foo")]),
    ("upper", "SS", [(["foo"], "FOO")]),
]

@pytest.fixture(params=component_tests, ids=[i[0] for i in component_tests])
def component(request):
    return request.param

def test_component(component):
    def get_type(c):
        if c == "S":
            return "String"
        elif c == "B":
            return "Bool"
        elif c == "I":
            return "Int"
        else:
            raise Execption()
    def gen_program_type(S):
        types = [get_type(c) for c in S]
        return f"({', '.join(types[:-1])}) -> {types[-1]}"
    def gen_eval_program(name, S):
        return f"({name} {' '.join([f'(@param {i})' for i in range(len(S)-1)])})"
    def gen_synth_program(name, S):
        return f"{name}\\({', '.join([f'@param[0-9]' for i in range(len(S)-1)])}\\)"

    synth = SQLSynth("spec.tyrell.jinja2", program_type=gen_program_type(component[1]))
    eval_p = gen_eval_program(component[0], component[1])
    synth_p = gen_synth_program(component[0], component[1])

    for (i, o) in component[2]:
        assert(synth.eval(eval_p, i) == o)

    examples = [ Example(input=i, output=o) for (i, o) in component[2]]
    assert(re.match(synth_p, str(synth.synthesize(depth=1, loc=1, examples=examples))))

def test_row():
    synth = SQLSynth("spec.tyrell.jinja2", program_type="(String, Int, Bool) -> Row", columns=["String", "Int", "Bool"])
    eval_p = "(row (@param 0) (@param 1) (@param 2))"
    synth_p = "row(@param0, @param1, @param2)"

    example = (["abc", 1, True], ("abc", 1, True))
    assert(synth.eval(eval_p, example[0]) == example[1])

    examples = [Example(input=example[0], output=example[1])]
    assert(synth_p == str(synth.synthesize(depth=1, loc=1, examples=examples)))

# def test_eval_translate(synth_ssss):
#     p = "(translate (@param 0) (@param 1) (@param 2))"
#     assert(synth_ssss.eval(p, ["foo", "fo", "ba"]) == "baa")

# def test_synth_translate(synth_ssss):
#     p = "translate(@param0, @param1, @param2)"
#     assert(str(synth_ssss.synthesize(
#         examples=[Example(input=["foo", "fo", "ba"], output="baa")],
#         depth=1, loc=1)) == p)

# def test_eval_initcap(synth_ss):
#     p = "(initcap (@param 0))"
#     assert(synth_ss.eval(p, ["heLLo worLD"]) == "Hello World")

# def test_synth_initcap(synth_ss):
#     p = "initcap(@param0)"
#     assert(str(synth_ss.synthesize(
#         examples=[Example(input=["heLLo worLD"], output="Hello World")],
#         depth=1, loc=1
#     )) == p)
