import pystache


def formatHtml(template, doc):
    return pystache.render(template, doc)
