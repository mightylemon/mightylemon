from blog.models import Blog


class BlogMiddleware:

    def process_request(self, request):
        """
        Sets request.blog to the first Blog. Lame.
        Multiple blogs is too ambitious for now.
        """
        try:
            request.blog = Blog.objects.all()[0]
        except IndexError:
            # Allow administration without a Blog
            # TODO use reverse to find admin urls
            if request.path.find('/admin') != 0:
                raise Exception("Blog not found! Add a blog in the admin please.")
            request.blog = None
        return None