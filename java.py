import os
import re
import regex

words = {
'Modificadores de acesso' : ['private', 'protected', 'public'],
'Modificadores de classes, variáveis ou métodos' : ['abstract', 'class', 'extends', 'final', 'implements', 'interface', 'native', 'new', 'static', 'strictfp', 'synchronized', 'transient', 'volatile'],
'Controle de fluxo dentro de um bloco de código': ['break', 'case', 'continue', 'default', 'do', 'else', 'for', 'if', 'instanceof', 'return', 'switch', 'while'],
'Tratamento de erros' : ['assert', 'catch', 'finally', 'throw(s|)', 'try'],
'Controle de pacotes' : ['import', 'package'],
'Primitivos' : ['boolean', 'byte', 'char', 'double', 'float', 'int', 'long', 'short'],
'Variáveis de referência' : ['super', 'this'],
'Retorno de um método' : ['void'],
'Palavras reservadas não utilizadas' : ['const', 'goto']
#'Sinalizações': ['\+','\-','\/','\%','\=']
}

patterns = {

'numbers'    : r'[0-9]+[\.]*',
'parameters' : r'[A-Za-z0-9\[\]\,\s*]*',
'identifier' : r'[\s]*[A-Za-z0-9]+[\s]*',
'expressios' : r'[A-Za-z0-9]+[\+\-\*\/]+[\(\)]*[\s]*',
'function'   : r'([A-Za-z0-9]+[\s]*(\([A-Za-z0-9\[\]\,\s]*\)))'

}


#r"([A-Za-z0-9]+[\s]*\(([A-Za-z0-9\[\]\,\s]*)\))"


def recognize(phrase):
    result = []
    middle_pattern = patterns['function']
    mp = regex.compile(middle_pattern)
    # return mp.findall(phrase)[0][1]
    if mp.findall(phrase):
        params = mp.findall(phrase)[0][1]
        return params[1:-1].split(',') # regex.split(r'(\,)', params[1:-1])


print(recognize(" virgula(String s1, int i2){}"))
print(recognize(" virgula (String s1 , int i2)"))
print(recognize(" virgula(String s1)"))
print(recognize(" virgula(s1, i2)"))
print(recognize(" virgula(s1)"))
print(recognize(" (virgula)"))
