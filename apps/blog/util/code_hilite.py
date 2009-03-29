from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, TextLexer

from docutils import nodes
from docutils.writers import html4css1
from docutils.core import publish_parts
from docutils.parsers.rst import directives

import markdown

from django.utils.safestring import mark_safe


#rst -> HTML with code hiliting
VARIANTS = {}

def pygments_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):
    try:
        lexer = get_lexer_by_name(arguments[0])
    except (ValueError, IndexError):
        # no lexer found - use the text one instead of an exception
        lexer = TextLexer()
    parsed = highlight(u"\n".join(content), lexer, HtmlFormatter())
    return [nodes.raw("", parsed, format="html")]
pygments_directive.arguments = (0, 1, False)
pygments_directive.content = 1
pygments_directive.options = dict([(key, directives.flag) for key in VARIANTS])

directives.register_directive("sourcecode", pygments_directive)


class HTMLWriter(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator

class HTMLTranslator(html4css1.HTMLTranslator):
    named_tags = []
    
    def visit_literal(self, node):
        # TODO: wrapping fixes.
        self.body.append("<code>%s</code>" % node.astext())
        raise nodes.SkipNode


def rst_to_html(value):
    parts = publish_parts(source=value, writer=HTMLWriter(),
        settings_overrides={"initial_header_level": 2})
    return parts["fragment"]


#markdown -> HTML with code hiliting
# http://lethain.com/entry/2008/jan/09/cleanly-extending-python-markdown-syntax-highlight/

class CodeBlockProcessor(markdown.Preprocessor):
    """
    Code from http://lethain.com/entry/2008/jan/09/cleanly-extending-python-markdown-syntax-highlight/
    
    This will cause a full scan of the input text for lines beginning with @@.  Blocks that fall between
    @@ tags will be assumed to be code blocks and formatted with pygments, the language must be specified
    after the tag.
    """
    def run(self, lines):
        new_lines = []
        seen_start = False
        lang = None
        block = []
        for line in lines:
            untouched = line
            line = line.lstrip()
            if line.startswith("@@") and not seen_start:
                lang = line.strip("@@").strip()
                seen_start = True
            elif line.startswith("@@") and seen_start:
                try:
                    lexer = get_lexer_by_name(lang)
                except (ValueError, IndexError):
                        # no lexer found - use the text one instead of an exception
                        lexer = TextLexer()
                block[-1] = block[-1].rstrip()
                content = "\n".join(block)
                highlighted = highlight(content, lexer, HtmlFormatter())
                new_lines.append("%s" % (highlighted))
                lang = None
                block = []
                seen_start = False
            elif seen_start is True:
                block.append(line)
            else:
                new_lines.append(untouched)
        return new_lines

def extendMarkdown(md):
    md.preprocessors.append(CodeBlockProcessor())
    print md.preprocessors
    
    

def markdown_to_html(text):
    """
    Convert markdown to HTML with code hiliting
    """
    md = markdown.Markdown()
    extendMarkdown(md)
    md.source = text
    return unicode(md)

def to_html(obj):
    """
    Markup filter that converts an object to html formatting.  Support for rst, and markdown with syntax hiliting.
    """
    if obj.markup_type == "html":
        html = obj.body
    elif obj.markup_type == "rst":
        html = rst_to_html(obj.body)
    elif obj.markup_type == "markdown":
        html = markdown_to_html(obj.body)
    return mark_safe(html)


