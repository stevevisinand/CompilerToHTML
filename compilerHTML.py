__author__ = 'stevevisinand'

from generatorHTML import *

import AST
from AST import addToClass
from functools import reduce

from syntaxHTML import elementsTypes

#Contain variables
vars = {}

#ProgramNode
#Un noeud de type Program "compile" (execute) simplement ses enfants dans l ordre :
@addToClass ( AST.ProgramNode )
def compile(self) :
    #html = ""

    #print("ProgramNode : ", self.children)
    for c in self.children:
        c.compile()
        #code = c.compile()
        #if isinstance(code, str):
        #    html += code

    #return html


#AssignNode
@addToClass ( AST.AssignNode )
def compile(self) :

    #print("AssignNode, self.children :", self.children)

    vars[self.children[0].tok] = self.children[1].compile()

    #print("AssignNode, vars:", vars)


#TokenNode
@addToClass(AST.TokenNode)
def compile(self):


    #print("TOkenNode type 1 :",  self.tok.__class__)

    #if is string it could be a var
    if isinstance(self.tok, str):
        try:
            #return the var
            return vars[self.tok]
        except KeyError:
            return self.tok # OKAY it's a String

    return self.tok # it's something else (number etc...)



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
        attributs.append(c.compile()) #create a type that accept only ":"  => AttributeAssignementNode

    return attributs


#AttributeAssignementNode : ":"
@addToClass(AST.AttributeAssignementNode)
def compile(self):

    attr = []

    attr.append(self.children[0].tok)
    attr.append(self.children[1].compile())

    return attr


#MenuNode
@addToClass(AST.MenuNode)
def compile(self):

    #print("self.children[0].tok", self.children[0])

    #ATTR NAME (MENU)       #CONTENT (ListNode)
   # pair = []
   # pair.append(self.children[0].tok) #[0] : 'list'
   # pair.append(self.children[1].compile()) #[1] : [ [name, link], [name, link] ]

    return self.children[0].compile() #[ [name, link], [name, link] ]


#ListNode
@addToClass(AST.ListNode)
def compile(self):

    #|  |  |  |  |  list # <-- you are hear
    #|  |  |  |  |  |  :
    #|  |  |  |  |  |  |  'home'
    #|  |  |  |  |  |  |  'index'
    #|  |  |  |  |  |  :
    #|  |  |  |  |  |  |  'gallerie'
    #|  |  |  |  |  |  |  'gallery'

    links = []
    for c in self.children:
        links.append(c.compile()) # create a type that accept only ":" => AttributeAssignementNode
        #return  [element : value]

    return links #[ [name, link], [name, link] ]



#page
@addToClass(AST.PageAssignNode)
def compile(self):
    pageName = self.children[0].tok

    pageExpr = self.children[1].compile() #return [pageName(string), addrName(string), html(string)]

    #create PAGE !

    print("New Page created : "+pageExpr[0])

    generate_page(pageExpr[0],pageExpr[1], pageExpr[2])


@addToClass(AST.PageExpressionNode)
def compile(self):

    nameList = self.children[0].compile() # []
    addrList = self.children[1].compile() # []

    if(nameList[0] != 'name'):
        #throw error
        print("Error, first arg of a page must be a 'name'")
        quit()
    if(addrList[0] != 'address'):
        #throw error
        print("Error, first arg of a page must be a 'address'")
        quit()

    pageName = nameList[1]
    addrName = addrList[1]


    html = ""

    for c in self.children:
        code = c.compile()

        if isinstance(code, str):
            html += code

    return [pageName, addrName, html]


#FunctionNode = print
@addToClass(AST.FunctionNode)
def compile(self):

    content = str(self.children[0])

    if(elements.has_key(content)): #so we need to work a little...

        elementName = content
        elementAttrs = elements[content]

        attributes = {}
        for attr in elementAttrs:
            attributes[attr[0]] = attr[1]

        #print("Attributes : ", attributes)

        if(elementName in elementsTypes.keys()): #we know he's type
            #Here you can know the type of the element ! :)
            elementType = elementsTypes[elementName]


            if(elementType == 'header'):
                #return generated HTML for a header
                if('title' in attributes.keys()):
                    titleHeader = attributes['title']

                    color = ""
                    textcolor = ""
                    if('color' in attributes.keys()):
                        color = attributes['color']
                    if('text_color' in attributes.keys()):
                        textcolor = attributes['text_color']

                    return str(generate_header(str(titleHeader), color, textcolor))

                else:
                    print("Aie ! title attribut must be defined for the element : ", elementName)
                    quit()


            elif(elementType == 'footer'):
                #nothing obligatoire

                title = ""
                paragraph = ""
                copyright = ""
                color = ""
                textcolor = ""
                if('title' in attributes.keys()):
                    title = attributes['title']
                if('paragraph' in attributes.keys()):
                    paragraph = attributes['paragraph']
                if('copyright' in attributes.keys()):
                    copyright = attributes['copyright']
                if('color' in attributes.keys()):
                    color = attributes['color']
                if('text_color' in attributes.keys()):
                    textcolor = attributes['text_color']

                return str(generate_footer_page(title, paragraph, copyright, color, textcolor))


            elif(elementType == 'nav'):

                menu = []
                color = ""
                textcolor = ""

                if('menu' in attributes.keys()):
                    menu = attributes['menu']
                if('color' in attributes.keys()):
                    color = attributes['color']
                if('text_color' in attributes.keys()):
                    textcolor = attributes['text_color']

                return str(generate_nav(menu, color, textcolor))

        else: #show error
            print("Ouch ! Internal Error, We don't know the type of the element : "+elementName)
            quit()

    else: #it's a simple string or a variable error

        print("-------", self.children[0].tok)
        return str(content)


forNodeVars = {}


#ForNode : simple for
@addToClass(AST.ForNode)
def compile(self):

    varName = str(self.children.pop(0))
    fromInt = int(self.children.pop(0))
    toInt = int(self.children.pop(0))

    #forNodeVars.append(varName, fromInt)
    #forNodeVars[varName] = fromInt


    html = ""
    for i in range(fromInt, toInt):

        for child in self.children :
            res = child.compile()
            if isinstance(res, str):
                html += res


    return html



#PageAddition node is managed in syntaxeHTML and GeneratorHTML ;)
@addToClass(AST.PageAdditionNode)
def compile(self):
    print("Page addition")
    #nothing to do here ! :)





if __name__ == "__main__":
    from syntaxHTML import parse
    import sys
    prog = open("input_03.txt").read()
    ast = parse(prog)


    ast.compile()
