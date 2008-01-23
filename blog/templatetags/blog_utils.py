
from django.template import Library

register = Library()

def show_post(post):
    return dict(post=post)
register.inclusion_tag("blog/post_brief.html")(show_post)
