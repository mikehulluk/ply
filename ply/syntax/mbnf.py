#!/usr/bin/python
# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc

import sys

# Accepted TOKENS:
t_STAR = r'\*'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_COLONEQUALS = r':='
t_PIPE = r'\|'
t_QUESTIONMARK = r'\?'

t_ignore = ' \t\n'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

reserved = {
    # keyword-in-language : NODE-NAME
    #'if' : 'IF',
}
tokens = ['LPAREN',
          'RPAREN',

          'COLONEQUALS',
          'STAR',
          'PIPE',
          'QUESTIONMARK',
          'ID'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t








# Utility functions:
import ast


class CodeObjectProxy(object):

    def __init__(self, src_code):
        self.node_ast = ast.parse(src_code, mode='exec')
        self.node = compile(self.node_ast, '<string>', mode='exec')
        self.func_name = self.node_ast.body[0].name
        self.src_code = src_code

    @property
    def name(self):
        return self.func_name

# Its not big or clever, we just generate
# new function/production names by incrementing
# global variable:
_new_func_numb = 0


def _get_new_function_and_production_names():
    global _new_func_numb
    # Create a new function name for this expression:
    new_function_name = 'p_generatedfunc%d' % _new_func_numb
    new_production_name = 'production_%d' % _new_func_numb
    _new_func_numb = _new_func_numb + 1
    return (new_function_name, new_production_name)


# Accepted GRAMMAR rules:


def p_mbnfsyntax_productionname(p):
    '''production_name :  ID'''
    p[0] = p[1]

def p_mbnfsyntax_prod(p):
    '''production : production_lhs COLONEQUALS production_rhs '''

    (t0_local_production_def, t0_generated_rules) = p[3]


    t0_new_function_name, t0_new_production_name = _get_new_function_and_production_names()


    forwarding_function_name = p.lexer.function_forward_name
    p.lexer.function_forward_name = None
    assert forwarding_function_name


    t1_new_func_def = '''
def {func_name}(p):
    '{prod_lhs} : {prod_rhs}'
    # Function generated by: '{generating_function}'
    _{forward_function_name}(p)

'''.format(func_name=t0_new_function_name,
           prod_lhs=p[1],
           prod_rhs=t0_local_production_def,
           generating_function=sys._getframe().f_code.co_name,
           forward_function_name=forwarding_function_name
           )
    co1 = CodeObjectProxy(src_code=t1_new_func_def)

    p[0] = (p[1], t0_local_production_def, [co1] + t0_generated_rules )

def p_mbnfsyntax_pr3(p):
    'production_lhs : production_name'
    p[0] = p[1]

# The right handside can be empty, or an expression:
def p_mbnfsyntax_p1(p):
    'production_rhs : '
    p[0] = ('', [] )

def p_mbnfsyntax_p2(p):
    'production_rhs : production_expr '
    p[0] = p[1]










# All of the following functions should return a 2-tuple containing
#  t[0] = the local production rule
#  t[1] - a list of function-objects that generate the productions.

def p_mbnfsyntax_expr0(p):
    'production_expr :  production_term'
    p[0] = p[1]

def p_mbnfsyntax_t0(p):
    'production_term :  production_name'
    p[0] = ( p[1],[] )

def p_mbnfsyntax_t1(p):
    'production_term :  production_term production_term'
    (t0_local_production_def, t0_generated_rules) = p[1]
    (t1_local_production_def, t1_generated_rules) = p[2]

    p[0] = (t0_local_production_def + ' ' + t1_local_production_def,
            t0_generated_rules + t1_generated_rules)










def p_mbnfsyntax_t1a(p):
    'production_term :  production_term STAR'
    (t0_local_production_def, t0_generated_rules) = p[1]

    # We create 2 functions, to allow the following productions:
    #  prod_list: empty | (prod_list prod)
    t0_new_function_name, t0_new_production_name = _get_new_function_and_production_names()
    t1_new_function_name, _t1_new_production_name = _get_new_function_and_production_names()

    # Create two functions itself:
    t0_new_func_def = '''
def {func_name}(p):
    '{prod_name} : '
    # Function generated by: '{generating_function} (A)'
    p[0] = []
'''.format(func_name=t0_new_function_name,
               prod_name=t0_new_production_name,
               prod_rhs=t0_local_production_def,
               generating_function = sys._getframe().f_code.co_name
               )
    co0 = CodeObjectProxy(src_code=t0_new_func_def)

    t1_new_func_def = '''
def {func_name}(p):
    '{prod_name} : {prod_name} {prod_rhs}'
    # Function generated by: '{generating_function} (B)'
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        print p
        assert False
'''.format(func_name=t1_new_function_name,
               prod_name=t0_new_production_name,
               prod_rhs=t0_local_production_def,
               generating_function = sys._getframe().f_code.co_name
               )
    co1 = CodeObjectProxy(src_code=t1_new_func_def)


    p[0] = (t0_new_production_name,
            t0_generated_rules + [co0,co1])



def p_mbnfsyntax_t1b(p):
    'production_term :  production_term QUESTIONMARK'
    (t0_local_production_def, t0_generated_rules) = p[1]

    # We create 2 functions, to allow the following productions:
    #  prod_list: empty | (prod)
    t0_new_function_name, t0_new_production_name = _get_new_function_and_production_names()
    t1_new_function_name, _t1_new_production_name = _get_new_function_and_production_names()

    # Create two functions itself:
    t0_new_func_def = '''
def {func_name}(p):
    '{prod_name} : '
    # Function generated by: '{generating_function} (A)'
    p[0] = None
'''.format(func_name=t0_new_function_name,
               prod_name=t0_new_production_name,
               prod_rhs=t0_local_production_def,
               generating_function = sys._getframe().f_code.co_name
               )
    co0 = CodeObjectProxy(src_code=t0_new_func_def)

    t1_new_func_def = '''
def {func_name}(p):
    '{prod_name} : {prod_rhs}'
    # Function generated by: '{generating_function} (B)'
    # Lets avoid having lots of lists of lists:
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]
'''.format(func_name=t1_new_function_name,
               prod_name=t0_new_production_name,
               prod_rhs=t0_local_production_def,
               generating_function = sys._getframe().f_code.co_name
               )
    co1 = CodeObjectProxy(src_code=t1_new_func_def)


    p[0] = (t0_new_production_name,
            t0_generated_rules + [co0,co1])

def p_mbnfsyntax_t2(p):
    'production_term :  production_term PIPE production_term'

    # We create a new production symbol, and 2 new functions:
    t0_new_function_name, t0_new_production_name = _get_new_function_and_production_names()
    t1_new_function_name, _t1_new_production_name = _get_new_function_and_production_names()

    (t0_local_production_def, t0_generated_rules) = p[1]
    (t1_local_production_def, t1_generated_rules) = p[3]

    # Create two functions itself:
    t0_new_func_def = '''
def {func_name}(p):
    '{prod_name} : {prod_rhs}'
    # Function generated by: '{generating_function}'
    p[0] = p[1]
'''.format(func_name=t0_new_function_name,
               prod_name=t0_new_production_name,
               prod_rhs=t0_local_production_def,
               generating_function = sys._getframe().f_code.co_name
               )
    co0 = CodeObjectProxy(src_code=t0_new_func_def)

    t1_new_func_def = '''
def {func_name}(p):
    '{prod_name} : {prod_rhs}'
    # Function generated by: '{generating_function}'
    p[0] = p[1]
'''.format(func_name=t1_new_function_name,
               prod_name=t0_new_production_name,
               prod_rhs=t1_local_production_def,
               generating_function = sys._getframe().f_code.co_name
               )
    co1 = CodeObjectProxy(src_code=t1_new_func_def)


    p[0] = (t0_new_production_name,
            t0_generated_rules + t1_generated_rules + [co0,co1])








def p_mbnfsyntax_t3(p):
    'production_term :  LPAREN production_term RPAREN'

    t0_new_function_name, t0_new_production_name = _get_new_function_and_production_names()
    (local_production_def, generated_rules) = p[2]
    t0_new_func_def = '''
def {func_name}(p):
    '{prod_name} : {prod_rhs}'
    # Function generated by: '{generating_function}'
    # Lets avoid having lots of lists of lists:
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1:]
'''.format(func_name=t0_new_function_name,
               prod_name=t0_new_production_name,
               prod_rhs=local_production_def,
               generating_function = sys._getframe().f_code.co_name
               )
    co0 = CodeObjectProxy(src_code=t0_new_func_def)


    p[0] = t0_new_production_name, generated_rules + [co0]




precedence = (
    ('left', 'PIPE', ),
    ('left', 'STAR', 'QUESTIONMARK'),
)






def rewrite_function_in_bnf(name, function, namespace):
    print '\tFunction: ', name


    # Look at the docstring:
    docstring = function.__doc__


    # Build the parser:
    lexer = lex.lex()
    parser = yacc.yacc(start='production')


    # Run the parser:
    lexer.src_txt = docstring
    lexer.function_forward_name = name
    lhs_symbol, rhs_symbol, new_functions = parser.parse(docstring, tracking=True)


    # And replace the old function with the new functions in the namespace, by replaceing 'p_X' to '_p_X'...
    namespace['_'+name] = namespace.pop(name)
    # ... and by adding the new functions in:
    for func in new_functions:
        exec func.node in namespace

    return new_functions







def rewrite_module_in_bnf(namespace, logfilename='to_bnf.log'):
    print 'Rewriting module in BNF'


    with open(logfilename,'w') as logfile:

        # Find all functions in the namespace starting with 'p_'
        production_functions = dict( (k,v) for (k, v) in namespace.iteritems()
                                    if k.startswith('p_') )
        for (name,function) in production_functions.iteritems():
            if name=='p_error':
                continue
            print ' *** Rewriting function:', name
            new_functions = rewrite_function_in_bnf(name=name, function=function, namespace=namespace)
            
            # And log it:
            module_contents = '\n\n'.join([f.src_code for f in new_functions])
            logfile.write('Function:'.ljust(12) + name  + '\n')
            logfile.write('Docstring:'.ljust(12) + function.__doc__.strip() + '\n')
            logfile.write(module_contents)
            logfile.write('==================================\n')
            logfile.write('==================================\n')
            logfile.write('\n\n')

        print
        print 'Done Rewritting namespace'
        print




