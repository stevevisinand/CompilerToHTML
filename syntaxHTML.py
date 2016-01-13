__author__ = 'horia_000'

import ply.yacc as yacc
from lexHTML import tokens
import AST
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
loops = []

# Define our page elements
page_elements = []


# TODO Program
def p_program_recursive(p):
    """ program : statement
                | statement ';' program
                | statement ',' program """
    try:
        p[0] = p[3]
        p[0] = AST.ProgramNode([p[1]] + p[3].children)
    except:
        p[0] = p[1]
        p[0] = AST.ProgramNode(p[1])


# TODO Statment
def p_statement(p):
    """ statement : assignment
                  | elementAssignment
                  | pageAssignment
                  | expression
    """
    p[0] = p[1]
    print "Statement",p[0]
    # p[0] = AST.EntryNode()
    # p[0] = AST.ProgramNode(p[1])


# TODO Assignment
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
    # p[0] = p[3]
    # TODO AST-Assignment
    print "ASSSIGNEMENT!!!"
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


# Numbers
def p_expression_number(p):
    """expression : NUMBER"""
    # p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# Strings
def p_expression_string(p):
    """expression : STRING"""
    # p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# Increments or Decrements
def p_expression_delta(p):
    """expression : DELTA"""
    p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# Boolean conditions
def p_expression_condition(p):
    """expression : CONDITION"""
    p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# Not used so screw it
# def p_expression_comment(p):
#     """expression : COMMENT"""
#     print p.lineno
#     print p[1]
#     # p[0] = p[1]


# Identifiers
def p_expression_identifier(p):
    """expression : IDENTIFIER"""
    # p[0] = variables[p[1]]
    # print 'was used.'
    # TODO AST-TokenNode
    p[0] = AST.TokenNode(variables[p[1]])



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
    # for i in range(int(p[5]), int(p[7])):
    #     # See if the loopStructure actually makes a call to an existing element.
    #     if p[9][1] in elements:
    #         loops.append(elements[p[9][1]])
    #     else:
    #         loops.append(p[9][1])
    # p[0] = loops
    # print "Loop Def"
    # TODO AST.ForNode
    p[0] = AST.ForNode([AST.TokenNode(p[3]), AST.TokenNode(p[5]), AST.TokenNode(p[7]), p[9]])


def p_loop_structure(p):
    """ loopStructure : '{' function '}'
    """
    # try:
    #    p[0] = p[4]
    # except:
    p[0] = p[2]


def p_function(p):
    """
        function : PRINT IDENTIFIER '(' IDENTIFIER ')'
                 | PRINT IDENTIFIER
                 | PRINT STRING
    """
    # try:
    #     p[0] = [p[1], p[2], p[4]]
    # except:
    #     p[0] = [p[1], p[2]]
    #
    # if p[2] in elements.keys():
    #     page_elements.append(elements[p[2]])
    # else:
    #     page_elements.append(p[2])
    # TODO AST-PrintNode
    # print type(p[2]),p[2]
    p[0] = AST.PrintNode(AST.TokenNode(p[2]))


# Used for ignoring comments.
# def p_empty(p):
#     '''empty :'''
#     pass


# Pages
def p_page_assignment(p):
    """
        pageAssignment : PAGE IDENTIFIER '{' pageExpression '}'
    """
    global loops, page_elements
    page = None
    if (attributes.get('name') is not None) & (attributes.get('address') is not None):
        page = HTMLClasses.Page(attributes['name'], attributes['address'])

        page.add(loops)
        page.add(page_elements)

        pages[p[2]] = page
        global currentPageKey
        currentPageKey = p[2]

        # Clear the loops as they were already given to a page.
        loops = []
        # Clear the page elements as they were already given to a page.
        page_elements = []

    # p[0] = p[2]
    # p[0] = page
    # # TODO AST-PageAssignNode
    p[0] = AST.PageAssignNode([AST.TokenNode(p[2]), p[4]])


# TODO - Fix page expression
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
    # print "Element Assignment"
    # print attributes
    # element = None
    # if p[2] == 'nav':
    #     element = HTMLClasses.Nav(p[3])
    # elif p[2] == 'header':
    #     element = HTMLClasses.Header(p[3])
    # elif p[2] == 'footer':
    #     element = HTMLClasses.Footer(p[3])
    # global currentElementKey
    # currentElementKey = p[3]
    #
    # # print "Setting current Element " + currentElementKey + "'s attributes to:" + str(attributes)
    # element.setAttributes(attributes)
    # elements[p[3]] = element
    #
    # attributes.clear()
    # menus.clear()
    # p[0] = p[5]
    # TODO AST-ElementAssignNode
    # Test what instance it is of
    # print isinstance(p[5],AST.AttributeAssignementNode);
    p[0] = AST.ElementAssignNode([AST.TokenNode(p[2]), p[5]])


def p_element_expression(p):
    ''' elementExpression : attributeAssignment ';'
                          | attributeAssignment ';' elementExpression
    '''
    # print "Element Expression - Am in element:" + currentElementKey
    try:
        p[0] = p[3]
        # print "elem_expression 3 :",p[3]
        # p[0] = AST.TokenNode(p[3])
    except:
        p[0] = p[1]
        # print "elem_expression 1 :",p[1]
        # p[0] = AST.TokenNode(p[1])


def p_attribute_assignment(p):
    # '''
    # attributeAssignment  : TITLE ':' STRING
    #                      | COLOR ':' STRING
    #                      | PARAGRAPH ':' STRING
    #                      | COPYRIGHT ':' STRING
    #                      | CONTENT ':' STRING
    #                      | MENU ':' menuDefinition
    #                      | NAME ':' STRING
    #                      | ADDRESS ':' STRING
    #                      | TITLE ':' IDENTIFIER
    #                      | COLOR ':' IDENTIFIER
    #                      | PARAGRAPH ':' IDENTIFIER
    #                      | COPYRIGHT ':' IDENTIFIER
    #                      | CONTENT ':' IDENTIFIER
    #                      | MENU ':' IDENTIFIER
    #                      | NAME ':' IDENTIFIER
    #                      | ADDRESS ':' IDENTIFIER
    # '''
    '''
    attributeAssignment  : TITLE ':' expression
                         | COLOR ':' expression
                         | PARAGRAPH ':' expression
                         | COPYRIGHT ':' expression
                         | CONTENT ':' expression
                         | MENU ':' menuDefinition
                         | MENU ':' expression
                         | NAME ':' expression
                         | ADDRESS ':' expression
    '''
    # Check if we have a call to an existing variable.
    # if p[3] in variables.keys():
    #     # We do, so the attribute is assigned that variable.
    #     attributes[p[1]] = variables[p[3]]
    # else:
    #     # We don't, just assign the STRING to the attribute.
    #     attributes[p[1]] = p[3]
    # # print 'Printing attribute assignation: ', p[1], type(p[3]), p[3]
    # p[0] = attributes[p[1]]
    # TODO AST-AttributeAssignementNode
    p[0] = AST.AttributeAssignementNode([AST.TokenNode(p[1]), p[3]])


# def p_element_menu_assignation(p):
#     """ menuAssignment : IDENTIFIER ':' menuDefinition """
#     p[0] = p[2]
#     print p[2]


# TODO AST-MenuNode
def p_element_menu_definition(p):
    """ menuDefinition : '[' listAssignment ']'
    """
    # p[0] = menus
    # print p[2]

    p[0] = AST.MenuNode([p[2]])


# TODO AST-ListAssignement
def p_list_assignment(p):
    """ listAssignment : STRING ':' IDENTIFIER ','
                       | STRING ':' IDENTIFIER
                       | STRING ':' IDENTIFIER ',' listAssignment
    """
    # menus[p[1]] = p[3]
    # p[0] = menus[p[1]]
    # p[0] = p[3]
    # print p[3]
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), AST.TokenNode(p[3])])


def p_error(p):
    if p:
        print ("Syntax error in line %d at '%s'" % (p.lineno, p.value))
    else:
        print ("Syntax error at EOF, '%s'" % p.value)
    parser = yacc.yacc()
    parser.errok()


# TODO : ADDITION of PAGES
# def p_expression_operation(p):
#     """expression : expression ADD_OP expression"""
#     # Create a new node from p[2], add it to the node of p[1], then do nothing. =
#     # p[1].addNext(AST.Node(p[2]))
#     print "detected operation."


def parse(program):
    return yacc.parse(program)

yacc.yacc(outputdir='generated')

if __name__ == '__main__':
    import sys

    prog = open("input_00.txt").read()
    result = yacc.parse(prog)
    delimiter = '\n'
    # print "-------------\tVariables, Pages and Elements\t-------------"
    # print variables, delimiter, pages, delimiter, elements
    # print "-------------\tAttributes and Menus\t-------------"
    # print attributes, delimiter, menus
    # print "#######################\tResult\t#######################"
    print(result)
