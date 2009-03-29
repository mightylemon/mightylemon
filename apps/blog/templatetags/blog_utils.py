
from django.template import Library
from blog.util.code_hilite import to_html

register = Library()

register.filter("to_html", to_html)

def show_post_brief(context, post):
    return {
        "post": post,
        "last": context["forloop"]["last"],
        "can_edit": context["user"].is_staff,
    }
register.inclusion_tag("blog/post_brief.html", takes_context=True)(show_post_brief)

@register.filter
def date_microformat(d):
    '''
        Microformat version of a date.
        2009-02-10T02:58:00+00:00 (ideal)
        2009-02-09T17:54:41.181868-08:00 (mine)
    '''
    return d.isoformat()
