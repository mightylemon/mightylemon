from blog.models import Blog
import settings


class BlogMiddleware:

    def process_request(self, request):
        """
        Sets request.blog to the first Blog. Lame.
        Multiple blogs is too ambitious for now.
        """
        try:
            if settings.APP_ENGINE:
                request.blog = Blog.all()[0]
            else:
                request.blog = Blog.objects.all()[0]
        except IndexError:
            if settings.APP_ENGINE:
                blog = Blog(title="Oebfare", author=None)
                blog.put()
                request.blog = blog
            else:
                # Allow administration without a Blog
                # TODO use reverse to find admin urls
                if request.path.find('/admin') != 0:
                    raise Exception("Blog not found! Add a blog in the admin please.")
                request.blog = None
        return None