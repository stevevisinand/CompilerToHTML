__author__ = 'stevevisinand'

from generatorHTML import *

import AST
from AST import addToClass
from functools import reduce


#on remplace par le texte en "bytecode" pour la machine virtuelle
operations={
    '+' : 'ADD',
    '-' : 'SUB',
    '*' : 'MUL',
    '/' : 'DIV',
}

vars = {}

#contain pages Attributs
#  "PAGENAME"
#       | -> "ATTRNAME" = ATTR
#       | -> "ATTRNAME" = ATTR
#  "PAGENAME2"
#       | -> "ATTRNAME" = ATTR
#       | -> "ATTRNAME" = ATTR
attributes = {}

#ProgramNode
#Un noeud de type Program "compile" (execute) simplement ses enfants dans l ordre :
@addToClass ( AST.ProgramNode )
def execute(self) :
    html = ""
    for c in self.children:
        html += c.compile()
    return html


#AssignNode
@addToClass ( AST.AssignNode )
def compile(self) :

    print("AssignNode")

    vars[self.children[0].tok] = self.children[1].compile()


#TokenNode
@addToClass( AST.TokenNode )
def compile(self):

    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print ("*** Error: variable %s undefined!" % self.tok)
    return self.tok



#TODO : PageAssignNode
#Contain pages description
@addToClass( AST.PageAssignNode )
def compile(self) :
    #TODO : Parent ?
    attributes[self.parent()][self.children[0].tok] = self.children[1].compile()


var curentAttributes = {}


#TODO : PageAdditionNode
#TODO : ForNode
#TODO : WhileNode

#TODO : MenuNode
#TODO : AttributeAssignementNode


#TODO : ElementExpressionNode
@addToClass( AST.ElementExpressionNode )
def compile(self) :
    #rien

    for(childern in children)
    self.children[1].compile()

#TODO : AttributeAssignementNode
@addToClass( AST.AttributeAssignementNode )
def compile(self) :
    curentAttributes[self.children[0].tok] = self.children[1].execute()


#TODO : ElementAssignNode

#TODO : OpNode





"""
#tenir compte des operateurs unaires (du genre -2)
# operation arithmetique
@addToClass(AST.OpNode)
def compile(self):
    bytecode = ""
    if len(self.children) == 1: # si c est une operation unaire (nombre negatif), empile le nombre et l'inverse
        bytecode += self.children[0].compile()
        bytecode += "USUB\n"
    else:                       # si c'est une operation binaire, empile les enfants puis l'operation
        for c in self.children:
            bytecode += c.compile()
        bytecode += operations[self.op] + "\n"
    return bytecode

"""

"""
# notre AST ne comporte qu un
# seul type de noeud pour les nombres et les identificateurs
# PUSHC <val>: pushes the constant value <val> on the execution stack
# PUSHV <id>: pushes the value of the identifier <id> on the execution stack
@addToClass(AST.TokenNode)
def compile(self):
    bytecode = ""
    if isinstance(self.tok, str): #value
        bytecode += "PUSHV %s\n" % self.tok
    else:                         #constant
        bytecode += "PUSHC %s\n" % self.tok
    return bytecode

    print(self.type)
"""

"""

#ASSIGN
@addToClass ( AST.AssignNode )
def compile(self) :
    vars[self.children[0].tok] = self.children[1].execute()


# notre AST ne comporte qu un
# seul type de noeud pour les nombres et les identificateurs
@addToClass(AST.TokenNode)
def compile(self):

    if isinstance(self.tok, str):
        try:
            return vars[self.tok]
        except KeyError:
            print ("*** Error: variable %s undefined!" % self.tok)
    return self.tok



#ASSIGN
@addToClass ( AST . AssignNode )
def compile(self) :
    vars[self.children[0].tok] = self.children[1].execute()

#PRINT
@addToClass ( AST . FunctionNode )
def compile(self) :
    print (self.children[0].execute() )

#WHILE
@addToClass(AST.WhileNode)
def compile(self):
    while self.children[0].execute():
        self.children[1].execute()
"""


if __name__ == "__main__":
    from syntaxHTML import parse
    import sys
    prog = open("input_00.txt").read()
    ast = parse(prog)

    """
    # create an nav structure
    #            name      link
    nav =   [   ["home", "/link1"],
                ["gallery", # menu accordeon
                    [
                        ["gal1",  "/gal1"],
                        ["gal2", "/gal2"] ]
                    ]
            ]

    #generate page content
    pageContent = generate_header("Mon site", "blue", "red")
    pageContent += generate_nav(nav)
    pageContent += generate_content_page("<p>Contenu</p>")
    pageContent += generate_footer_page("Title", "paragraphe", "copyright", "blue", "red")

    generate_page("index", pageContent) # create page "index.html" (addr)
    """

    ast.execute()
