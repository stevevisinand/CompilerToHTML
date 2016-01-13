__author__ = 'stevevisinand'

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