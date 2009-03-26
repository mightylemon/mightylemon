
from django.views.generic import date_based
from blog.models import Post
from django.template import RequestContext
from django.shortcuts import render_to_response

def privileged_post_queryset(view_func):
    def _wrapped_view(request, **kwargs):
        if request.user.is_authenticated():
            kwargs["queryset"] = request.blog.posts.all()
        else:
            kwargs["queryset"] = request.blog.posts.active()
        return view_func(request, **kwargs)
    return _wrapped_view

def homepage(request, **kwargs):
    defaults = {
        "date_field": "pub_date",
        "num_latest": request.blog.settings.posts_per_page,
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
archive_index = privileged_post_queryset(date_based.archive_index)

def archive_full(request, **kwargs):
    return render_to_response("blog/post_archive_full.html", {
        'posts': kwargs["queryset"], # all posts
    }, context_instance=RequestContext(request))
archive_full = privileged_post_queryset(archive_full)