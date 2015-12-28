__author__ = 'horia_000'

import ply.yacc as yacc
from lexHTML import tokens
# import AST
import HTMLClasses


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
# Use AST nodes for this
loops = []

# def p_program_statement(p):
#     """ program : statement """
#     p[0] = p[1]
#     # p[0] = AST.ProgramNode(p[1])

# Program
def p_program_recursive(p):
    """ program : statement
                | statement ';' program
                | statement ',' program """
    try:
        p[0] = p[3]
    except:
        p[0] = p[1]
        # p[0] = AST.ProgramNode([p[1]] + p[3].children)


# Statement
def p_statement(p):
    """ statement : assignment
                  | elementAssignment
                  | pageAssignment
                  | expression
    """
    p[0] = p[1]


# Assignment
def p_assignment(p):
    """ assignment  : IDENTIFIER ':' expression
                    | IDENTIFIER '=' expression
    """
    # """ assignment  : IDENTIFIER '=' expression """
    # """ assignment  : IDENTIFIER ':' expression
    #                 | IDENTIFIER '=' expression
    #                 | IDENTIFIER ':' structure
    # """
    variables[p[1]] = p[3]
    p[0] = p[3]
    # p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


# Numbers
def p_expression_number(p):
    """expression : NUMBER"""
    p[0] = p[1]


# Strings
def p_expression_string(p):
    """expression : STRING"""
    p[0] = p[1]


# Increments or Decrements
def p_expression_delta(p):
    """expression : DELTA"""
    p[0] = p[1]


# Boolean conditions
def p_expression_condition(p):
    """expression : CONDITION"""
    p[0] = p[1]


# Not used so screw it
# def p_expression_comment(p):
#     """expression : COMMENT"""
#     print p.lineno
#     print p[1]
#     # p[0] = p[1]


# Identifiers
def p_expression_identifier(p):
    """expression : IDENTIFIER"""
    p[0] = variables[p[1]]


# # Define other forms an expression can take, bad as this is ambiguous
# def p_expression(p):
#     """ expression : IDENTIFIER '=' NUMBER
#                    | IDENTIFIER CONDITION NUMBER
#                    | IDENTIFIER DELTA
#     """
#     p[0] = p[1]


def p_loop_definition(p):
    # Too complicated:
    # """ loopDefinition : FOR '(' IDENTIFIER '=' NUMBER ';' IDENTIFIER CONDITION NUMBER ';' IDENTIFIER DELTA ')' loopStructure"""
    """ loopDefinition : FOR '(' IDENTIFIER FROM NUMBER TO NUMBER ')' loopStructure"""
    #     0                1  2      3       4    5      6   7     8     9
    # print 'loop def'
    for i in range(int(p[5]), int(p[7])):
        loops.append(elements[p[9][1]])
    p[0] = loops


def p_loop_structure(p):
    """ loopStructure : '{' function '}'"""
    # print 'loop struct'
    p[0] = p[2]


def p_function(p):
    """
        function : PRINT IDENTIFIER '(' IDENTIFIER ')'
                 | PRINT IDENTIFIER
    """
    delimiter = ','
    try:
        p[0] = [p[1],p[2],p[4]]
    except:
        p[0] = [p[1],p[2]]


# Used for ignoring comments.
# def p_empty(p):
#     '''empty :'''
#     pass


# Pages
def p_page_assignment(p):
    """
        pageAssignment : PAGE IDENTIFIER '{' pageExpression '}'
    """
    global loops
    if (attributes.get('name') is not None) & (attributes.get('address') is not None):
        page = HTMLClasses.Page(attributes['name'], attributes['address'])

        page.add(loops)

        pages[p[2]] = page
        global currentPageKey
        currentPageKey = p[2]
        # Clear the loops as they were already given to a page.
        loops = []
    p[0] = p[2]


def p_page_expression(p):
    """
        pageExpression : attributeAssignment ';'
                       | pageFunction ';'
                       | attributeAssignment ';' pageExpression
                       | pageFunction ';' pageExpression
    """
    try:
        p[0] = p[3]
    except:
        p[0] = p[1]


def p_page_function(p):
    """
        pageFunction : function
                     | loopDefinition
    """
    p[0] = p[1]


# def p_page_function_arguments(p):
#     """
#         arguments : NUMBER
#                   | NUMBER ',' arguments
#     """
#     try:
#         p[0] = p[3]
#     except:
#         p[0] = p[1]
#
#     print p[0]


# Element
def p_element_assignment(p):
    """
        elementAssignment : ELEMENT NAV    IDENTIFIER '{' elementExpression '}'
                          | ELEMENT HEADER IDENTIFIER '{' elementExpression '}'
                          | ELEMENT FOOTER IDENTIFIER '{' elementExpression '}'
    """
    element = None
    if p[2] == 'nav':
        element = HTMLClasses.Nav(p[3])
    elif p[2] == 'header':
        element = HTMLClasses.Header(p[3])
    elif p[2] == 'footer':
        element = HTMLClasses.Footer(p[3])
    global currentElementKey
    currentElementKey = p[3]

    # print "Setting current Element " + currentElementKey + "'s attributes to:" + str(attributes)
    element.setAttributes(attributes)
    elements[p[3]] = element
    attributes.clear()
    menus.clear()
    p[0] = p[5]


def p_element_expression(p):
    ''' elementExpression : attributeAssignment ';'
                          | attributeAssignment ';' elementExpression
    '''
    # print "Element Expression - Am in element:" + currentElementKey
    try:
        p[0] = p[3]
    except:
        p[0] = p[1]


def p_attribute_assignment(p):
    '''
    attributeAssignment  : TITLE ':' STRING
                         | COLOR ':' STRING
                         | PARAGRAPH ':' STRING
                         | COPYRIGHT ':' STRING
                         | CONTENT ':' STRING
                         | MENU ':' menuDefinition
                         | NAME ':' STRING
                         | ADDRESS ':' STRING
    '''
    # TODO: Find a way to know which element I am in. Not doable as we go from bottom to top.
    # print "Att Assignment-Am in element:" + currentElementKey
    # print "Att assignment - assigning:" + p[3] + " to " + p[1]

    attributes[p[1]] = p[3]
    # print 'Printing attribute assignation: ', p[1], type(p[3]), p[3]
    p[0] = attributes[p[1]]


# def p_element_menu_assignation(p):
#     """ menuAssignment : IDENTIFIER ':' menuDefinition """
#     p[0] = p[2]
#     print p[2]


def p_element_menu_definition(p):
    """ menuDefinition : '[' listAssignment ']'
    """
    p[0] = menus
    # print p[2]


def p_list_assignment(p):
    """ listAssignment : STRING ':' IDENTIFIER ','
                       | STRING ':' IDENTIFIER
                       | STRING ':' IDENTIFIER ',' listAssignment
    """
    menus[p[1]] = p[3]
    p[0] = menus[p[1]]
    # p[0] = p[3]


def p_error(p):
    if p:
        print ("Syntax error in line %d at '%s'" % (p.lineno, p.value))
    else:
        print ('Syntax error at EOF')
    parser = yacc.yacc()
    parser.errok()

# TODO : ADDITION of PAGES
# def p_expression_operation(p):
#     """expression : expression ADD_OP expression"""
#     # Create a new node from p[2], add it to the node of p[1], then do nothing. =
#     # p[1].addNext(AST.Node(p[2]))
#     print "detected operation."


yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys

    program = open(sys.argv[1]).read()
    result = yacc.parse(program, debug=0)
    delimiter = '\n'
    print "-------------\tVariables, Pages and Elements\t-------------"
    print variables, delimiter, pages, delimiter, elements
    print "-------------\tAttributes and Menus\t-------------"
    print attributes, delimiter, menus
    print "#######################\tResult\t#######################"
    print result
