import os
import re
import regex
from java import *

# def list_files():
#     for dirname, dirnames, filenames in os.walk('/your/application/path'):
#         # print path to all subdirectories first.
#         for subdirname in dirnames:
#             print(os.path.join(dirname, subdirname))
#
#         # print path to all filenames.
#         for filename in filenames:
#             print(os.path.join(dirname, filename), files_info(os.path.join(dirname, filename)))
#
#         # Advanced usage:
#         # editing the 'dirnames' list will stop os.walk() from recursing into there.
#         if '.git' in dirnames:
#             # don't go into any .git directories.
#             dirnames.remove('.git')

# def list_files(startpath = '/your/application/path'):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))

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

#print(re.escape(text))
def getWords(phrase):
    result = []
    indices = []
    for w in words:
        for t in words[w]:
            r = re.compile(r'\b'+ t)
            matches = r.finditer(phrase)
            for m in matches:
                indices.append(m.span()[0])
                indices.append(m.span()[1])
    indices = sorted(indices)
    if indices != []:
        [result.append(phrase[i:j].strip()) for i,j in zip(indices, indices[1:]+[None])]
    else:
        result.append(phrase)
    return [r for r in result if r]

def separate(text):
    res = ((text.replace("{", "\n{\n")).replace("}", "\n}\n")).replace(";", "\n")
    result = []
    indices = [0]
    pattern = r"(\".\s*?\"|\'.\s*?\')|(\s)"
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    match = regex.finditer(res)
    for m in match:
        if m.group(1) is None and m.group(2) != ' ':
            aux = m.span()
            indices.append(aux[0])
            indices.append(aux[1])
    [result.append(res[i:j].strip()) for i,j in zip(indices, indices[1:]+[None])]
    return [getWords(r) for r in result if r]

def files_info(file):
    print()
    print(file, '\n')
    with open(file) as f:
        total = ""
        for line in f:
            total = total + (line.replace("\t", ""))
        result = remove_comments(total).replace("\n", "")
        for r in separate(result):
            print(r)

def list_files(startpath = '/your/application/path'):
    for root, dirs, files in os.walk(startpath):
        for f in files:
            if ".java" in f:
                files_info(root + '/' + f)

list_files()
