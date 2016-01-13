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
        code = c.compile()
        if isinstance(code, str):
            html += code

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

    print("TOkenNode type 1 :",  self.tok.__class__)

    #if is string it could be a var
    if isinstance(self.tok, str):
        try:
            #return the var
            return vars[self.tok]
        except KeyError:
            return self.tok # OKAY it's a String

    return self.tok # it's something else (number etc...)



##FAIT A L AVEUGLE

# contain element
elements = {}
#   ELEMENTNAME : | -> attribut (paire cle valeur) = [] liste [0] = key, [1] = value
#                 | -> attribut (paire cle valeur)

#ElementAssignNode
@addToClass(AST.ElementAssignNode)
def compile(self):
                #NAME                           #ALL elemExpr (ElementExpressionNode)
    elements[self.children[0].tok] = self.children[1].compile()


#ElementExpressionNode
@addToClass(AST.ElementExpressionNode)
def compile(self):
    # elemExpr can have multiple values that compose the attributs

    attributs = []
    for c in self.children:
        attributs.append(c.compile()) #TODO : create a type that accept only ":"

    return attributs


#MenuNode
@addToClass(AST.MenuNode)
def compile(self):

    #ATTR NAME (MENU)       #CONTENT (ListNode)
    pair = []
    pair.append(self.children[0].tok) #[0]
    pair.append(self.children[1].compile()) #[1] : {key , value}

    return pair


#ListNode
@addToClass(AST.ListNode)
def compile(self):

    #Seriously ? how to do that shit !?
    #|  |  |  |  |  list # you ar hear
    #|  |  |  |  |  |  :
    #|  |  |  |  |  |  |  'home'
    #|  |  |  |  |  |  |  'index'
    #|  |  |  |  |  |  :
    #|  |  |  |  |  |  |  'gallerie'
    #|  |  |  |  |  |  |  'gallery'

    #you need to return {} : key, value
    #TODO

    link = {}
    for c in self.children:
        link.append(c.compile()) #TODO : create a type that accept only ":"



if __name__ == "__main__":
    from syntaxHTML import parse
    import sys
    prog = open("input_03.txt").read()
    ast = parse(prog)


    ast.compile()
