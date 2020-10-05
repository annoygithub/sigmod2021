import sys
import json
import xml.dom.minidom as dom

def is_failed(p):
    return p['status'] == 'FAILURE' and 'product.assertion.1' == p['property']

def parse_int(inputs, i):
    return (int(inputs[i]['values'][0]['data']), i+1)

def parse_long(inputs, i):
    return (int(inputs[i]['values'][0]['data'][:-1]), i+1)

def parse_double(inputs, i):
    return (float(inputs[i]['values'][0]['data']), i+1)

def parse_bool(inputs, i):
    return (inputs[i]['values'][0]['data'] == 'TRUE', i+1)

def parse_string(inputs, index):
    size = int(inputs[index]['values'][1]['binary'], 2)
    buf = ""
    for i in range(size):
        buf = buf + chr(int(inputs[index+1+i]['values'][0]['binary'], 2))
    return (buf, index+size+1)

def parse_astring(inputs, index):
    values = inputs[index]['values']
    assert values[1]['type'] == '__CPROVER_size_t'
    size = int(values[1]['binary'], 2)
    ret = []
    index += 1
    for i in range(size):
        (s, index) = parse_string(inputs, index)
        ret.append(s)
    return (ret, index)

def parse_any(inputs, i):
    values = inputs[i]['values']
    tpe = int(values[1]['binary'], 2)
    if tpe == 1:
        (obj, i) = parse_int(inputs, i+1)
    elif tpe == 2:
        (obj, i) = parse_string(inputs, i+1)
    elif tpe == 3:
        (obj, i) = parse_astring(inputs, i+1)
    else:
        raise Exception(f"Unkown type {tpe} of Any")
    return ([tpe, obj], i)

def parse_aany(inputs, i):
    values = inputs[i]['values']
    assert values[1]['type'] == '__CPROVER_size_t'
    size = int(values[1]['binary'], 2)
    arr = []
    i += 1
    for _ in range(size):
        (x, i) = parse_any(inputs, i)
        arr.append(x)
    return (arr[:size], i)

def parse_inputs(inputs):
    ce = []
    i = 0
    while i < len(inputs):
        assert('product' in inputs[i]['sourceLocation']['function'])
        if 'type' not in inputs[i]['values'][0] and inputs[i]['values'][0]['name'] == 'float':
            # deal with the buggy output of double
            (x, i) = parse_double(inputs, i)
            ce.append(x)
            continue
        
        tpe = inputs[i]['values'][0]['type']
        if tpe in ('int', 'signed int', 'unsigned int'):
            (x, i) = parse_int(inputs, i)
        elif tpe in ('signed long int', 'unsigned long int'):
            (x, i) = parse_long(inputs, i)
        elif tpe == '_Bool':
            (x, i) = parse_bool(inputs, i)
        elif tpe == 'String':
            (x, i) = parse_string(inputs, i)
        elif tpe == 'Any':
            (x, i) = parse_any(inputs, i)
        elif tpe == 'AString':
            (x, i) = parse_astring(inputs, i)
        elif tpe == 'AAny':
            (x, i) = parse_aany(inputs, i)
        else:
            raise Exception(f"Not implemented input type {tpe} in inputs[{i}]")
        ce.append(x)
    return ce

def parse_cbmc_json_result(j):
    r = [i for i in j if 'result' in i][0]['result']
    f = [i for i in r if is_failed(i)]
    if len(f) == 0:
        return None

    assert(len(f) == 1)
    t = f[0]['trace']
    inputs = [i for i in t if i['stepType'] == 'input']
    return parse_inputs(inputs)

def parse_cbmc_result(filename):
    j = json.load(open(filename))
    return parse_cbmc_json_result(j)



if __name__ == '__main__':
    import sys
    ce = parse_cbmc_result(sys.argv[1])
    if ce is None:
        sys.exit(0)
    print(ce)

