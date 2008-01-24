
from django.contrib.syndication import feeds

from oebfare.blog.models import Post

class LatestPostFeed(feeds.Feed):
    """
    Feed of the latest 10 posts.
    """
    title = "oebfare latest entries"
    link = "/blog/"
    
    def items(self):
        return Post.objects.order_by("-pub_date")[:10]
