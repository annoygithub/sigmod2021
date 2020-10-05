import logging
import queue
import pprint
from copy import deepcopy
import cegis
from dfg import gen_dfg

LOG = logging.getLogger("composition")
pp = pprint.PrettyPrinter(indent=4)

def compose_sql(dfg, block):
    args_sql = []
    for arg in block['args']:
        if arg[2] < 0:
            args_sql.append(f"@arg{-arg[2]-1}")
        else:
            args_sql.append(compose_sql(dfg, dfg['blocks'][arg[2]]))
    sql = block['sql']
    for i in range(len(args_sql)):
        sql = sql.replace(f'@param{i}', args_sql[i])
    return sql

def comp_synth(dfg):
    for bid in dfg['blocks']:
        block = dfg['blocks'][bid]
        if 'sql' in block:
            if block['sql'] is None:
                return bid
            continue
        
        LOG.info(f"----------------------Synthesizing block {bid}----------------------")
        LOG.debug(f"\n{pprint.pformat(block)}")
        sql = cegis.c_cegis(block)
        if sql is None:
            block['sql'] = None
            return bid
        else:
            block['sql'] = str(sql)

    # import pdb; pdb.set_trace()
    sqls = list(compose_sql(dfg, dfg['blocks'][i]) for i in dfg['returns'])
    if len(dfg["returns"]) == 1:
        return sqls[0]
    else:
        return f"row({', '.join(sqls)})"

def merge_dfg_node(dfg, pid, cid, i):
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
    cblock["depth"] += pblock["depth"]

def merge_dfg(dfg, bid):
    merged = []

    # collect neighbors (parents and children)
    parents = [(a[2], i) for i, a in enumerate(dfg["blocks"][bid]['args']) if a[2] >= 0]
    children = []
    for cid, block in dfg["blocks"].items():
        for j, a in enumerate(block['args']):
            if a[2] == bid:
                children.insert(0, (cid, j))

    # try merging with all children
    if len(children) > 0:
        for cid, i in children:
            g = deepcopy(dfg)
            merge_dfg_node(g, bid, cid, i)
            if len(children) == 1:
                del g["blocks"][bid]
            merged.insert(0, g)

    # try merging with each parent
    for pid, i in parents:
        g = deepcopy(dfg)
        merge_dfg_node(g, pid, bid, i)
        merged.append(g)

    # import pdb; pdb.set_trace()
    return merged

def synth(udf, refinement=True, debug=False):
    cegis.init(debug)

    LOG.info("Constructing DFG")
    dfg = gen_dfg(udf)

    dfg_queue = [dfg]
    while len(dfg_queue) > 0:
        dfg = dfg_queue[0]
        del dfg_queue[0]
        LOG.info(f"=====================DFG size {len(dfg['blocks'])}======================")
        LOG.debug(f"\n{pprint.pformat(dfg)}")

        sql = comp_synth(dfg)

        if type(sql) == int: # FIXME: hacky
            LOG.info("Synthesized failed")
            if refinement:
                LOG.info("Trying to merge node")
                merged_dfgs = merge_dfg(dfg, bid=sql)
                dfg_queue = merged_dfgs + dfg_queue
            else:
                LOG.info("DFG refinement is disabled, exit with failure")
                return
        else:
            LOG.info(f"Composed SQL: {sql}")
            return sql
    LOG.info("Failed to syntheis with refinement")


if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    # def udf(x: (Int, Int, Int)) = {
    #    val t1 = x._1 + x._2
    #    return (t1+x._3, t1+x._3)
    #}
    dfg = {
        "args": ["Int", "Int", "Int"], # type list of udf args
        "blocks": {
            1: {
                "args": [("a", "Int", -1), ("b", "Int", -2)], # (<name>, <type>, <from>), negative number for udf args
                "ret": ("t1", "Int"),
                "body" : "val t1 = a + b",
                # "sql": "add(@param0, @param1)"
            },
            2: {
                "args": [("t1", "Int", 1), ("c", "Int", -3)],
                "ret": ("t2", "Int"),
                "body" : "val t2 = t1 + c",
                # "sql": "add(@param0, @param1)"
            },
            3: {
                "args": [("t1", "Int", 1), ("c", "Int", -3)],
                "ret": ("t3", "Int"),
                "body" : "val t3 = t1 - c",
                # "sql": "sub(@param0, @param1)"
            }
        },
        "returns": [2, 3],
    }

    print(comp_synth(dfg))
