
from django.views.generic import date_based
from oebfare.blog.models import Post

def privileged_post_queryset(view_func):
    def _wrapped_view(request, **kwargs):
        if request.user.is_authenticated():
            kwargs["queryset"] = Post.objects.all()
        else:
            kwargs["queryset"] = Post.objects.active()
        return view_func(request, **kwargs)
    return _wrapped_view

def homepage(request, **kwargs):
    defaults = {
        "date_field": "pub_date",
        "num_latest": 3,
        "template_name": "homepage.html",
        "template_object_name": "posts",
    }
    defaults.update(kwargs)
    return date_based.archive_index(request, **defaults)
homepage = privileged_post_queryset(homepage)

object_detail = privileged_post_queryset(date_based.object_detail)
archive_day = privileged_post_queryset(date_based.archive_day)
archive_month = privileged_post_queryset(date_based.archive_month)
archive_year = privileged_post_queryset(date_based.archive_year)
