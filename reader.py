import os
import re
import regex
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

def recognize(phrase):
    def recognize_class(phrase):
        pattern = r"class ([A-Za-z0-9]+)"
        r = re.compile(pattern)
        matches = r.search(phrase)
        return matches

    def recognize_function(phrase):
        pattern = r"[A-Za-z0-9]+[\s]*\([A-Za-z0-9\s*]*\)$"
        r = re.compile(pattern)
        matches = r.search(phrase)
        return matches

    if recognize_class(phrase):
        return recognize_class(phrase).group(1)
    elif recognize_function(phrase):
        return recognize_function(phrase).group()

def getWords(phrase):
    indices = []
    for w in words:
        for t in words[w]:
            r = re.compile(r'\b'+ t)
            matches = r.finditer(phrase)
            for m in matches:
                indices.append(m.group())
    if indices and recognize(phrase) :
        return [recognize(phrase), indices]

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
    return [getWords(r) for r in result if r and getWords(r) is not None]

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

def list_files(startpath = 'file/path'):
    for root, dirs, files in os.walk(startpath):
        for f in files:
            if ".java" in f:
                files_info(root + '/' + f)

list_files()
