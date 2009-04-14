
from django.conf.urls.defaults import *

from blog.models import Post
from blog.views import *
from blog.feeds import LatestPostFeed, LatestPostsByTagFeed

feeds = {
    "latest": LatestPostFeed,
    "tags": LatestPostsByTagFeed,
}

date_based_dict = {
    "date_field": "pub_date",
}

urlpatterns = patterns("",
    url(r"^feeds/(?P<url>.*)/$", "django.contrib.syndication.views.feed", {
        "feed_dict": feeds,
    }, name="blog_feeds"),
    
    url(r"tags/(?P<tag>[^/]+)/$", "tagging.views.tagged_object_list", {
        "queryset_or_model": Post,
        "template_name": "blog/post_tag_list.html",
        "related_tags": True,
    }, name="blog_tag_detail"),

    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$",
        object_detail, dict(date_based_dict, **{
            "template_object_name": "post",
        }), name="blog_post_detail"),
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$",
        archive_day, date_based_dict, name="blog_archive_daily"),
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/$",
        archive_month, date_based_dict, name="blog_archive_month"),
    url(r"^(?P<year>\d{4})/$",
        archive_year, date_based_dict, name="blog_archive_year"),

    url(r"^(?P<permalink>[-\w]+)/", permalinked, name="blog_permalink"),

    url(r"^$", archive_index, date_based_dict, name="blog_archive_index"),

    url(r"^archive/$", archive_full, name="blog_archive_full"),
)
