# astmonkey-tester #


Simple script for validating output of `astmonkey` library (https://github.com/mutpy/astmonkey) on different python files.

## Requirements ##

* `python` > 3.6.0
* `meld` executable for meld diff
* `diff` executable for standard diff
* `astmonkey` library

## Usage ##

```bash
> python3 tester.py -h
```

```python
usage: tester.py [-h] [-b BRANCH] [-i] [-l] path

Validate astmonkey library on python files from given github repository.

positional arguments:
  path                  GitHub repo url or name

optional arguments:
  -h, --help            show this help message and exit
  -b BRANCH, --branch BRANCH
                        Branch name
  -i, --interactive     Run in interactive mode, allow investigating bugs
  -l, --local           Interpret given url as local file path
```

### Test github code ###
Test `astmonkey` on python code from github repository:

```bash
> python3 tester.py -i https://github.com/mutpy/astmonkey
```

```python
astmonkey-master/astmonkey/__init__.py: OK
astmonkey-master/astmonkey/tests/__init__.py: OK
astmonkey-master/astmonkey/tests/test_transformers.py: OK
astmonkey-master/astmonkey/tests/test_utils.py: OK
astmonkey-master/astmonkey/tests/test_visitors.py: OK
astmonkey-master/astmonkey/tests/utils.py: OK
astmonkey-master/astmonkey/transformers.py: OK
astmonkey-master/astmonkey/utils.py: OK
astmonkey-master/astmonkey/visitors.py: SyntaxError [invalid syntax (<unknown>, line 59)]
  Compare results [next / diff code / meld code / diff ast / quit]: n

astmonkey-master/examples/edge-graph-node-visitor.py: OK
astmonkey-master/examples/graph_node_visitor.py: OK
astmonkey-master/examples/is_docstring.py: OK
astmonkey-master/examples/parent_node_transformer.py: OK
astmonkey-master/examples/source_generator_node_visitor.py: OK
astmonkey-master/setup.py: OK

Success: 14 / 15 = 93.33%
```

### Run test cases ###
Test `astmonkey` on local filest (from path or directory):

```bash
> python3 tester.py -l ./bugs/
```

```python
./bugs/longstring.py: SyntaxError [invalid syntax (<unknown>, line 3)]
./bugs/ifexp.py: AssertionError []
./bugs/asyncwith.py: AssertionError []
./bugs/strstr.py: AssertionError []
./bugs/multiimport.py: SyntaxError [invalid syntax (<unknown>, line 1)]
./bugs/nestedif.py: SyntaxError [invalid syntax (<unknown>, line 3)]
./bugs/kwonlyargs.py: AssertionError []
./bugs/visualindent.py: SyntaxError [invalid syntax (<unknown>, line 2)]
./bugs/rstring.py: AssertionError []
./bugs/matmul.py: KeyError [<class '_ast.MatMult'>]
./bugs/elif.py: SyntaxError [invalid syntax (<unknown>, line 3)]
./bugs/tryelse.py: AssertionError []
./bugs/strannotation.py: SyntaxError [invalid syntax (<unknown>, line 1)]

Success: 0 / 13 = 0.00%
```

## Complex test suit ## 
To test probably all python features, you can use `python/cpython` repo:

```bash
> python3 tester.py python/cpython
```

```python
<many lines>

Success: 1124 / 1850 = 60.76%
```

## Test Cases ##
Directory `bugs/` contains samples codes which raise exception when test with following code:
```python
import ast
from astmonkey import visitors

code = "..."
node = ast.parse(code)
code_gen = visitors.to_source(node)
node_gen = ast.parse(code_gen)

assert ast.dump(node) == ast.dump(node_gen)
```
