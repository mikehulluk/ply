
import ply
import ply.lex as lex
import ply.yacc as yacc

import ply.syntax

reserved = {
   'true' : 'TRUE',
   'false' : 'FALSE',
   'null' : 'NULL',

}
tokens = [
   'LSQUARE',
   'RSQUARE',
   'LPARAN',
   'RPARAN',
   'COMMA',
   'COLON',
   'STRING',
   'INT',
   'ID',

] + list(reserved.values())


t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LPARAN = r'\('
t_RPARAN = r'\)'
t_COLON= r':'
t_COMMA= r','

t_ignore  = ' \t\n'
#t_LBRACKET  = r'\['
#t_RBRACKET  = r'\]'
#t_EQUALS  = r'='

def t_STRING(t):
    r'''".*?"'''
    #t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t



def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
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






def p_func1(p): 
    ''' data := ID ( (LSQUARE INT? RSQUARE) | ID | INT ) (LPARAN INT* RPARAN)? ID''' 
    #''' data := ID (INT|ID| (LSQUARE RSQUARE) ) ID'''
    p[0] = p[1:]


# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    assert False



import pprint
from pprint import pprint



test_string = '''hello [] (8 5 6)  world '''
test_string = '''hello [] world '''


# Turn our grammar from MBNF to EBNF
ply.syntax.mbnf.rewrite_module_in_bnf(namespace=locals())

lexer = lex.lex(debug=True)

#lexer.input(test_string)
#while 1:
#    print lexer.next()
#assert False
parser = yacc.yacc(start='data',debug=True)

print '\n\n'
res = parser.parse(test_string,debug=True)

print '\nFinal results:: '
pprint (res)
print res
print


print '\n\nParsed OK!'
