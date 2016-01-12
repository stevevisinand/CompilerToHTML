'''
src/syntaxHTML

This file contains the grammar of our language.

Remarks:
    The grammar is strict, however there are differences with the specification we have
    initially provided. These differences are highlighted by the ##DIFFERENCE## comment.

History:
    Sections beginning and ending with ######### within functions
    are sections in which the HTMLClasses data structures were used instead of AST.
    They contain solutions in building the required data structures with their elements
    but they did not really respect the building blocks of a compiler.
    Kept for work history.

Notes:
    The TODOs can be used in some IDEs for faster navigation within the grammar definitions.
'''
__author__ = 'Horia Mut'

import ply.yacc as yacc
from lexHTML import tokens
import AST
import HTMLClasses

# =====================
# Parser global variables
# =====================
DEBUG = True


# =====================
# Helper function
# =====================
def debugger(location, p, index, add_value=False):
    if DEBUG:
        print location,"--------"
        if isinstance(index, list):
            for i in index:
                if add_value:
                    print "p[%r]:[class %s,val %r]" % (i, p[i].__class__, p[i])
                else:
                    print "p[%r]:[class %s]" % (i, p[i].__class__)
        else:
            if add_value:
                print "p[%r]:[class %s,val %r]" % (index, p[index].__class__, p[index])
            else:
                print "p[%r]:[class %s]" % (index, p[index].__class__)

        print "----------------"


# =====================
# Storage
# ======================
# Lists and dictionaries used to store pages, variables, elements, attributes, menus, loops
# ======================

# Define our variables
variables = {}

# Define our "sitemap"
pages = {}

# Define our page elements
elements = {}

# Define our attributes
attributes = {}

# Define our menus
menus = {}

# Define our loops
loops = []

# Define our page elements
page_elements = []


# ======================
# Grammar definitions
# ======================

# TODO Program - working
def p_program_recursive(p):
    """ program : statement
                | statement ';' program
                | statement ',' program """
    try:
        p[0] = AST.ProgramNode([p[1]] + p[3].children)
    except:
        p[0] = AST.ProgramNode(p[1])


# TODO Statment - working
def p_statement(p):
    """ statement : assignment
                  | elementAssignment
                  | pageAssignment
                  | expression
    """
    debugger("Statement",p,1)
    p[0] = p[1]
    # print "Statement", p[0]


# TODO Assignment - Variables - working
def p_assignment(p):
    """ assignment  : IDENTIFIER ':' expression
                    | IDENTIFIER '=' expression
    """
    variables[p[1]] = p[3]
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


# TODO Expression Number - working
def p_expression_number(p):
    """expression : NUMBER"""
    # p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# TODO Expression String - working
def p_expression_string(p):
    """expression : STRING"""
    # p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# TODO Expression Delta - working
def p_expression_delta(p):
    """expression : DELTA"""
    # p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# TODO Expression Condition - working
def p_expression_condition(p):
    """expression : CONDITION"""
    # p[0] = p[1]
    p[0] = AST.TokenNode(p[1])


# TODO Expression Identifier - working
def p_expression_identifier(p):
    """expression : IDENTIFIER"""
    # p[0] = variables[p[1]]
    p[0] = AST.TokenNode(variables[p[1]])


# TODO LoopDefinition - working ##DIFFERENCE##
def p_loop_definition(p):
    """ loopDefinition : FOR '(' IDENTIFIER FROM NUMBER TO NUMBER ')' loopStructure"""
    #     0                1  2      3       4    5      6   7     8     9

    # Multiple versions were tried before deciding to change the grammar.
    # V2 was too complicated.
    # V2 Grammar rule:
    # loopDefinition : FOR '(' IDENTIFIER '=' NUMBER ';' IDENTIFIER CONDITION NUMBER ';' IDENTIFIER DELTA ')' loopStructure

    #############################################
    # for i in range(int(p[5]), int(p[7])):
    #     # See if the loopStructure actually makes a call to an existing element.
    #     if p[9][1] in elements:
    #         loops.append(elements[p[9][1]])
    #     else:
    #         loops.append(p[9][1])
    # p[0] = loops
    #############################################

    debugger("LoopDefinition",p,9,True)
    p[0] = AST.ForNode([AST.TokenNode(p[3]), AST.TokenNode(p[5]), AST.TokenNode(p[7]), p[9]])


# TODO LoopStructure - working
def p_loop_structure(p):
    """ loopStructure : '{' function '}' """
    debugger("LoopStructure",p,2)
    p[0] = p[2]


# TODO Function - working
def p_function(p):
    """
        function : PRINT IDENTIFIER '(' IDENTIFIER ')'
                 | PRINT IDENTIFIER
                 | PRINT STRING
    """
    #############################################
    # try:
    #     p[0] = [p[1], p[2], p[4]]
    # except:
    #     p[0] = [p[1], p[2]]
    #
    # if p[2] in elements.keys():
    #     page_elements.append(elements[p[2]])
    # else:
    #     page_elements.append(p[2])
    #############################################
    p[0] = AST.FunctionNode(AST.TokenNode(p[2]))
    debugger("HEREfunction", p, 2)


# # Used for ignoring comments.
# def p_empty(p):
#     '''empty :'''
#     pass


# TODO PageAssignment - working
def p_page_assignment(p):
    """
        pageAssignment : PAGE IDENTIFIER '{' pageExpression '}'
    """

    ############################################
    # global loops, page_elements
    # page = None
    # if (attributes.get('name') is not None) & (attributes.get('address') is not None):
    #     page = HTMLClasses.Page(attributes['name'], attributes['address'])
    #
    #     page.add(loops)
    #     page.add(page_elements)
    #
    #     pages[p[2]] = page
    #     global currentPageKey
    #     currentPageKey = p[2]
    #
    #     # Clear the loops as they were already given to a page.
    #     loops = []
    #     # Clear the page elements as they were already given to a page.
    #     page_elements = []
    #
    # p[0] = page
    ############################################

    p[0] = AST.PageAssignNode([AST.TokenNode(p[2]), p[4]])


# TODO PageExpression - working
def p_page_expression(p):
    """
        pageExpression : attributeAssignment ';'
                       | pageFunction ';'
                       | attributeAssignment ';' pageExpression
                       | pageFunction ';' pageExpression
    """
    try:
        p[0] = AST.PageExpressionNode([p[1]] + p[3].children)
    except:
        p[0] = AST.PageExpressionNode([p[1]])


# TODO PageFunction - working
def p_page_function(p):
    """
        pageFunction : function
                     | loopDefinition
    """
    p[0] = p[1]

##DIFFERENCE##
# Could be used to set arguments to functions.
# In our case it would be numbers.
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


# TODO ElementAssignment - working
def p_element_assignment(p):
    """
        elementAssignment : ELEMENT NAV    IDENTIFIER '{' elementExpression '}'
                          | ELEMENT HEADER IDENTIFIER '{' elementExpression '}'
                          | ELEMENT FOOTER IDENTIFIER '{' elementExpression '}'
    """
    ############################################
    # # Get the correct element type.
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
    # element.setAttributes(attributes)
    # elements[p[3]] = element
    #
    # # Clear the set data as it was allocated to the element.
    # attributes.clear()
    # menus.clear()
    #
    # # Set the element.
    # p[0] = p[5]
    ############################################

    ##DIFFERENCE##
    # In the specification each element has a determined list of attributes it
    # can posess. This would mean multiple nodes.
    # We have added the possibility to make "generic" nodes that are defined by their children
    # instead of by their type.

    # TODO - uncomment to use non-generic element nodes
    # if p[2] == 'nav':
    #     p[0] = AST.NavElementNode([AST.TokenNode(p[2]), p[5]])
    # elif p[2] == 'header':
    #     p[0] = AST.HeaderElementNode([AST.TokenNode(p[2]), p[5]])
    # elif p[2] == 'footer':
    #     p[0] = AST.FooterElementNode([AST.TokenNode(p[2]), p[5]])
    # TODO - comment to use generic element node
    p[0] = AST.ElementAssignNode([AST.TokenNode(p[2]), p[5]])


# TODO ElementExpression - working
def p_element_expression(p):
    ''' elementExpression : attributeAssignment ';'
                          | attributeAssignment ';' elementExpression
    '''
    try:
        p[0] = AST.ElementExpressionNode([p[1]] + p[3].children)
    except:
        p[0] = AST.ElementExpressionNode([p[1]])


# TODO AttributeAssignment - working
def p_attribute_assignment(p):
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
    ############################################
    # Check if we have a call to an existing variable.
    # if p[3] in variables.keys():
    #     # We do, so the attribute is assigned that variable.
    #     attributes[p[1]] = variables[p[3]]
    # else:
    #     # We don't, just assign the STRING to the attribute.
    #     attributes[p[1]] = p[3]
    # # print 'Printing attribute assignation: ', p[1], type(p[3]), p[3]
    # p[0] = attributes[p[1]]
    ############################################
    if p[3] in variables.keys():
        p[0] = AST.AttributeAssignementNode([AST.TokenNode(p[1]), variables[p[3]]])
        debugger("HEEEEERREEE",p,0,True);
    else:
        p[0] = AST.AttributeAssignementNode([AST.TokenNode(p[1]), p[3]])


# TODO menuDefinition - working
def p_element_menu_definition(p):
    """ menuDefinition : '[' listAssignment ']' """
    # V1
    # print "menuDefinition"
    # print p[2].__class__
    # listAssignement = []
    # for key in p[2].keys():
    #     value = p[2].get(key)
    #     listAssignement.append(AST.AssignNode([key,value]))
    # p[0] = AST.MenuNode(listAssignement)
    # print p[0]

    # V2
    p[0] = AST.MenuNode([p[2]])


# TODO ListAssignement - working
def p_list_assignment(p):
    """ listAssignment : STRING ':' IDENTIFIER
                       |  STRING ':' IDENTIFIER ',' listAssignment
    """
    try:
        assignement = AST.AssignNode([AST.TokenNode(p[1]), AST.TokenNode(p[3])])
        p[0] = AST.ListNode([assignement] + p[5].children)
    except:
        assignement = AST.AssignNode([AST.TokenNode(p[1]), AST.TokenNode(p[3])])
        p[0] = AST.ListNode([assignement])


def p_error(p):
    if p:
        print ("Syntax error in line %d at '%s'" % (p.lineno, p.value))
    else:
        print ("Syntax error at EOF, '%s'" % p.value)
    parser = yacc.yacc()
    parser.errok()


# TODO : ADDITION of PAGES - Not Done - ##DIFFERENCE##
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

    prog = open(sys.argv[1]).read()
    result = yacc.parse(prog)
    delimiter = '\n'
    # print "-------------\tVariables, Pages and Elements\t-------------"
    # print variables, delimiter, pages, delimiter, elements
    # print "-------------\tAttributes and Menus\t-------------"
    # print attributes, delimiter, menus
    # print "#######################\tResult\t#######################"
    print(result)
