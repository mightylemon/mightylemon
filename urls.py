
from django.conf import settings
from django.conf.urls.defaults import *

from oebfare.blog.feeds import LatestPostFeed, LatestPostsByTagFeed
from oebfare.links.feeds import LatestLinkFeed

feeds = {
    "latest": LatestPostFeed,
    "tags": LatestPostsByTagFeed,
    "links": LatestLinkFeed,
}

urlpatterns = patterns("",
    url(r"^admin/", include("django.contrib.admin.urls")),
    url(r"^blog/", include("oebfare.blog.urls")),
    url(r"^comments/", include("django.contrib.comments.urls.comments")),
    url(r"^feeds/(?P<url>.*)/$", "django.contrib.syndication.views.feed", {
        "feed_dict": feeds,
    }),
    url(r"^$", "oebfare.blog.views.homepage", name="oebfare_home"),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns("django.views",
        url(r"^static/(?P<path>.*)", "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
