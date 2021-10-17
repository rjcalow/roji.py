
'''
converts markdown to html
seperated to allow quick swaping of markdown converters
or just add mdx extensions :)
'''
import markdown 
from mdx_extensions.figureAltCaption import FigureCaptionExtension
from mdx_extensions.mdx_urlize import UrlizeExtension
from mdx_extensions.mdx_headdown import DowngradeHeadingsExtension
from mdx_extensions.nlbqx import NLBQExtension

def mdtohtml(md):
    HTML =  markdown.markdown(md, extensions=[
        'tables', 'fenced_code',  FigureCaptionExtension(), UrlizeExtension(), DowngradeHeadingsExtension(), NLBQExtension()])

    return HTML