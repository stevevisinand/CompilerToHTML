__author__ = 'stevevisinand'

#import AST
#from AST import addToClass
#from functools import reduce

"""
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
@addToClass ( AST.AssignNode )
def compile(self) :
    vars[self.children[0].tok] = self.children[1].execute()

"""


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

#
# Generate header element, if you don't need to change attribut let it to ""
#
def generate_header(title, color="", textcolor=""):
    styles=styles_color_textColor(color, textcolor)

    return """
                <header """+styles+""">
                <div class='center'>
                    <h1 id='title-header'>"""+title+"""</h1>
                </div>
                </header>
                """
#
# Generate nav element, if you don't need to change attribut let it to ""
#
def generate_nav(arrayLink, color="", textcolor=""):
    styles=styles_color_textColor(color, textcolor)

    html = """<nav """+styles+""">
            <div class="center">
                <ul>
                """

    for pair in arrayLink:
        page = pair[0]
        link = pair[1]
        if isinstance(link, list):
                html = html + "<a href='#'><li>"+page+"<ul class='sous-menu'>"

                for pair1 in link:
                    page1 = pair1[0]
                    link1 = pair1[1]
                    html = html+ "<a href='"+link1+"'><li>"+page1+"</li></a>"

                html = html+ "</ul></li></a>"

        else:
            html = html+ "<a href='"+link+"'><li>"+page+"</li></a>"


    html = html+"""</ul>
            </div>
        </nav>"""

    return html


#
# Generate new page .htm and add contentHTML on it
#
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

    fichier = open("./generatedSite/"+pageName+".html","w")
    fichier.writelines(pageHtml)
    fichier.close()

#
# Generate main content element, if you don't need to change attribut let it to ""
#
def generate_content_page(content):
    return  """<div class="center contenu">
            """+content+"""
            </div>"""

#
# Generate footer element, if you don't need to change attribut let it to ""
#
def generate_footer_page(title="", paragraph="", copyright="", color="", textcolor=""):
    styles = styles_color_textColor(color, textcolor)

    if(title != ""):
        title = '<h1 class="title-foot">' + title + '</h1>'

    if(paragraph != ""):
        paragraph = ' <p>' + paragraph + '</p>'

    if(copyright != ""):
        copyright = '<p class="copyright">' + copyright + '</p>'

    return """
        <footer """+styles+"""">
            <div class="center">
                """ + title + """
                """ + paragraph + """
                """ + copyright + """
            </div>
        </footer>
    """

#
# Generate styles to apply on elements
#
def styles_color_textColor(color, textcolor):

    styles=""

    if(color!="" or textcolor!=""):
        styles = "style='"
    if(color!=""):
        styles = styles + "background-color:"+color+";"
    if(textcolor!=""):
        styles = styles + " color:"+textcolor+";"
    if(styles!=""):
        styles = styles + "'"

    return styles


if __name__ == "__main__":
    #from parser5 import parse
    #import sys
    #prog = open("lex.txt").read()
    #ast = parse(prog)

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

    #ast.execute()