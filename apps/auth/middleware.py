from django.contrib.auth.models import User


class AuthorMiddleware:

    def process_request(self, request):
        """
        Sets request.author to the first User. Lame.
        Multiple blogs/authors is too ambitious for now.
        """
        try:
            request.author = User.objects.all()[0]
        except IndexError:
            raise Exception("Blog author not found! Add an author in the admin please.")
        return None