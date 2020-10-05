import sys
import json
import xml.dom.minidom as dom

def is_failed(p):
    return p['status'] == 'FAILURE' and \
        'java::cegis.product.Jassert.assert_equal' in p['property'] and \
        'assertion' in p['property']

def parse_input(input, trace):
    assert('Product.product' in input['sourceLocation']['function'])
    
    value = input['values'][0]
    tpe = value['type']
    if tpe == 'int':
        return value['data']
    elif tpe == 'struct java.lang.String *' or tpe == 'const struct java.lang.String *':
        objname = value['data']
        assigns = [i for i in trace if i['stepType'] == 'assignment']
        assign = [a for a in assigns if a['lhs'] == objname][0]
        m_length = [a for a in assigns if a['lhs'] == f"{objname}.length"]
        m_data = [a for a in assigns if a['lhs'] == f"{objname}.data"]
        assert(len(m_length) > 0)
        assert(len(m_length) == len(m_data))
        m_length, m_data = m_length[-1], m_data[-1]
        assert(m_length['value']['type'] == 'int')
        if m_length['value']['data'] == '0':
            return '""'
        else:
            raise Exception(f"Not implemented string with {m_length} and {m_data}")
    else:
        raise Exception(f"Not implemented input type {tpe}")

def parse_jbmc_json_result(j):
    r = [i for i in j if 'result' in i][0]['result']
    f = [i for i in r if is_failed(i)]
    if len(f) == 0:
        return None

    assert(len(f) == 1)
    t = f[0]['trace']
    inputs = [i for i in t if i['stepType'] == 'input']
    ce = [parse_input(input, t) for input in inputs]
    return ce

def parse_jbmc_result(filename):
    j = json.load(open(filename))
    return parse_jbmc_json_result(j)

def get_xml_childNodes(node, tag):
    return [n for n in node.childNodes if n.nodeName == tag]


def is_failed_xml(n):
    return n.getAttribute('status') == 'FAILURE' and \
        'java::cegis.product.Jassert.assert_equal' in n.getAttribute('property') and \
        'assertion' in n.getAttribute('property')

def parse_xml_array_object_value(trace, objname):
    assigns = get_xml_childNodes(trace, 'assignment')
    array_assign = [n for n in assigns if get_xml_childNodes(n, "full_lhs")[0].childNodes[0].data == objname]
    value = get_xml_childNodes(array_assign[-1], 'full_lhs_value')[0].childNodes[0].data
    assert(value[0] == '{')
    assert(value[-1] == '}')
    value1 = f"[{value[1:-1]}]"
    s = "".join(eval(value1))
    return s


def parse_xml_string_object_value(trace, objname):
    assigns = get_xml_childNodes(trace, 'assignment')
    m_length = [n for n in assigns if get_xml_childNodes(n, "full_lhs")[0].childNodes[0].data == f"{objname}.length"]
    m_data = [n for n in assigns if get_xml_childNodes(n, "full_lhs")[0].childNodes[0].data == f"{objname}.data"]
    assert(len(m_length) > 0)
    assert(len(m_data) == len(m_length))
    m_length, m_data = m_length[-1], m_data[-1]
    length = int(get_xml_childNodes(m_length, "full_lhs_value")[0].childNodes[0].data)
    arrayobj = get_xml_childNodes(m_data, "full_lhs_value")[0].childNodes[0].data
    return parse_xml_array_object_value(trace, arrayobj)

def parse_xml_input(input, trace):
    location = get_xml_childNodes(input, 'location')[0]
    assert('Product.product' in location.getAttribute('function'))

    id = get_xml_childNodes(input, 'input_id')[0].childNodes[0].data
    value = get_xml_childNodes(input, 'value')[0].childNodes[0].data
    if id[-1] == 'a':
        objname = value[1:]
        return parse_xml_string_object_value(trace, objname)
    elif id[-1] == 'i':
        return int(value)
    else:
        raise Exception(f"not implemented input type for {id}")

def parse_jbmc_xml_result(d):
    root = d.documentElement
    results = get_xml_childNodes(root, "result")
    result = [r for r in results if is_failed_xml(r)]
    if len(result) == 0:
        return None
    
    assert(len(result) == 1)
    trace = get_xml_childNodes(result[0], 'goto_trace')[0]
    inputs = get_xml_childNodes(trace, 'input')
    ce = [parse_xml_input(i, trace) for i in inputs]
    return ce



if __name__ == '__main__':
    import sys
    ce = parse_jbmc_result(sys.argv[1])
    if ce is None:
        sys.exit(0)
    print(" ".join(ce))

