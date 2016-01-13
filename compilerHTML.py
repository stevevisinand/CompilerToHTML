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


#ProgramNode
#Un noeud de type Program "compile" (execute) simplement ses enfants dans l ordre :
@addToClass ( AST.ProgramNode )
def compile(self) :
    html = ""
    for c in self.children:
        html += c.compile()
    return html


#AssignNode
@addToClass ( AST.AssignNode )
def compile(self) :
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




if __name__ == "__main__":
    from syntaxHTML import parse
    import sys
    prog = open("input_03.txt").read()
    ast = parse(prog)


    ast.compile()
