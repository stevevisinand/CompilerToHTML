__author__ = 'horia_000'

import ply.yacc as yacc
from lexHTML import tokens


def p_error(p):
    print ("Syntax error in line %d" % p.lineno)
    parser = yacc.yacc()
    parser.errok()


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_string(p):
    """expression : STRING"""
    p[0] = p[1]


def p_expression_comment(p):
    """expression : COMMENT"""
    p[0] = p[1]


#def p_statement(p):
#    """expression : element string identifier '{' expression '}' """
#   p[0] = p[3]





yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys

    program = open(sys.argv[1]).read()
    result = yacc.parse(program, debug=0)
    print result
