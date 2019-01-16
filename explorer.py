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

def list_files(startpath = '/your/application/path'):
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

# def files_info(filepath, conection):
#     result = ""
#     with open(filepath) as f:
#         for line in f:
#             if conection in line and filepath.split("/")[-1] not in result :
#                 result = result + "" + filepath.split("/")[-1]
#     return result

# def list_files():
#     for dirname, dirnames, filenames in os.walk('/your/application/path'):
#         # print path to all subdirectories first.
#         for subdirname in dirnames:
#             print(os.path.join(dirname, subdirname))
#
#         # print path to all filenames.
#         for filename in filenames:
#             print(os.path.join(dirname, filename)) #, files_info(os.path.join(dirname, filename)))
#
#         # Advanced usage:
#         # editing the 'dirnames' list will stop os.walk() from recursing into there.
#         if '.git' in dirnames:
#             # don't go into any .git directories.
#             dirnames.remove('.git')
#
# # list_files()

# def list_files(startpath = '/your/application/path'):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         if '.git' in dirs:
#             dirs.remove('.git')
#         for f in files:
#             if '.java' in f:
#                 print('{}{}'.format(subindent, f), root + "/" + f)
#                 #print('{}{}'.format(subindent, root + "/" + f))

#list_files()

# def remove_comments(string):
#     pattern = r"(\".*?\"|\'.*?\')|(/\*.*?\*/|//[^\r\n]*$)"
#     # first group captures quoted strings (double or single)
#     # second group captures comments (//single-line or /* multi-line */)
#     regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
#     def _replacer(match):
#         # if the 2nd group (capturing comments) is not None,
#         # it means we have captured a non-quoted (real) comment string.
#         if match.group(2) is not None:
#             return "" # so we will return empty to remove the comment
#         else: # otherwise, we will return the 1st group
#             return match.group(1) # captured quoted-string
#     return regex.sub(_replacer, string)
#
# #print(re.escape(text))
# def getWords(phrase):
#     result = []
#     indices = []
#     for w in words:
#         for t in words[w]:
#             r = re.compile(r'\b'+ t)
#             matches = r.finditer(phrase)
#             for m in matches:
#                 indices.append(m.span()[0])
#                 indices.append(m.span()[1])
#     indices = sorted(indices)
#     if indices != []:
#         [result.append(phrase[i:j].strip()) for i,j in zip(indices, indices[1:]+[None])]
#     else:
#         result.append(phrase)
#     return [r for r in result if r]
#
# def separate(text):
#     res = ((text.replace("{", "\n{\n")).replace("}", "\n}\n")).replace(";", "\n")
#     result = []
#     indices = [0]
#     pattern = r"(\".\s*?\"|\'.\s*?\')|(\s)"
#     regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
#     match = regex.finditer(res)
#     for m in match:
#         if m.group(1) is None and m.group(2) != ' ':
#             aux = m.span()
#             indices.append(aux[0])
#             indices.append(aux[1])
#     [result.append(res[i:j].strip()) for i,j in zip(indices, indices[1:]+[None])]
#     return [getWords(r) for r in result if r]
#
# def files_info(file):
#     print()
#     print(file, '\n')
#     with open(file) as f:
#         total = ""
#         for line in f:
#             total = total + (line.replace("\t", ""))
#         result = remove_comments(total).replace("\n", "")
#         for r in separate(result):
#             print(r)
