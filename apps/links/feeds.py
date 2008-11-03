
from django.contrib.syndication import feeds

from links.models import Link

class LatestLinkFeed(feeds.Feed):
    """
    Feed of the latest 10 links.
    """
    title = "oebfare: Latest Links"
    link = "/blog/"
    
    def items(self):
        return Link.objects.all()[:10]
    
    def item_link(self, obj):
        return obj.url
    
    def item_guid(self, obj):
        # By default django.contrib.syndication uses the item_link as the
        # unique id for an item when item_guid is not present. Here we use
        # the link object primary key to identify this item since the
        # item_link could possible be duplicated over time.
        return str(obj.pk)
