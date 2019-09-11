import os
import re
import regex
# from java import *

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

def recognize_keywords(params):
    m = []
    for i in params[0].split(" "):
        for w in words:
            if i in words[w]:
                m.append(i)
    print(params, m)

def recognize_function(phrase):
    result = []
    middle_pattern = r"[\s]([A-Za-z0-9]+[\s]*\([A-Za-z0-9\[\]\,\s*]*\))"
    end_pattern = r"\{"
    mp = re.compile(middle_pattern)
    ep = re.compile(end_pattern)
    matches = []
    if (mp.search(phrase) and ep.search(phrase)):
        matches = mp.search(phrase) # [mp.search(phrase), ep.search(phrase)]
    return matches

def separate_function(phrase):
    b, e = recognize_function(phrase).span()
    components = (phrase[:b].split(" "), phrase[b+1:e], (phrase[e+1:-1].strip()).split(" "))
    return components

def recognize_blocks(phrase):
    pattern = r"{$"
    reg = re.compile(pattern)
    return reg.search(phrase)

def separate(text):
    pattern = r"(\".*?\"|\'.*?\')|([\{\};])"
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    matches = regex.finditer(text)
    # for m in matches:
    #     print(m)
    indices = [0]
    [(indices.append(m.span()[0]+1), indices.append(m.span()[1])) for m in matches if m.group(1) is None]
    result = [text[i:j].strip() for i,j in zip(indices, indices[1:]+[None]) if text[i:j]]
    return result

def function_content(line, func):
    # print("func", func)
    # print("line", line)
    pattern1 = regex.compile(r'\{((?:[^{}]|(?R))*)\}')
    result = ""
    for s in pattern1.search(line).captures(1):
        if (func + s + '}') in line:
            result = s
    return result

def block_content(line, bloc):
    # print("func", func)
    # print("line", line)
    pattern1 = regex.compile(r'\{((?:[^{}]|(?R))*)\}')
    result = ""
    for s in pattern1.search(line).captures(1):
        if (bloc + s + '}') in line:
            result = s
    return result


def files_info(file, file_name):
    result = {}
    name = file_name.split('.')[0]
    print()
    with open(file) as f:
        total = ""
        for line in f:
            total = total + line     # (line.replace("\t", ""))
        aux = remove_comments(total) # .replace("\n", "")
        print(name)
        for s in separate(aux):
            if recognize_function(s):
                result[s] = function_content(aux, s)
    return result

def list_files(startpath = 'file'):
    for root, dirs, files in os.walk(startpath):
        for f in files:
            if ".java" in f:
                # files_info(root + '/' + f, f)
                detalhes = files_info(root + '/' + f, f)
                for d in detalhes:
                    print(separate_function(d), ":")
                    # print("united\n", detalhes[d], "\n")
                    parts = separate(detalhes[d])
                    # print(parts)
                    for det in parts:
                        # print(det.replace("\n", "").replace("\t", ""))
                        if recognize_blocks(det):
                            print(det.replace("\n", "").replace("\t", "")) #, ":", block_content(detalhes[d], det))
                    print("\n\n")

list_files()
