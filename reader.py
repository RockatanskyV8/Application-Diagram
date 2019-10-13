import os
import re
import regex
#from java import *

def remove_comments(string):
    #font: https://stackoverflow.com/a/18381470/8316383
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

def separators(string):
    pattern = r"(\".*?\"|\'.*?\')|(\W)" #r'([^a-zA-z0-9\"\'\s])'
    matches = regex.finditer(pattern, string)
    indices = [0]
    [(indices.append(m.span()[0]), indices.append(m.span()[1])) for m in matches]
    return [string[i:j].strip() for i,j in zip(indices, indices[1:]+[None]) if string[i:j]]

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

def separate(text):
    pattern = r"(\".*?\"|\'.*?\')|([\{\};])"
    regex = re.compile(pattern, re.MULTILINE|re.DOTALL)
    matches = regex.finditer(text)
    indices = [0]
    [(indices.append(m.span()[0]+1), indices.append(m.span()[1])) for m in matches if m.group(1) is None]
    return [text[i:j].strip() for i,j in zip(indices, indices[1:]+[None]) if text[i:j]]

def function_content(line, func):
    pattern1 = regex.compile(r'\{((?:[^{}]|(?R))*)\}')
    result = ""
    # return(pattern1.search(line).captures(1))
    for s in pattern1.search(line).captures(1):
        if (func + s + '}') in line:
            # print(s.replace("\t", "").split("\n"))
            result = s # repr(s)
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
                # funct = (recognize_function(s))
                result[s] = function_content(aux, s)
    return result

def list_files(startpath = 'file/path'):
    for root, dirs, files in os.walk(startpath):
        for f in files:
            if ".java" in f:
                # files_info(root + '/' + f, f)
                detalhes = files_info(root + '/' + f, f)
                for d in detalhes:
                    #print(d, "\n", repr(detalhes[d]) )
                    aux = (detalhes[d].replace("\t", "").replace("\n", "").replace("}", "")).split(";")
                    print(separate_function(d) , ":\n" )
                    for a in aux:
                        print(separators(a))

list_files('/home/lucas/Scripts/java/fj-21-jdbc')

