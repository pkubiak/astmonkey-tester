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
> python3 tester.py -l ./tests/
```

```python
./tests/longstring.py: SyntaxError [invalid syntax (<unknown>, line 3)]
./tests/ifexp.py: AssertionError []
./tests/asyncwith.py: AssertionError []
./tests/strstr.py: AssertionError []
./tests/multiimport.py: SyntaxError [invalid syntax (<unknown>, line 1)]
./tests/nestedif.py: SyntaxError [invalid syntax (<unknown>, line 3)]
./tests/kwonlyargs.py: AssertionError []
./tests/visualindent.py: SyntaxError [invalid syntax (<unknown>, line 2)]
./tests/rstring.py: AssertionError []
./tests/matmul.py: KeyError [<class '_ast.MatMult'>]
./tests/elif.py: SyntaxError [invalid syntax (<unknown>, line 3)]
./tests/tryelse.py: AssertionError []
./tests/strannotation.py: SyntaxError [invalid syntax (<unknown>, line 1)]

Success: 0 / 13 = 0.00%
```


## Test Cases ##
Directory `tests/` contains samples codes which raise exception when test with following code:
```python
import ast
from astmonkey import visitors

code = "..."
node = ast.parse(code)
code_gen = visitors.to_source(node)
node_gen = ast.parse(code_gen)

assert ast.dump(node) == ast.dump(node_gen)
```
