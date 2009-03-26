from django.db.models.signals import post_syncdb
from django.contrib.auth.models import User
from blog.models import Blog

def make_blog(sender, **kwargs):
    """
    Create a new blog during syncdb. The user
    *should* create a superuser so assume that
    this is the blog author.
    """
    if not kwargs['interactive']:
        return

    # Do nothing if a blog already exists
    try:
        blog = Blog.objects.all()[0]
        return
    except IndexError:
        pass

    # Create a blog if a user exists
    try:
        author = User.objects.all()[0]
    except IndexError:
        return

    try:
        # Prompt for a blog title
        title = raw_input('Blog title: ')
        blog = Blog(title=title, author=author)
        blog.save()
    except KeyboardInterrupt:
        sys.stderr.write("\nOperation cancelled.\n")
        sys.exit(1)

post_syncdb.connect(make_blog)