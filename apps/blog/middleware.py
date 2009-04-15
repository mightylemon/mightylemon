from django import http
from django.core.urlresolvers import reverse
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
                callback = reverse('setup')
                if request.path == callback:
                    # We're going to the easy setup view
                    return None
                # Redirect to Google login
                from google.appengine.api import users
                return http.HttpResponseRedirect(users.create_login_url(callback))
            else:
                # Allow administration without a Blog
                # TODO use reverse to find admin urls
                if request.path.find('/admin') != 0:
                    raise Exception("Blog not found! Add a blog in the admin please.")
                request.blog = None
        return None