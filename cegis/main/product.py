

def gen_udf_arglist(udf):
    args = [f"{arg[0]}:{arg[1]}" for arg in udf['args']]
    return ", ".join(args)

def gen_udf_func(udf):
    return f"""
        def udf({gen_udf_arglist(udf)}): {udf['ret'][1]} = {{
            {udf['body']}
            return {udf['ret'][0]}
        }}
    """

def gen_sql_arglist(udf):
    args = [f"_{i+1}:{udf['args'][i][1]}" for i in range(len(udf['args']))]
    return ", ".join(args)

def gen_sql_func(udf, sql):
    if sql is None:
        sql = f"null.asInstanceOf[{udf['ret'][1]}]"
    return (f"""
        def sql({gen_sql_arglist(udf)}) = {sql}
    """)

def gen_product_func(udf):
    arglist = gen_sql_arglist(udf)
    return (f"""
        def product({arglist}) = {{
            val a = udf({arglist})
            val b = sql({arglist})
            Jassert.assert_equal(a, b)
        }}
    """)

def gen_product_invoke(udf):
    args = [f"null.asInstanceOf[{arg[1]}]" for arg in udf['args']]
    return f"""
        product({", ".join(args)})
    """

def gen_product_prog(udf, sql=None):
    return (f"""
    package cegis.product

    object Product{{
{gen_udf_func(udf)}
{gen_sql_func(udf, sql)}
{gen_product_func(udf)}
    
        def main(args: Array[String]): Unit = {{
            if (args(0) == "gen") {{
                val n = args(1).toInt
                ExampleGenerator.genExamples("udf", Product, n)
            }}

            if (args(0) == "run") {{
                val input = args.slice(1, args.size)
                ExampleGenerator.runInput("udf", Product, input)
            }}

            if (args(0) == "jpf") {{
                {gen_product_invoke(udf)}
            }}
        }}
    }}
    """)

def gen_sql_from_trinity(sql):
    # import code
    # code.InteractiveConsole(locals=locals()).interact()
    if sql.is_apply():
        args = [gen_sql_from_trinity(arg) for arg in sql.args]
        return f"SqlModel.{sql.name}({', '.join(args)})"
    elif sql.is_param():
        return f"_{sql.index+1}"
    elif sql.is_enum():
        if sql.type.name == "ConstString":
            return f'"{sql.data}"'
        elif sql.type.name in ("ConstInt", "ConstBool"):
            return sql.data
        else:
            raise Exception(f"Unknown enum type{sql.type}")
    else:
        raise Exception(f"Unknown sql {sql}")

def gen_c_row_type_and_func(udf):
    if type(udf['ret']) != list:
        return ""
    struct_fields = ";\n".join([f"{r[1]} _{i+1}" for (i, r) in enumerate(udf['ret'])])
    arg_list = ", ".join([f"{r[1]} _{i+1}" for (i, r) in enumerate(udf['ret'])])
    init_fields = ";\n".join([f"r._{i+1} = _{i+1}" for i in range(len(udf['ret']))])
    return f"""
typedef struct{{
    {struct_fields};
}} Row;

Row SQL_row({arg_list}) {{
    Row r;
    {init_fields};
    return r;
}}
    """

def get_c_udf_arglist(udf):
    return ", ".join([f"{arg[1]} {arg[0]}" for arg in udf['args']])

def gen_c_row_udf(udf):
    return f"""
#include "String.h"
#include "Array.h"
#include "Map.h"
#include "Any.h"
#include "box.h"
#include "Tuple.h"

Row udf({get_c_udf_arglist(udf)}) {{
    {udf["body"]};
    return SQL_row({", ".join([r[0] for r in udf['ret']])});
}}
    """

def gen_c_udf(udf):
    if type(udf["ret"]) == list:
        return gen_c_row_udf(udf)
    return f"""
#include "String.h"
#include "Array.h"
#include "Map.h"
#include "Any.h"
#include "box.h"
#include "Tuple.h"

{udf["ret"][1]} udf({get_c_udf_arglist(udf)}) {{
    {udf["body"]};
    return {udf["ret"][0]};
}}
    """

def gen_c_sql_from_trinity(sql):
    # import code
    # code.InteractiveConsole(locals=locals()).interact()
    if sql.is_apply():
        args = [gen_c_sql_from_trinity(arg) for arg in sql.args]
        return f"SQL_{sql.name}({', '.join(args)})"
    elif sql.is_param():
        return f"_{sql.index+1}"
    elif sql.is_enum():
        if sql.type.name == "ConstString":
            return f'"{repr(sql.data)[1:-1]}"'
        elif sql.type.name in ("ConstInt", "ConstBool", "ConstDouble"):
            return sql.data
        else:
            raise Exception(f"Unknown enum type {sql.type}")
    else:
        raise Exception(f"Unknown sql {sql}")

def gen_c_sql_arglist(udf):
    args = [f"{udf['args'][i][1]} _{i+1}" for i in range(len(udf['args']))]
    return ", ".join(args)

def gen_c_sql(udf, sql):
    retType = "Row" if type(udf['ret']) == list else udf["ret"][1]
    if sql:
        c_sql = gen_c_sql_from_trinity(sql)
    
    arglist = gen_c_sql_arglist(udf)
    return f"""
#include "sql_model.h"

{retType} sql({arglist}) {{
    {retType} r;
    {f"r = {c_sql};" if sql else ""}
    return r;
}}
    """

def gen_var(i, arg):
    return f"_{i+1}_{arg[0]}"

def gen_c_cast_inputs(udf):
    stmts = []
    for i, arg in enumerate(udf["args"]):
        var = gen_var(i, arg)
        if arg[1] == "String":
            stmts.append(f"String {var} = malloc(sizeof(_String));\n")
            stmts.append(f"{var}->size = (strlen(argv[{i+2}]) - 2) / 2;\n")
            stmts.append(f"{var}->buf = unhex(argv[{i+2}] + 1, {var}->size * 2);")
        elif arg[1] == "int":
            stmts.append(f"int {var} = atoi(argv[{i+2}]);")
        elif arg[1] == "long":
            stmts.append(f"long {var} = atoi(argv[{i+2}]);")
        elif arg[1] == "double":
            stmts.append(f"double {var} = atof(argv[{i+2}]);")
        elif arg[1] == "_Bool":
            stmts.append(f'_Bool {var} = strcmp(argv[{i+2}], "true") == 0 ? 1 : 0;')
        elif arg[1] == "AString":
            stmts.append(f'AString {var} = cstr2astr(argv[{i+2}]);')
        elif arg[1] == "Any":
            stmts.append(f"Any {var} = str2any(argv[{i+2}]);")
        elif arg[1] == "AAny":
            stmts.append(f"AAny {var} = str2aany(argv[{i+2}]);")
        elif arg[1] == "AStringAny":
            stmts.append(f"AStringAny {var} = str2astringany(argv[{i+2}]);")
        else:
            raise Exception(f"Unknown type {arg[1]}")
    return "\n".join(stmts)

def gen_c_call_arglist(udf):
    args = []
    for i, arg in enumerate(udf["args"]):
        var = gen_var(i, arg)
        if arg[1] == "String":
            args.append(f"dup_string({var})")
        elif arg[1] == "AString":
            args.append(f"dup_astring({var})")
        elif arg[1] in ("int", "long", "_Bool", "double"):
            args.append(var)
        elif arg[1] == "Any":
            args.append(f"dup_any({var})")
        elif arg[1] == "AAny":
            args.append(f"dup_aany({var})")
        elif arg[1] == "AStringAny":
            args.append(f"dup_astringany({var})")
        else:
            raise Exception(f"Unknown type {arg[1]}")
    return ", ".join(args)

def gen_c_call_udf(udf, ret):
    retType = "Row" if type(udf["ret"]) == list else udf['ret'][1]
    return f"{retType} {ret} = udf({gen_c_call_arglist(udf)});"

def gen_c_rand_inputs(udf):
    stmts = []
    arglist = [str(len(udf["args"]))]
    for i, arg in enumerate(udf["args"]):
        # if arg[1] == "String":
        #     rand_func = "rand_string"
        # elif arg[1] == "int":
        #     rand_func = "rand_int"
        # elif arg[1] == "long":
        #     rand_func = "rand_long"
        # elif arg[1] == "_Bool":
        #     rand_func = "rand_bool"
        # elif arg[1] == "AString":
        #     rand_func = "rand_astring"
        # elif arg[1] == "Any":
        #     rand_func = "rand_any"
        # elif arg[1] == "AAny":
        #     rand_func = "rand_aany"
        # elif arg[1] == "AStringAny":
        #     rand_func = "rand_astringany"
        # else:
        #     raise Exception(f"Unknown type {arg[1]}")
        var = gen_var(i, arg)
        arglist.append(f"TYPE_{arg[1]}")
        arglist.append(f"&{var}")
        stmts.append(f"{arg[1]} {var};")

    stmts.append(f"rand_inputs({', '.join(arglist)});")
    return "\n".join(stmts)


def gen_c_print_format(tpe):
    if tpe == "String":
        return '\\"%s\\"'
    elif tpe == "int":
        return "%d"
    elif tpe == "long":
        return "%li"
    elif tpe == "_Bool":
        return "%s"
    elif tpe == "double":
        return "%.10f"
    elif tpe == "AString":
        return "%s"
    elif tpe == "MStringAny":
        return "%s"
    elif tpe == "Any":
        return "%s"
    elif tpe == "AAny":
        return "%s"
    elif tpe == "AStringAny":
        return "%s"
    else:
        raise Exception(f"Unknown type {tpe}")

def gen_c_print_arg(tpe, var):
    if tpe == "String":
        return f"hex({var}->buf, (int){var}->size)"
    elif tpe == "int" or tpe == "long" or tpe == 'double':
        return var
    elif tpe == "_Bool":
        return f'{var} ? "true" : "false"'
    elif tpe == "AString":
        return f"astr2cstr({var})"
    elif tpe == "MStringAny":
        return f"mstringany2str({var})"
    elif tpe == "Any":
        return f"any2str({var})"
    elif tpe == "AAny":
        return f"aany2str({var})"
    elif tpe == "AStringAny":
        return f"astringany2str({var})"
    else:
        raise Exception(f"Unknown type {tpe}")

def gen_c_print_result(udf):
    input_fmts = ", ".join([gen_c_print_format(arg[1]) for arg in udf["args"]])
    input_args = ", ".join([gen_c_print_arg(arg[1], gen_var(i, arg)) 
                            for i, arg in enumerate(udf["args"])])
    if type(udf["ret"]) == list:
        output_fmt = f"[{', '.join([gen_c_print_format(r[1]) for r in udf['ret']])}]"
        output_arg = ", ".join([gen_c_print_arg(r[1], f"ret._{i+1}") 
                            for (i, r) in enumerate(udf["ret"])])
    else:
        output_fmt = gen_c_print_format(udf["ret"][1])
        output_arg = gen_c_print_arg(udf["ret"][1], "ret")

    args = output_arg if input_args == "" else f"{input_args}, {output_arg}"

    return f"""printf("{{\\"input\\": [{input_fmts}], \\"output\\": {output_fmt}}}\\n", {args});"""


def gen_c_udf_prog(udf):
    return f"""
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "rand_input.h"

{gen_c_row_type_and_func(udf)}

#include "udf.c"

int main(int argc, char* argv[]) {{
    assert(argc >= 2);

    if (strcmp(argv[1], "gen") == 0) {{
        assert(argc == 3);
        int n = atoi(argv[2]);
        for (int i=0; i<n; i++) {{
            {gen_c_rand_inputs(udf)}
            {gen_c_call_udf(udf, "ret")}
            {gen_c_print_result(udf)}
        }}
    }}
    else if (strcmp(argv[1], "run") == 0) {{
        assert(argc == 2 + {len(udf["args"])});
        {gen_c_cast_inputs(udf)}
        {gen_c_call_udf(udf, "ret")}
        {gen_c_print_result(udf)}
    }}
    return 0;
}}
    """

def gen_c_call_sql(udf, ret):
    if type(udf['ret']) == list:
        return f"Row {ret} = sql({gen_c_call_arglist(udf)});"
    return f"{udf['ret'][1]} {ret} = sql({gen_c_call_arglist(udf)});"

def gen_c_sql_prog(udf):
    return f"""
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "rand_input.h"

{gen_c_row_type_and_func(udf)}

#include "sql.c"

int main(int argc, char* argv[]) {{
    assert(argc >= 2);

    if (strcmp(argv[1], "gen") == 0) {{
        assert(argc == 3);
        int n = atoi(argv[2]);
        for (int i=0; i<n; i++) {{
            {gen_c_rand_inputs(udf)}
            {gen_c_call_sql(udf, "ret")}
            {gen_c_print_result(udf)}
        }}
    }}
    else if (strcmp(argv[1], "run") == 0) {{
        assert(argc == 2 + {len(udf["args"])});
        {gen_c_cast_inputs(udf)}
        {gen_c_call_sql(udf, "ret")}
        {gen_c_print_result(udf)}
    }}
    return 0;
}}
    """

def gen_c_sym_inputs(udf):
    stmts = []
    for i, arg in enumerate(udf["args"]):
        if arg[1] == "String":
            sym_func = "sym_string"
        elif arg[1] == "int":
            sym_func = "sym_int"
        elif arg[1] == "long":
            sym_func = "sym_long"
        elif arg[1] == "_Bool":
            sym_func = "sym_bool"
        elif arg[1] == "AString":
            sym_func = "sym_astring"
        elif arg[1] == "Any":
            sym_func = "sym_any"
        elif arg[1] == "AAny":
            sym_func = "sym_aany"
        elif arg[1] == "double":
            sym_func = "sym_double"
        else:
            raise Exception(f"Unknown type {arg[1]}")

        stmts.append(f"{arg[1]} {gen_var(i, arg)} = {sym_func}();")

    return "\n".join(stmts)

_i_count=0
def gen_i_var():
    global _i_count
    _i_count += 1
    return f'i{_i_count}'

def gen_c_trace_sym_input(stmts, var, tpe):
    # if MAX_STRING_LENGTH==0:
    #     MAX_STRING_LENGTH = 32
    # MAX_ASTRING_SIZE = 2
    # MAX_AANY_SIZE = 2
    if tpe == "String":
        # arglist = [var] + [f"{var}->size"] + [f"{var}->buf[{i}]" for i in range(MAX_STRING_LENGTH)]
        # arglist = ", ".join(arglist)
        # stmts.append(f'__CPROVER_input("{var}", {arglist});')
        vari=gen_i_var()
        stmts.append(f'__CPROVER_input("{var}", {var}, {var}->size);')
        stmts.append(f"for (int {vari}=0; {vari}<{var}->size; {vari}++) {{")
        stmts.append(f'__CPROVER_input("{var}->buf[{vari}]", {var}->buf[{vari}]);')
        stmts.append("}")
    elif tpe == "int" or tpe == "_Bool" or tpe  == "long" or tpe == "double":
        stmts.append(f'__CPROVER_input("{var}", {var});')
    elif tpe == "AString":
        # arglist = []
        # arglist.append(var)
        # arglist.append(f"{var}->size")
        # for i in range(MAX_ASTRING_SIZE):
        #     arglist.append(f"{var}->arr[{i}]->size")
        #     for j in range(MAX_STRING_LENGTH):
        #         arglist.append(f"{var}->arr[{i}]->buf[{j}]")
        # arglist = ", ".join(arglist)
        # stmts.append(f'__CPROVER_input("{var}", {arglist});')
        vari=gen_i_var()
        stmts.append(f'__CPROVER_input("{var}", {var}, {var}->size);')
        stmts.append(f"for (int {vari}=0; {vari}<{var}->size; {vari}++) {{")
        gen_c_trace_sym_input(stmts, f"{var}->arr[{vari}]", "String")
        stmts.append("}")
    elif tpe == "Any":
        stmts.append(f'__CPROVER_input("{var}", {var}, {var}->type);')
        stmts.append(f"if (TYPE_INT == {var}->type){{")
        gen_c_trace_sym_input(stmts, f"((Integer)({var}->obj))->v", "int")
        stmts.append("}")
        stmts.append(f"else if (TYPE_STRING == {var}->type){{")
        gen_c_trace_sym_input(stmts, f"((String)({var}->obj))", "String")
        stmts.append("}")
        stmts.append(f"else if (TYPE_ASTRING == {var}->type){{")
        gen_c_trace_sym_input(stmts, f"((AString)({var}->obj))", "AString")
        stmts.append("}")
    elif tpe == "AAny":
        vari=gen_i_var()
        stmts.append(f'__CPROVER_input("{var}", {var}, {var}->size);')
        stmts.append(f'for (int {vari}=0; {vari}<{var}->size; {vari}++) {{')
        gen_c_trace_sym_input(stmts, f"{var}->arr[{vari}]", "Any")
        stmts.append('}')
    else:
        raise Exception(f"Unknown type {tpe}")

def gen_c_trace_sym_inputs(udf):
    stmts = []
    for i, arg in enumerate(udf["args"]):
        var = gen_var(i, arg)
        gen_c_trace_sym_input(stmts, var, arg[1])

    return "\n".join(stmts)

def gen_c_assert_equal_tpe(tpe, l, r):
    if tpe == "String":
        return f"assert(String_equals({l}, {r}));"
    elif tpe == "AString":
        return f"assert(AString_equals({l}, {r}));"
    elif tpe == "int" or tpe == "_Bool" or tpe == "long":
        return f"assert({l} == {r});"
    elif tpe == "Any":
        return f"assert(Any_equals({l}, {r}));"
    elif tpe == "AAny":
        return f"assert(AAny_equals({l}, {r}));"
    elif tpe == "AStringAny":
        return f"assert(AStringAny_equals({l}, {r}));"
    elif tpe == "MStringAny":
        return f"assert(MStringAny_equals({l}, {r}));"
    elif tpe == "double":
        return f"assert(-0.001 < ({l})-({r}) && ({l})-({r}) < 0.001);"
    else:
        raise Exception(f"Unknown type {tpe}")

def gen_c_assert_equal(udf):
    if type(udf['ret']) == list:
        return "\n".join([gen_c_assert_equal_tpe(r[1], f"ret._{i+1}", f"ret1._{i+1}") 
                            for i, r in enumerate(udf['ret'])])
    return gen_c_assert_equal_tpe(udf['ret'][1], "ret", "ret1")

def gen_c_product_prog(udf):
    return f"""
#include <assert.h>
#include "sym_input.h"
#include "rand_input.h"

{gen_c_row_type_and_func(udf)}

#include "sql.c"
#include "udf.c"

void product() {{
    {gen_c_sym_inputs(udf)}
    {gen_c_trace_sym_inputs(udf)}
    {gen_c_call_udf(udf, "ret")}
    {gen_c_call_sql(udf, "ret1")}
    {gen_c_assert_equal(udf)}
}}
    """


if __name__ == "__main__":
    import sys

    udf = {    "body": """int startIndex=String_indexOf(name, ", ");""",
    "args": [("name", "String")],
    "ret": ("startIndex", "int"),
    "strings": ['", "']}

    print(gen_c_udf(udf))
    print(gen_c_udf_prog(udf))
    print(gen_c_product_prog(udf))
