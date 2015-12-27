__author__ = 'hmut'


# Define later
class Page:
    """
    Class representing an HTML Page.
    Always contains a name and an adress.
    Also contains two empty lists.
    An elements list and a sub_pages list.
    """
    def __init__(self,name,address):
        self.name = name
        self.address = address
        self.elements = []
        self.sub_pages = []

    def __add__(self, other):
        self.sub_pages.append(other)

    def __repr__(self):
        return '\n' + 'Page: ' + self.name + ' @' + self.address + '\n' + str(self.elements) + '\n' + str(self.sub_pages)

    def add(self,other):
        if type(other) == Page:
            Page.__add__(self,other)
        else:
            self.elements.append(other)

class Element:
    """
    Abstract class representing the elements of a page
    """

    def __init__(self):
        self.type = 'abstract'
        self.name = 'no Name'
        self.attributes = {}

    def __repr__(self):
        return self.type + ' ' + self.name

    def setAttributes(self, attributes):
        for attrKey in attributes.keys():
            self.attributes[attrKey] = attributes.get(attrKey)


class Nav(Element):
    def __init__(self, name):
        Element.__init__(self)
        self.type = 'nav'
        self.name = name
        self.attributes = {'color': '#000', 'text_color': '#111', 'menu': {}}

    def __repr__(self):
        return '\n' + self.type + ' ' + self.name + '\nAttributes: ' + str(self.attributes)

    def setAttributes(self, attributes):
        Element.setAttributes(self, attributes)
        # Special action needs to be done for the menu map.
        menu = attributes['menu']
        # Temporary map
        nav_menu = {}
        for key in menu.keys():
            nav_menu[key] = menu.get(key)
        self.attributes['menu'] = nav_menu


class Header(Element):
    def __init__(self, name):
        Element.__init__(self)
        self.type = 'header'
        self.name = name
        self.attributes = {'color': '#000', 'text_color': '#111', 'title': 'none'}

    def __repr__(self):
        return '\n' + self.type + ' ' + self.name + '\nAttributes: ' + str(self.attributes)


class Footer(Element):
    def __init__(self, name):
        Element.__init__(self)
        self.type = 'footer'
        self.name = name
        self.attributes = {'color': '#000', 'text_color': '#111', 'title': 'none', 'paragraph': 'HE-ARGH industries',
                           'copyright': 'Le Mutz and CIE.'}

    def __repr__(self):
        return '\n' + self.type + ' ' + self.name + '\nAttributes: ' + str(self.attributes)
