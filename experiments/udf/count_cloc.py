
import os, glob, re
from pprint import pprint

model_dir = os.path.dirname(os.path.realpath(__file__)) + "/../../scala2c/models"

def extract_func(seg):
    lines = seg.split("\n")
    for i in range(len(lines)):
        l = lines[i]
        if re.search('^[^ ]', l) and re.search('\(', l):
            func_name = re.findall('([^ ]*)\(', l)
            assert len(func_name) == 1
            return (func_name[0], lines[i+1:])

    assert False, f"Cannot find function in {seg}"

def collect_model_funcs_from_c(src):
    buf = open(src).read()
    assert buf[-5:] == '\n}\n\n\n', f"invalid end of {src}"
    segments = buf.split("\n}\n\n\n")
    return [extract_func(seg) for seg in segments if seg]
        

def collect_model_funcs():
    model_files = glob.glob(f"{model_dir}/*.c")
    funcs=[]
    for f in model_files:
        # print(f)
        funcs = funcs + collect_model_funcs_from_c(f)

    funcs_with_calls = dict(funcs)
    assert len(funcs) == len(funcs_with_calls)

    for f in funcs_with_calls:
        body = funcs_with_calls[f]
        words = re.findall('\w+', '\n'.join(body))
        calls = set([w for w in words if w in funcs_with_calls])
        funcs_with_calls[f] = [len(body), calls]

    last_total_calls = -1
    total_calls = sum([len(v[1]) for v in funcs_with_calls.values()])
    while last_total_calls != total_calls:
        last_total_calls = total_calls
        for f in funcs_with_calls:
            calls = funcs_with_calls[f][1]
            calls_bak = list(calls)
            for c in calls_bak:
                calls = calls.union(funcs_with_calls[c][1])
            funcs_with_calls[f][1] = calls
        total_calls = sum([len(v[1]) for v in funcs_with_calls.values()])

    return funcs_with_calls


if __name__ == '__main__':
    pprint(collect_model_funcs())
