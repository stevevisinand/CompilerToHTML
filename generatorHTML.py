__author__ = 'stevevisinand'

from syntaxHTML import pagesAddr
from syntaxHTML import pagesAdded

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

        if(pair[1] not in pagesAddr):
            print('Page must specify an address and a name. Error in page : ' + pair[1])
            quit()

        link = str(pagesAddr[pair[1]]['address']) #address is generated with syntaxHTML ! :D


        if pair[1] in pagesAdded.keys():


            underPages = pagesAdded[pair[1]]

            html = html + "<a href='#'><li>"+page+"<ul class='sous-menu'><a href='"+link+"'><li>"+page+"</li></a>"

            for page in underPages:

                if page not in pagesAddr.keys():
                    print("Mhm! it seems you forget the 'adress' or 'name' of the page : ", page )
                    quit()
                if 'name' not in pagesAddr[page].keys():
                    print("OUCH ! You didn't specify the 'name' of the page : ", page )
                    quit()


                page1 = str(pagesAddr[page]['name'])
                link1 = str(pagesAddr[page]['address'])
                html = html+ "<a href='"+link1+"'><li>"+page1+"</li></a>"

            html = html+ "</ul></li></a>"

        else:
            html = html+ "<a href='"+link+"'><li>"+page+"</li></a>"


    html = html+"""</ul>
            </div>
        </nav>"""

    return html


def cleanDir():
    import os
    filelist = [ f for f in os.listdir("./generatedSite/") if f.endswith(".htm") ]
    for f in filelist:
        os.remove("./generatedSite/"+f)

#
# Generate new page .htm and add contentHTML on it
#
def generate_page(pageName, pageAddr, contentHTML):

    pageHtml="""<!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8" />
                    <title>"""+pageName+"""</title>
                    <link rel="stylesheet" type="text/css" href="styles/styles.css">
                </head>
                <body>

                """+contentHTML+"""

                </body>
                </html>
                """

    fichier = open("./generatedSite/"+pageAddr,"w")
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
        <footer """+styles+""">
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
