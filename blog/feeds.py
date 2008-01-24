
from django.contrib.syndication import feeds
from django.core.exceptions import ObjectDoesNotExist

from tagging.models import Tag, TaggedItem

from oebfare.blog.models import Post

class LatestPostFeed(feeds.Feed):
    """
    Feed of the latest 10 posts.
    """
    title = "oebfare latest entries"
    link = "/blog/"
    
    def items(self):
        return Post.objects.all()[:10]

class LatestPostsByTagFeed(feeds.Feed):
    """
    Feed of latest 10 posts by a given tag.
    """
    link = "/blog/"
    
    def get_object(self, bits):
        if len(bits) != 1:
            raise ObjectDoesNotExist
        return Tag.objects.get(name=bits[0])
    
    def title(self, obj):
        return 'oebfare: Entries tagged with "%s"' % obj
    
    def description(self, obj):
        return 'The latest entries tagged with "%s"' % obj
    
    def items(self, obj):
        return TaggedItem.objects.get_by_model(Post, obj)
