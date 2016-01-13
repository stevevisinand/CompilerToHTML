__author__ = 'stevevisinand'

from generatorHTML import *

import AST
from AST import addToClass
from functools import reduce

#Contain variables
vars = {}

#ProgramNode
#Un noeud de type Program "compile" (execute) simplement ses enfants dans l ordre :
@addToClass ( AST.ProgramNode )
def compile(self) :
    html = ""

    print("ProgramNode : ", self.children)
    for c in self.children:
        html += c.compile()
    return html


#AssignNode
@addToClass ( AST.AssignNode )
def compile(self) :

    print("AssignNode, self.children :", self.children)

    vars[self.children[0].tok] = self.children[1].compile()

    print("AssignNode, vars:", vars)


#TokenNode
@addToClass(AST.TokenNode)
def compile(self):
    print("print : ", self.tok)

    #if is string it could be a var
    if isinstance(self.tok, str):
        try:
            #return the var
            return vars[self.tok]
        except KeyError:
            return self.tok # OKAY it's a String

    return self.tok # it's something else (number etc...)



##FAIT A L AVEUGLE


elements = {}
#   ELEMENTNAME : | -> attribut (paire cle valeur)
#                 | -> attribut (paire cle valeur)

#ElementAssignNode
@addToClass(AST.ElementAssignNode)
def compile(self):
                #NAME                           #ALL elemExpr
    elements[self.children[0].tok] = self.children[1].compile()


@addToClass(AST.ElementExpressionNode)
def compile(self):
    # elemExpr can have multiple values that compose the attributs

    attributs = []
    for c in self.children:
        attributs.append(c.compile()) #TODO : create a type that accept only ":"

    return attributs




if __name__ == "__main__":
    from syntaxHTML import parse
    import sys
    prog = open("input_00.txt").read()
    ast = parse(prog)


    ast.compile()
