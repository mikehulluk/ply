print 'Testing new syntaxes'
import ply
import ply.lex as lex
import ply.yacc as yacc

import ply.syntax

reserved = {
   'SOURCE' : 'SOURCE',
   'SRC' : 'SRC',
   #'else' : 'ELSE',
   #'while' : 'WHILE',

}
tokens = [
   'NEWLINE',
   'LBRACKET',
   'RBRACKET',
   'EQUALS',
   'ID',
   'INT',
   'URL',

] + list(reserved.values())


t_NEWLINE = r'\n'
t_ignore  = ' \t'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_EQUALS  = r'='

def t_URL(t):
    r'http://[a-zA-Z_./][a-zA-Z_0-9./]*'
    return t

def t_INT(t):
    r'[0-9]+'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    assert False,'Problem in LEXER'
    #t.lexer.skip(1)



def p_mbnf_f1(p):
    '''srcs_line := src_line* '''
    #p[0] = p[1:]
    print 'Run p_mbnf1'
    p[0] = [ t for t in p[1] if t]
    print '\t',p[0]

def p_mbnf_f2(p):
    '''src_line := SOURCE URL (LBRACKET (ID EQUALS (ID|INT))* RBRACKET )? NEWLINE '''
    print 'Run p_mbnf2'
    for i in range(0,5):
        print '\tExisting:', i, p[i]
    p[0] = [
            p[2],
            p[3]
            ]
    print '\t',p[0]

def p_mbnf_f3(p):
    '''src_line := NEWLINE '''
    print 'Run p_mbnf3'
    p[0] = None
    print '\t',p[0]


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    assert False



import pprint
from pprint import pprint



test_string = '''
SOURCE http://en.wikipedia.org/wiki/Queen_Victoria [DEPTH=1 MODE=Spider]
SOURCE http://en.wikipedia.org/wiki/George_III_of_the_United_Kingdom
'''


#print
#print 'Pre-rewritign'
#print locals()
#print

# Turn our grammar from MBNF to EBNF
ply.syntax.mbnf.rewrite_module_in_bnf(namespace=locals())

#print 'After rewritting, the module looks like:'
#print locals()
#
#print
#print 'Starting Lexing & Yaccing'
#print


lexer = lex.lex(debug=True)

#lexer.input(test_string)
#while 1:
#    print lexer.next()
#assert False
parser = yacc.yacc(start='srcs_line',debug=True)

print '\n\n'
res = parser.parse(test_string) #,debug=True)

print '\nFinal results:: '
pprint (res)
print res
print


print '\n\nParsed OK!'
