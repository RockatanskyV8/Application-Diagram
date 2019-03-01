import os
import re
from java import *

def remove_comments(string):
    pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
    # first group captures quoted strings (double or single)
    # second group captures comments (//single-line or /* multi-line */)
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    def _replacer(match):
        # if the 2nd group (capturing comments) is not None,
        # it means we have captured a non-quoted (real) comment string.
        if match.group(2) is not None:
            return "" # so we will return empty to remove the comment
        else: # otherwise, we will return the 1st group
            return match.group(1) # captured quoted-string
    return regex.sub(_replacer, string)

def code_list(startpath):
    code_files = []
    for root, dirs, files in os.walk(startpath):
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            if '.java' in f:
                code_files.append([root + "/" + f, f])
    return code_files

def files_info(filepath, conection):
    result = ""
    total = ""
    with open(filepath) as f:
        for line in f:
            total = total + line
    aux = remove_comments(total).split("\n")
    for line in aux:
        if conection in line and filepath.split("/")[-1] not in result :
            result = result + "" + filepath.split("/")[-1]
    return result

def find_connection(path, name):
    result = []
    for l in code_list(path):
        aux = l[1].split(".")[0]
        if aux != name and files_info(l[0], name):
            result.append(files_info(l[0], name))
    return result

def list_files(startpath = 'file/path'):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        if '.git' in dirs:
            dirs.remove('.git')
        for f in files:
            if '.java' in f:
                print('{}{}'.format(subindent, f), find_connection(startpath, f.split(".")[0]))

list_files()
