from pprint import pprint

def parse_prog(prog, i=0):
    if prog[i] == '@':
        assert prog[i:i+4] == '@arg'
        assert prog[i+4] in "0123456789"
        if i+5 < len(prog) and prog[i+5] in "0123456789":
            return (prog[i:i+6], i+6)
        else:
            return (prog[i:i+5], i+5)
    
    lp = prog.find('(', i)
    assert i != -1

    func = prog[i:lp]
    if func in ("constString", "constInt", "constDouble"):
        end = prog.find(')', lp)
        assert end != -1
        s = prog[lp+1: end]
        if end != len(prog)-1:
            assert prog[end+1] in ",)"
        ast = [func, [s]]
        return (ast, end+1)
    else:
        i = lp + 1
        children = []
        while True:
            (child, i) = parse_prog(prog, i)
            children.append(child)
            if prog[i] == ')':
                break
            i += 2
        ast = [func, children]
        return (ast, i+1)

tofunc0 = {
    "string_array0": "array",
}

tofunc = {
    "any_array1_int": "array",
    "any_array1_string": "array",
    "any_array1_astring": "array",
    "any_array1_any": "array",
    "any_array2_any_int": "array",
    "any_array2_any_string": "array",
    "any_array2_any_astring": "array",
    "any_array2_any_any": "array",
    "any_array2_int_int": "array",
    "any_array2_int_string": "array",
    "any_array2_int_astring": "array",
    "any_array2_int_any": "array",
    "any_array2_string_int": "array",
    "any_array2_string_string": "array",
    "any_array2_string_astring": "array",
    "any_array2_string_any": "array",
    "any_array2_astring_int": "array",
    "any_array2_astring_string": "array",
    "any_array2_astring_astring": "array",
    "any_array2_astring_any": "array",
    "any_array_concat": "concat",
    "astring_len": "size",
    "concat": "concat",
    "if_astr": "if",
    "if_bool": "if",
    "if_int": "if",
    "if_str": "if",
    "if_double": "if",
    "length": "length",
    "locate2": "locate",
    "lower": "lower",
    "map_string_any_concat": "concat",
    "map_string_any_from_arrays": "map_from_arrays",
    "map_string_any_keys": "map_keys",
    "map_string_any_values": "map_values",
    "pow": "pow",
    "replace2": "replace",
    "string_any_array_zip": "arrays_zip",
    "string_array1": "array",
    "string_array2": "array",
    "string_array_concat": "concat",
    "string_array_contains": "array_contains",
    "string_array_intersect": "array_intersect",
    "string_array_join": "array_join",
    "substring2": "substring",
    "substring_index": "substring_index",
    "trim": "trim",
    "not": "not",
    "row": ""
}

tobinop = {
    "add": "+",
    "addD": "+",
    "sub": "-",
    "subD": "-",
    "mul": "*",
    "mulD": "*",
    "div": "/",
    "divD": "/",
    "mod": "%",
    "eq": "=",
    "eq_double": "=",
    "eq_str": "=",
    "neq": "!=",
    "and": "and",
    "or": "or",
    "le": "<=",
    "le_double": "<=",
    "lt": "<",
    "lt_double": "<"
}

tocast = {
    "cast_astring2any": "",
    "cast_int2any": "",
    "cast_int2str": "string",
    "cast_double2str": "string",
    "cast_str2any": "",
    "cast_str2int": "int",
    "cast_str2double": "double"
}

tosubscr = {
    "astring_get",
}

toconst = {
    "constInt",
    "constString",
    "constDouble"
}

pos_adjust = {
    "substring_index": [2],
    "substring": [1,2],
    "[]": [1],
    "locate": [2],
}

def do_translate(ast):
    name = ast[0]
    if name == '@':
        return
    if name in tofunc0:
        ast[0] = tofunc0[name]
        ast[1] = []
        return
    
    if name in tofunc:
        ast[0] = tofunc[name]
        for t in ast[1]:
            do_translate(t)
        return

    if name in tobinop:
        assert len(ast[1]) == 2
        ast[0] = tobinop[name]
        do_translate(ast[1][0])
        do_translate(ast[1][1])
        return

    if name in tocast:
        assert len(ast[1]) == 1
        ast[0] = "cast"
        do_translate(ast[1][0])
        ast[1].append(tocast[name])
        return

    if name in tosubscr:
        assert len(ast[1]) == 2
        ast[0] = '[]'
        do_translate(ast[1][0])
        do_translate(ast[1][1])
        return

    if name in toconst:
        assert len(ast[1]) == 1
        return

    assert False

def do_print(ast, indent, *args):
    name = ast[0]
    if name == '@':
        return indent + args[int(ast[4:])]

    if name == '':
        return ',\n'.join([do_print(t, '', *args) for t in ast[1]])
    if name == 'cast':
        assert len(ast[1]) == 2
        if ast[1][1] == "":
            return do_print(ast[1][1], indent, *args)
        else:
            return f"""{indent}cast(
{do_print(ast[1][0], indent+' ', *args)} as {ast[1][1]}
{indent})"""

    if name == '[]':
        assert len(ast[1]) == 2
        array = do_print(ast[1][0], indent, *args)
        index = do_print(ast[1][0], indent + ' ', *args)
        return f"""{array}[
{index}+1
{indent}]"""

    if name in toconst:
        assert len(ast[1]) == 1
        if name == 'constInt' or name == 'constDouble':
            return indent + ast[1][0]
        if name == 'constString':
            return f"{indent}'{ast[1][0]}'"
        assert False

    if name in tobinop.values():
        assert len(ast[1]) == 2
        arg0 = do_print(ast[1][0], indent + ' ', *args)
        arg1 = do_print(ast[1][1], indent + ' ', *args)
        return f"""{indent}({arg0.strip()})
{indent + ' '}{name}
{indent}({arg1.strip()})"""

    if name[0] in 'abcdefghijklmnopqrst':
        arglist = []
        for i in range(len(ast[1])):
            child = ast[1][i]
            r = do_print(child, indent + ' ', *args)
            if name in pos_adjust and i in pos_adjust[name] and r[-2:] != '-1':
                r = r + ' + 1'
            arglist.append(r)
        arglist = ",\n".join(arglist)
        return f"""{indent}{name}(
{arglist}
{indent})"""

    assert False

def do_optimize_concat(ast):
    if ast[0] != 'concat':
        return

    while ast[1][0][0] == 'concat':
        ast[1] = ast[1][0][1] + ast[1][1:]

    while True:
        for i in range(0, len(ast[1])):
            if ast[1][i][0] == 'concat':
                found = True
                break
            found = False
        if not found:
            break
        ast[1] = ast[1][:i] + ast[1][i][1] + ast[1][i+1:]
        

def do_optimize_array(ast):
    if ast[0] != 'concat':
        return
    
    if ast[1][0][0] != 'array':
        return

    for t in ast[1]:
        assert t[0] == 'array'

    ast[0] = 'array'
    args = []
    for t in ast[1]:
        args = args + t[1]
    ast[1] = args

def do_optimize_if(ast):
    if ast[0] != 'if':
        return

    if ast[1][0] == ast[1][1]:
        ast[0] = 'or'
        ast[1] = [ast[1][0], ast[1][2]]
    elif ast[1][0] == ast[1][2]:
        ast[0] = 'and'
        ast[1] = [ast[1][0], ast[1][1]]

def do_optimize(ast):
    if type(ast) != list:
        return
    name = ast[0]
    if name in toconst:
        return

    do_optimize_concat(ast)
    do_optimize_array(ast)
    do_optimize_if(ast)

    for t in ast[1]:
        do_optimize(t)

def translate(prog, *args):
    (ast, i) = parse_prog(prog)
    assert i == len(prog)
    do_translate(ast)
    # pprint(ast)
    do_optimize(ast)
    return do_print(ast, '', *args)

def translate_exp(id, *args):
    for l in open(f"experiments/{id}/comp.log"):
        c = l
    c = c.strip()
    assert c[29:43] == 'Composed SQL: '
    trinity=c[43:]
    print(trinity)

    if len(args) == 0:
        for l in open(f"experiments/{id}/all.py"):
            c = l
        assert c[0] == '#'
        c = c[1:].strip()
        args = [a.strip() for a in c.split(',')]
    
    print(translate(trinity, *args))



if __name__  == "__main__":
    import sys
    translate_exp(sys.argv[1], *sys.argv[2:])
