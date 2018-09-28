"""
Validate astmonkey library on python files from given github repository.
"""

import argparse, ast, os, re, tempfile, sys
from astmonkey import visitors
import urllib.request
from zipfile import ZipFile

assert sys.version_info >= (3, 6, 0), "Python 3.6.0 required to run script"


def args_parse():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('path', help='GitHub repo url or name')
    parser.add_argument('-b', '--branch', help='Branch name', default='master')
    parser.add_argument('-i', '--interactive', action='store_true', help='Run in interactive mode, allow investigating bugs')
    parser.add_argument('-l', '--local', action='store_true', help='Interpret given url as local file path')

    return parser.parse_args()

def extract_repo_from_url(repo):
    repo = re.sub(r'^(https?://github.com/|git@github.com:)', '', repo)  #git@github.com:TheAlgorithms/Python.git
    repo = re.sub(r'\.git$', '', repo)
    return repo


def compare_files(text_orig, text_gen, command):
    if isinstance(text_orig, str):
        text_orig = text_orig.encode('utf-8')
    if isinstance(text_gen, str):
        text_gen = text_gen.encode('utf-8')

    with tempfile.NamedTemporaryFile('wb', suffix='.orig') as file_orig:
        file_orig.write(text_orig)
        file_orig.flush()

        with tempfile.NamedTemporaryFile('wb', suffix='.gen') as file_gen:
            file_gen.write(text_gen)
            file_gen.flush()

            os.system(command.format(file_orig=file_orig.name, file_gen=file_gen.name))


def meld(text_orig, text_gen):
    compare_files(text_orig, text_gen, "meld {file_orig} {file_gen}")


def diff(text_orig, text_gen):
    compare_files(text_orig, text_gen, "diff -y -B -d  --color=always {file_orig} {file_gen} | less")

def h(text):
    """Highliht text with ANSI markup"""
    return re.sub('_(\w)_', r'\033[1;33m\1\033[0m', text)

def enter_interactive(code_orig, node_orig, code_gen, node_gen):
    while True:
        a = input(h('  Compare results [_n_ext / _d_iff code / _m_eld code / diff _a_st / _q_uit]: '))
        if a == 'n':
            break
        elif a == 'd':
            diff(code_orig, code_gen)
        elif a == 'm':
            meld(code_orig, code_gen)
        elif a == 'a':
            if node_gen is None:
                print('    Generated code is not parsable')
            else:
                dump_orig = ast.dump(node_orig)
                dump_gen = ast.dump(node_gen)

                brackets = re.compile(r'([()\[\]])')
                meld(brackets.sub(r'\1\n', dump_orig), brackets.sub(r'\1\n', dump_gen))
        elif a == 'q':
            exit()
    print()


def test_code_generation(file_name, code_orig, interactive=False):
    print(f"{file_name}: ", end='')

    try:
        node_orig = ast.parse(code_orig)
    except SyntaxError:
        print("\033[1;34mSkipping\033[0m")
        return True


    code_gen = ''
    node_gen = None

    try:
        code_gen = visitors.to_source(node_orig)
        node_gen = ast.parse(code_gen)
        assert ast.dump(node_orig) == ast.dump(node_gen)
    except (SyntaxError, AssertionError, KeyError) as e:
        print("\033[1;31m%s\033[0m \033[31m[%s]\033[0m" % (type(e).__name__, str(e)))
        if interactive:
            enter_interactive(code_orig, node_orig, code_gen, node_gen)

        return False
    else:
        print("\033[1;32mOK\033[0m")
        return True


def summarize(fails, total):
    print('\nSuccess: %d / %d = %.2f%%' % (total-fails, total, 100.0*(total-fails)/total))


def test_repo(args):
    repo, branch = extract_repo_from_url(args.path), args.branch

    zip_url = f"https://codeload.github.com/{repo}/zip/{branch}"
    local_name = f"{repo}/{branch}.zip".replace('/', '_')

    if not os.path.exists(local_name):
        with urllib.request.urlopen(zip_url) as zip_request, open(local_name, 'wb') as output:
            output.write(zip_request.read())

    total = fails = 0
    with ZipFile(local_name) as zip_file:
        for file_name in zip_file.namelist():
            if not file_name.endswith('.py'):
                continue
            code = zip_file.open(file_name).read()
            if not test_code_generation(file_name, code, args.interactive):
                fails += 1
            total += 1
    summarize(fails, total)


def test_local(args):
    path = args.path

    total = fails = 0
    if os.path.isdir(path):
        import glob
        files = glob.glob(os.path.join(path,'**','*.py'), recursive=True)
    else:
        files = [path]

    for file_name in files:
        with open(file_name) as file:
            content = file.read()
            total += 1
            if not test_code_generation(file_name, content, args.interactive):
                fails += 1
    summarize(fails, total)

if __name__ == '__main__':
    args = args_parse()

    try:
        if args.local:
            test_local(args)
        else:
            test_repo(args)
    except KeyboardInterrupt:
        exit()
