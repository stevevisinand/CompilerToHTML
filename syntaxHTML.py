__author__ = 'horia_000'

import ply.yacc as yacc
from lexHTML import tokens
import AST


def p_error(p):
    print ("Syntax error in line %d" % p.lineno)
    parser = yacc.yacc()
    parser.errok()


def p_expression_operation(p):
    """expression : expression ADD_OP expression"""
    # Create a new node from p[2], add it to the node of p[1], then do nothing. =
    p[1].addNext(AST.Node(p[2]))


def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


def p_expression_string(p):
    """expression : STRING"""
    p[0] = p[1]


def p_expression_comment(p):
    """expression : COMMENT"""
    p[0] = p[1]


def p_expression_identifier(p):
    """expression : IDENTIFIER"""
    p[0] = p[1]

def p_expression_attribute(p):
    """
       expression : TITLE ':' STRING
                  | COLOR ':' STRING
                  | paragraph ':' STRING
                  | copyright ':' STRING
                  | address ':' STRING
                  | for ':' STRING
                  | content ':' STRING
    """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_assign(p):
    """ assignation : IDENTIFIER ':' expression
                    | IDENTIFIER '=' expression
    """
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_statement(p):
    """expression : element nav identifier structure
                  | element nav identifier structure
                  | element nav identifier structure
                  | element nav identifier structure
    """
    p[0] = p[3]


def p_structure(p):
    """    """

yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys

    program = open(sys.argv[1]).read()
    result = yacc.parse(program, debug=0)
    print result
