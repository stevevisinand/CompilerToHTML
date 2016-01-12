import ply.yacc as yacc
from lexHTML import tokens
import AST

# Define our variables
variables = {}

# Define our "sitemap"
pages = {}
currentPageKey = ''

# Define our page elements
elements = {}
currentElementKey = ''

# Define our attributes
attributes = {}

# Define our menus
menus = {}

# Define our loops
loops = []

# Define our page elements
page_elements = []


#yep faut bien parcourir le programme
def p_programme_statement(p) :
	'''programme : statement '''
	p[0] = AST.ProgramNode(p[1])


def p_programme_recursive(p) :
	'''programme : statement ';' programme'''
	p[0] = AST.ProgramNode([p[1]]+p[3].children)


def p_assign(p):
    """ assignment  : IDENTIFIER ':' expression
                    | IDENTIFIER '=' expression
    """
    variables[p[1]] = p[3]
    p[0] = AST.AssignNode([ AST.TokenNode(p[1]) , p[3] ])


# Numbers
def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = AST.TokenNode(p[1])

# Strings
def p_expression_string(p):
    """expression : STRING"""
    p[0] = AST.TokenNode(p[1])

#soit des assignations ou des expressions
def p_statement(p):
	''' statement : assignation
		| structure '''
	p[0] = p[1]

# Identifiers
def p_expression_var(p):
    '''expression : IDENTIFIER '''
    p[0] = AST.TokenNode(p[1])


# pour les expressions parenthesees, on pourra se satisfaire de remonter
# le sous-arbre sans inclure de noeud expression intermediaire.
def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]


def p_function(p):
    """
        function : PRINT IDENTIFIER '(' IDENTIFIER ')'
                 | PRINT IDENTIFIER
                 | PRINT STRING
    """
    try:
        p[0] = [p[1], p[2], p[4]]
    except:
        p[0] = [p[1], p[2]]

    if p[2] in elements.keys():
        page_elements.append(elements[p[2]])
    else:
        page_elements.append(p[2])
        # TODO p[0] = AST.PrintNode(p[2])
        # print type(p[0])

def p_error(p):
    print ("Syntax error in line %d" % p.lineno)
    yacc.errok()


def parse(program) :
    return yacc.parse(program)



yacc.yacc(outputdir='generated')


if __name__ == "__main__":
    import sys

    prog = open("input_03.txt").read()
    #result = yacc.parse(prog, debug=1)
    result = yacc.parse(prog)
    print (result)

    print vars


