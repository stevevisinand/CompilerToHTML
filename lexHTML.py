import ply.lex as lex

reserved_words = (
    'page',
    'name',
    'address',
    'content',
    'element',
    'nav',
    'header',
    'footer',
    'title',
    'color',
    'text',
    'text_color',
    'paragraph',
    'copyright',
    'menu',
    'for',
    'from',
    'to',
    'print',
    'ws',
)

tokens = (
             'IDENTIFIER',
             'STRING',
             'NUMBER',
             'COMMENT',
             'CONDITION',
             'DELTA',
             'ADD_OP'
         ) + tuple(map(lambda s: s.upper(), reserved_words))

literals = '(),:;={}[]"/+-*><.'


def t_IDENTIFIER(t):
    r'[A-Za-z_]\w*'
    if t.value in reserved_words:
        t.type = t.value.upper()
    return t


# TODO Lukas - Please define the limits of what can be considered a string and what cannot.
def t_STRING(t):
    r'"[A-Za-z _#()./1-9]*\"'
    t.value = t.value[1:-1]
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    try:
        t.value = float(t.value)
    except ValueError:
        print ("Line %d: Problem while parsing %s!" % (t.lineno, t.value))
        t.value = 0
    return t


def t_CONDITION(t):
    r'([<>]([=]?)|(([=!]=)))'
    t.value = t.value
    return t


def t_DELTA(t):
    r'([\+]+|[\-]+)'
    t.value = t.value
    return t


# Comments should actually be ignored.
# Using code from GardenSnake PLY example.

# Putting this before t_WS let it consume lines with only comments in
# them so the latter code never sees the WS part.  Not consuming the
# newline.  Needed for "if 1: #comment"
def t_COMMENT(t):
    r'[ ]*\/\/[^\n]*'
    # t.value = t.value[2:] # for debugging only
    # print t.value         # for debugging only
    pass


# Whitespace
def t_WS(t):
    r'[ ]+'
    if t.lexer.at_line_start and t.lexer.paren_count == 0:
        return t


#
# def t_COMMENT(t):
#     r'//[A-Za-z _][^\n]*'
#     t.value = t.value[2:]
#     return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t'


def t_error(t):
    print ("Illegal character '%s'" % repr(t.value[0]))
    t.lexer.skip(1)


lex.lex()

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    lex.input(prog)

    while 1:
        tok = lex.token()
        if not tok: break
        print ("line %d: %s(%s)" % (tok.lineno, tok.type, tok.value))
