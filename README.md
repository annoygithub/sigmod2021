<meta name="robots" content="noindex">

# Overview

This repository contains the code, data, and tools that we use to produce the results reported in the paper.

* `cegis/` implements the algorithm of lazy inductive synthesis.

* `experiments/` has all the benchmarks, including UDFs, TPC-H queries, and real applications.

* `scala2c/` is our prototype of Scala-to-C translator.

* `udf_extractor/` contains the tools used to extract UDFs from Github.

* `third_party/` has two off-the-shelf tools (Trinity and cbmc) that we used in our synthesizer. We fixed some bugs and slightly adjusted the original code to meet our needs.
  * [Trinity](https://fredfeng.github.io/Trinity/) is a program-by-example synthesizer
  * [cbmc](https://www.cprover.org/cbmc/) is a bounded model checker for programs written in C.



# Synthesizer

## Prerequisites

* Python 3.6 or above
* jinja2
```
pip3 install jinja2
```
* Trinity
```
cd third_party/Trinity
pip3 install .
```
* cbmc
```
cd third_party/cbmc/src
make DOWNLOADER=wget minisat2-download
make
```
* C models
```
cd scala2c/models
make
```
## Run
The following command runs **compositional** synthesis on a UDF:
```
python3 experiments/udf/4048/udf.py comp
```

The `.py` file contains the UDF translated to C. The original UDF is in the corresponding `.scala` file: `experiments/udf/4048/udf.scala`

To run **non-compositional** systhesis, simply execute the `.py` file:
```
python3 experiments/udf/4048/udf.py
```
