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

def recognize_class(phrase):
    pattern = r"class ([A-Za-z0-9]+)\{"
    r = re.compile(pattern)
    matches = r.search(phrase)
    return matches

def recognize_function(phrase):
    pattern = r"[\s][A-Za-z0-9]+[\s]*\([A-Za-z0-9\s*]*\)"
    r = re.compile(pattern)
    matches = r.search(phrase)
    return matches

def separate(text):
    pattern = r"(\".*?\"|\'.*?\')|([\{\};])"
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    matches = regex.finditer(text)
    indices = [0]
    [(indices.append(m.span()[0]), indices.append(m.span()[1])) for m in matches if m.group(1) is None]
    return [text[i:j].strip() for i,j in zip(indices, indices[1:]+[None]) if text[i:j]]

def files_info(file, file_name):
    print()
    print(file, ' ', file_name.split('.')[0], '\n')
    with open(file) as f:
        total = ""
        for line in f:
            total = total + (line.replace("\t", ""))
        aux = remove_comments(total).replace("\n", "")
        for s in separate(aux):
            if recognize_function(s):
                print(recognize_function(s).group())

def list_files(startpath = 'file/path'):
    for root, dirs, files in os.walk(startpath):
        for f in files:
            if ".java" in f:
                files_info(root + '/' + f, f)

list_files()
