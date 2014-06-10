
import ply
import ply.lex as lex
import ply.yacc as yacc

import pprint
#from pprint import pprint

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
   'FLOAT',
   'INT',
   'ID',

] + list(reserved.values())


t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_LPARAN = r'\{'
t_RPARAN = r'\}'
t_COLON= r':'
t_COMMA= r','

t_ignore  = ' \t\n'

def t_STRING(t):
    r'''".*?"'''
    return t


def t_FLOAT(t):
    r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
    t.value = float(t.value)
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
    ''' data := STRING | INT | FLOAT | bool | list | dict | NULL '''
    p[0] = p[1]

def p_func2(p):
    #''' list := LSQUARE (data (COMMA (data COMMA)*)?  )? RSQUARE'''
    ''' list := LSQUARE (data COMMA)* RSQUARE'''
    #p[0] = p[2]
    p[0] = [d for (d,_comma) in p[2] ]

def p_func3(p):
    ''' dict :=  LPARAN (data COLON data COMMA)* RPARAN'''
    p[0] = { t[0]:t[2] for t in p[2] }

def p_func4(p):
    ''' bool := TRUE | FALSE'''
    p[0] = p[1]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"
    assert False






test_string = '''
{
    "firstName": "John",
    "lastName": "Smith",
    "isAlive": true,
    "age": 25,
    "height_cm": 167.64,
    23.3: 34.5,
    "address": {
        "streetAddress": "21 2nd Street",
        "city": "New York",
        "state": "NY",
        "postalCode": "10021-3100",
    },
    "phoneNumbers": [
        { "type": "home", "number": "212 555-1234", },
        { "type": "office",  "number": "646 555-4567", },
    ],
}

'''


# Turn our grammar from MBNF to EBNF
ply.syntax.mbnf.rewrite_module_in_bnf(namespace=locals())

debug = False
lexer = lex.lex(debug=debug)
parser = yacc.yacc(start='data',debug=debug)

print '\n\n'
res = parser.parse(test_string,debug=debug)

print '\nFinal results:: '
pprint.pprint(res)


print '\n\nParsed OK!'
