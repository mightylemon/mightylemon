
from django.template import Library, Node

from links.models import Link

register = Library()

class GetLinksNode(Node):
    def __init__(self, context_var, limit):
        self.context_var = context_var
        self.limit = limit
    
    def render(self, context):
        links = Link.objects.all()
        if self.limit:
            links = links[:self.limit]
        context[self.context_var] = links
        return u""

def do_get_links(parser, token):
    """
    Usage:
        
        To fetch all links and store them to the context variable ``links``
        simply::
            
            {% get_links as links %}
        
        If you want to limit the number of links fetched then limit the
        results::
            
            {% get_links as links limit 5 %}
    """
    return GetLinksNode("links", 5)
register.tag("get_links")(do_get_links)
