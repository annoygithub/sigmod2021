import os
import pprint
import logging

LOG = logging.getLogger("dfg")

LIBRARY_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../../scala2c/models/'
LIBRARY_SOURCES = ["String.c"]

def collect_lib_dfgs():
    lib_dfgs = {}
    for src in LIBRARY_SOURCES:
        func = None
        for line in open(LIBRARY_PATH + src):
            if line[:5] == '"""*/':
                # print(dfg)
                dfg = eval(dfg)
                assert len(dfg["returns"]) == 1 and dfg["returns"][0] == len(dfg["blocks"]), pprint.pformat(dfg)
                lib_dfgs[func] = dfg
                func = None
            elif func is not None:
                dfg += line
            elif line[:5] == '/*"""':
                func = line.strip()[5:]
                dfg = ""
            
    # pprint.pprint(lib_dfgs)
    return lib_dfgs
library_dfgs = collect_lib_dfgs()           


class Expr:
    def __init__(self, op, opnds, inputs):
        self.op = op
        self.opnds = opnds
        self.inputs = inputs
    def __repr__(self):
        return f"Expr(op={self.op}, opnds={self.opnds}, inputs={self.inputs})"
    def __str__(self):
        if self.op == '()':
            return f"{self.opnds[0]}({', '.join([str(o) for o in self.opnds[1:]])})"
        elif self.op == '?:':
            return f"{self.opnds[0]} ? {self.opnds[1]} : {self.opnds[2]}"
        elif self.op in ('-', '+', '*', '/', '==', '!=', '&&', '||', '>', '<', '->', '%', '<=', '>='):
            return f"{self.opnds[0]} {self.op} {self.opnds[1]}"
        elif self.op in ('!'):
            return f"{self.op} {self.opnds[0]}"
        else:
            raise Exception(f"Unknown Expr op {self.op}")

class Stmt:
    def __init__(self, tpe, terms, pos):
        self.tpe = tpe
        self.terms = terms
        self.pos = pos
    def __repr__(self):
        return f"Stmt(tpe={self.tpe}, terms={self.terms})"
    def __str__(self):
        if self.tpe == '=':
            return f"{self.terms[0]} {self.terms[1]} = {str(self.terms[2])};"
        else:
            raise Exception(f"Unknown Stmt tpe {self.tpe}")

def get_number(s, i):
    j = i
    while s[j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        j += 1
    if s[j] == '.':
        j += 1
        while s[j] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            j += 1
    return s[i:j]

def get_id(s, i):
    j = i
    while (ord('a') <= ord(s[j]) and ord(s[j]) <= ord('z')) or \
            (ord('A') <= ord(s[j]) and ord(s[j]) <= ord('Z')) or \
            (ord('0') <= ord(s[j]) and ord(s[j]) <= ord('9')) or \
            s[j] == '_':
        j += 1
    return s[i:j]

def get_string(s, i):
    j = i+1
    while s[j] != '"':
        if s[j] == '\\':
            j += 1
        j += 1
    return s[i:j+1]

def get_tokens(s):
    i = 0
    line = 1
    col = 1
    while i < len(s):
        if s[i] in (' ', '\t'):
            i += 1
            col += 1
            continue
        elif s[i] == '\n':
            i += 1
            line += 1
            col = 1
            continue
        elif s[i] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            num = get_number(s, i)
            i += len(num)
            col += len(num)
            yield num
        elif (ord('a') <= ord(s[i]) and ord(s[i]) <= ord('z')) or (ord('A') <= ord(s[i]) and ord(s[i]) <= ord('Z')) or s[i] == '_':
            id = get_id(s, i)
            i += len(id)
            col += len(id)
            yield id
        elif s[i] == '"':
            str = get_string(s, i)
            i += len(str)
            col += len(str)
            yield str
        elif s[i] == '-':
            if s[i+1] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                num = get_number(s, i+1)
                i += len(num) + 1
                col += len(num) + 1
                yield '-' + num
            elif s[i+1] =='>':
                yield '->'
                i += 2
                col += 2
            else:
                yield s[i]
                i += 1
                col += 1
        elif s[i] == '=' and s[i+1] == '=':
            yield '=='
            i += 2
            col += 2
        elif s[i] == '&' and s[i+1] == '&':
            yield '&&'
            i += 2
            col += 2
        elif s[i] == '|' and s[i+1] == '|':
            yield '||'
            i += 2
            col += 2
        elif s[i] == '!' and s[i+1] == '=':
            yield '!='
            i += 2
            col += 2
        elif s[i] == '<' and s[i+1] == '=':
            yield '<='
            i += 2
            col += 2
        elif s[i] == '>' and s[i+1] == '=':
            yield '>='
            i += 2
            col += 2
        elif s[i] in ('(', ')', '"', ',', '=', ';', '?', ':', '>', '!', '{', '}', '+', '-', '*', '/', '<', '%'):
            yield s[i]
            i += 1
            col += 1
        else:
            raise Exception(f"Unknown char '{s[i]}'' at line {line} col {col}")
    assert i == len(s), f"Incomplete parse: line={line}, col={col}, i={i}, len(s)={len(s)}"

def get_func_call(tokens, i):
    opnds = []
    inputs = set()
    opnds.append(tokens[i])
    j = i+1
    while tokens[j] != ')':
        j += 1
        if tokens[j] == ')':
            break
        (expr, j) = get_expr(tokens, j)
        # print(expr)
        opnds.append(expr)
        if type(expr) != Expr:
            inputs.add(expr)
        else:
            inputs = inputs.union(expr.inputs)
        assert tokens[j] in (',', ')'), f"Expect tokens[{j}] in (',',')'), but get {tokens[j]} in {tokens}"
    call = Expr('()', opnds, inputs)
    return (call, j+1)

def get_trinary_expr(tokens, i):
    opnds = []
    inputs = set()
    opnds.append(tokens[i])

    assert tokens[i+1] == '?' , f"Invalid trinary expr at {i} in {tokens}"
    (opnd2, j) = get_expr(tokens, i+2)
    opnds.append(opnd2)

    assert tokens[j] == ':', f"Invalid trinary expr at {j} in {tokens}"
    (opnd3, j) = get_expr(tokens, j + 1)
    opnds.append(opnd3)

    inputs.add(tokens[i])

    if type(opnd2) == Expr:
        inputs = inputs.union(opnd2.inputs)
    else:
        inputs.add(opnd2)
    if type(opnd3) == Expr:
        inputs = inputs.union(opnd3.inputs)
    else:
        inputs.add(opnd3)
    return (Expr('?:', opnds, inputs), j)

def get_binary_expr(tokens, i):
    opnds = []
    inputs = set()
    opnds.append(tokens[i])
    opnds.append(tokens[i+2])
    inputs.add(tokens[i])
    if tokens[i+1] != '->':
        inputs.add(tokens[i+2])
    return (Expr(tokens[i+1], opnds, inputs), i + 3)

def get_unary_expr(tokens, i):
    opnds = [tokens[i+1]]
    inputs = {tokens[i+1]}
    return (Expr(tokens[i], opnds, inputs), i + 2)

def get_expr(tokens, i):
    if tokens[i+1] == '(':
        return get_func_call(tokens, i)
    elif tokens[i+1] in (',', ';', ')', ':'):
        return (tokens[i], i+1)
    elif tokens[i+1] == '?':
        return get_trinary_expr(tokens, i)
    elif tokens[i+1] in ('-', '+', '*', '/', '==', '!=', '&&', '||', '>', '<', '->', '%', '<=', '>='):
        return get_binary_expr(tokens, i)
    elif tokens[i] in ('!'):
        return get_unary_expr(tokens, i)
    else:
        raise Exception(f"Unknown tokens[{i}]={tokens[i]} in {tokens}")

def get_assign_stmt(tokens, i):
    (expr, j) = get_expr(tokens, i+3)
    assert tokens[j] == ';', f"Expect tokens[{j}]=';', but get {tokens[j]} in {tokens}"
    return Stmt('=', [tokens[i], tokens[i+1], expr], (i, j+1))

def get_if_stmt(tokens, i):
    if_stmts = list(get_stmts(tokens, i+5))
    pos = if_stmts[-1].pos[1]
    assert tokens[pos+1] == 'else', f"Expect tokens[{pos+1}]='else', but get {tokens[pos+1]} in {tokens}"
    else_stmts = list(get_stmts(tokens, pos+3))
    pos = else_stmts[-1].pos[1]
    return Stmt('ifelse', [if_stmts, else_stmts], (i, pos+1))

def get_stmts(tokens, i=0):
    while i < len(tokens):
        if tokens[i+2] == '=':
            stmt = get_assign_stmt(tokens, i)
            yield stmt
            i = stmt.pos[1]
        elif tokens[i] == 'if':
            stmt = get_if_stmt(tokens, i)
            yield stmt
            i = stmt.pos[1]
        elif tokens[i] == '}':
            break
        else:
            raise Exception(f"Unknown tokens[{i}]={tokens[i]} in {tokens}")

def parse_body(udf):
    tokens = list(get_tokens(udf['body']))
    return list(get_stmts(tokens))

varcount=0
def new_var():
    global varcount
    varcount += 1
    return f"__t_{varcount}"

def create_expr_block(expr, tpe, variables, blocks):
    var = new_var()
    stmt = Stmt('=', [tpe, var, expr], None)
    create_assign_block(stmt, variables, blocks, inline=False)
    return var

def inline_lib_dfgs(expr, variables, blocks):
    if type(expr) != Expr:
        return expr

    # inline subexpressions first
    inputs = set()
    x = 1 if expr.op == '()' else 0
    for i in range(x, len(expr.opnds)):
        e = inline_lib_dfgs(expr.opnds[i], variables, blocks)
        if type(e) == Expr:
            inputs = inputs.union(e.inputs)
        else:
            inputs.add(e)
        expr.opnds[i] = e
    expr.inputs = inputs

    if expr.op == '()' and expr.opnds[0] in library_dfgs:
        dfg = library_dfgs[expr.opnds[0]]
        # add blocks for args
        for i in range(1, len(expr.opnds)):
            if type(expr.opnds[i]) == Expr:
                var = create_expr_block(expr.opnds[i], dfg["args"][i-1], variables, blocks)
                expr.opnds[i] = var
        # do inlining
        for i, arg in enumerate(dfg["args"]):
            assert arg == variables[expr.opnds[i+1]][1]
        nblock = len(blocks)
        nprepend = nblock
        for bid, block in dfg["blocks"].items():
            nblock += 1
            # print(variables)
            # print(expr)
            # print(block)
            args = [(a[0], a[1], a[2] + nprepend if a[2] > 0 else variables[expr.opnds[-a[2]]][0]) for a in block["args"]]
            b = {
                "body": block["body"],
                "args": args,
                "ret": block["ret"],
                "depth": 1
            }
            if "strings" in block:
                b["strings"] = block["strings"]
            if "ints" in block:
                b["ints"] = block["ints"]
            if "doubles" in block:
                b["doubles"] = block["doubles"]
            blocks[nblock] = b

        # change expr to variable
        expr = new_var()
        variables[expr] = (len(blocks), dfg["blocks"][dfg["returns"][0]]["ret"][1])
    
    return expr

def create_assign_block(stmt, variables, blocks, inline=False):
    if inline:
        stmt.terms[2] = inline_lib_dfgs(stmt.terms[2], variables, blocks)
    inputs = stmt.terms[2].inputs if type(stmt.terms[2]) == Expr else [stmt.terms[2]]
    args = set()
    strings = set()
    doubles = set()
    ints = set()
    for input in inputs:
        if input[0] == '"':
            # ints.add(f'"{len(input)-2}"')
            # ints.add(f'"{2-len(input)}"')
            strings.add(input.replace("\\\\", "\\"))
        elif input[0] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-'):
            if '.' in input:
                doubles.add(f'"{input}"')
            else:
                ints.add(f'"{input}"')
        elif input == 'NULL':
            continue
        elif input in variables:
            args.add((input, variables[input][1], variables[input][0]))
        else:
            LOG.info(f"Unknown input {input} in {stmt}")

    nblock = len(blocks) + 1
    variables[stmt.terms[1]] = (nblock, stmt.terms[0])
    const = stmt.terms[0] != '_Bool' and \
            type(stmt.terms[2]) == str and \
            stmt.terms[2][0] in ('"', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-') and \
            (stmt.terms[2][0] == '"' or int(stmt.terms[2]) < 10)
    blocks[nblock] = {
        "body": str(stmt),
        "args": list(args),
        "ret": (stmt.terms[1], stmt.terms[0]),
        "strings": list(strings),
        "ints": list(ints) if len(ints) > 0 else ['"1"'],
        "doubles": list(doubles),
        "const": const,
        "depth": 2 if type(stmt.terms[2]) == Expr and stmt.terms[2].op == '()' else 1
    }

def create_return_block(var, variables, blocks):
    nblock = len(blocks) + 1
    tpe = variables[var][1]
    i = variables[var][0]
    assert i < 0
    blocks[nblock] = {
        "body": "",
        "args": [(var, tpe, i)],
        "ret": (var, tpe),
        "depth": 0
    }
    return nblock

def create_stmt_blocks(stmts, variables, blocks):
    for stmt in stmts:
        if stmt.tpe == '=':
            create_assign_block(stmt, variables, blocks)
        elif stmt.tpe == 'ifelse':
            create_stmt_blocks(stmt.terms[0], variables, blocks)
            create_stmt_blocks(stmt.terms[1], variables, blocks)
        else:
            raise Exception(f"Unknown stmt type {stmt.tpe} in {stmt}")

# def merge_unsupported_type(dfg):

def merge_dfg_node(dfg, pid, cid, i, merge_depth=True):
    pblock = dfg["blocks"][pid]
    cblock = dfg["blocks"][cid]
    del cblock["args"][i]
    if "sql" in cblock:
        del cblock["sql"]
    cblock["args"] = list(set(cblock["args"]).union(pblock["args"]))
    if "url" in cblock:
        del cblock["url"]
    cblock["body"] = f"{pblock['body']}\n{cblock['body']}"
    cblock["ints"] = list(set(cblock.get("ints", [])).union(set(pblock.get("ints", []))))
    cblock["doubles"] = list(set(cblock.get("doubles", [])).union(set(pblock.get("doubles", []))))
    cblock["strings"] = list(set(cblock.get("strings", [])).union(set(pblock.get("strings", []))))
    if merge_depth:
        cblock["depth"] += pblock["depth"]

def merge_to_children(dfg, bid, merge_depth=True):
    children = []
    for cid, block in dfg["blocks"].items():
        for j, a in enumerate(block['args']):
            if a[2] == bid:
                children.append((cid, j))

    if len(children) > 0:
        for cid, i in children:
            merge_dfg_node(dfg, bid, cid, i, merge_depth)
    
    del dfg["blocks"][bid]

def merge_constant(dfg):
    const_blocks = []
    for bid, block in dfg["blocks"].items():
        if 'const' in block and block['const']:
            const_blocks.append(bid)

    for bid in const_blocks:
        merge_to_children(dfg, bid, merge_depth=False)

def merge_unsupported_type(dfg):
    unsupported_blocks = []
    for bid, block in dfg["blocks"].items():
        if block['ret'][1] in ("Tuple", "Integer", "Tuple3", "Double", "Long"):
            unsupported_blocks.append(bid)
    
    for bid in unsupported_blocks:
        merge_to_children(dfg, bid)

def post_process(dfg):
    merge_unsupported_type(dfg)
    merge_constant(dfg)
    if len(dfg["blocks"]) == 1:
        list(dfg["blocks"].values())[0]["depth"] = 10000
    # remove_childless(dfg)


def fallback(udf):
    ret = udf["ret"]
    if type(ret) != list:
        ret = [ret]
    return {
        "args": [arg[1] for arg in udf["args"]],
        "blocks": {
            1: {
                "body": udf["body"],
                "args": udf["args"],
                "ret": udf["ret"],
                "strings": udf["strings"] if "strings" in udf else [],
                "ints": udf["ints"] if "ints" in udf else ['"1"'],
                "doubles": udf["doubles"] if "doubles" in udf else [],
                "depth": len(udf["body"].split("\n"))
            }
        },
        "returns": [1 for _ in ret]
    }

def gen_dfg(udf):
    if "for(" in udf["body"] or "for (" in udf["body"]:
        LOG.info("Loops are not supported yet, fallback to non-compositional systhesis")
        return fallback(udf)
    stmts = parse_body(udf)

    variables = {}
    for i, arg in enumerate(udf["args"]):
        variables[arg[0]] = (-1 * (i+1), arg[1])

    # gen stmt blocks
    blocks = {}
    create_stmt_blocks(stmts, variables, blocks)

    ret = udf["ret"]
    if type(ret) != list:
        ret = [ret]

    returns = []
    for r in ret:
        i = variables[r[0]][0]
        if i < 0:
            # gen return-only blocks
            returns.append(create_return_block(r[0], variables, blocks))
        else:
            returns.append(i)

    dfg = {
        "args": [arg[1] for arg in udf["args"]],
        "blocks": blocks,
        "returns": returns
    }

    post_process(dfg)

    return dfg
