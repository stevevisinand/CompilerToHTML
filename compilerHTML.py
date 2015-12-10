__author__ = 'stevevisinand'

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

#Un noeud de type Program "compile" (execute) simplement ses enfants dans l ordre :
@addToClass (AST.ProgramNode)
def execute(self) :
    bytecode = ""
    for c in self.children:
        bytecode += c.compile()
    return bytecode

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



#ASSIGN
@addToClass ( AST . AssignNode )
def compile(self) :
    vars[self.children[0].tok] = self.children[1].execute()




"""
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
@addToClass ( AST . PrintNode )
def compile(self) :
    print (self.children[0].execute() )

#WHILE
@addToClass(AST.WhileNode)
def compile(self):
    while self.children[0].execute():
        self.children[1].execute()
"""


def generate_header(title, color=""):

    styles=""
    if(color!=""):
        styles = "style='background-color:'"+color

    return """<header>
                <div class='center' "+styles+">
                    <h1 id='title-header'>"+title+"</h1>
                </div>
                </header>"""

def generate_nav(mapLink, color="", textcolor=""):

    styles=""
    if(color!=""):
        styles = "style='background-color:'"+color
    if(textcolor!=)


def generate_page(pageName, contentHTML):

    pageHtml="""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8" />
                    <title>"""+pageName+"""</title>
                    <link rel="stylesheet" type="text/css" href="styles.css">
                </head>
                <body>

                """+contentHTML+"""

                </body>
                </html>
                """

    fichier = open("./"+pageName+".html","w")
    fichier.writelines(pageHtml)
    fichier.close()



if __name__ == "__main__":
    #from parser5 import parse
    #import sys
    #prog = open("lex.txt").read()
    #ast = parse(prog)

    #ast.execute()

    generate_page("page", "<p>hello</p>")