
from django.conf.urls.defaults import *

from links.feeds import LatestLinkFeed

feeds = {
    "latest": LatestLinkFeed,
}

urlpatterns = patterns("",
    url(r"^feeds/(?P<url>.*)/$", "django.contrib.syndication.views.feed", {
        "feed_dict": feeds,
    }, name="links_feeds"),
)
