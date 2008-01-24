
from django.views.generic.date_based import archive_index

from oebfare.blog.models import Post

def homepage(request):
    return archive_index(request, **{
        "queryset": Post.objects.all(),
        "date_field": "pub_date",
        "num_latest": 3,
        "template_name": "homepage.html",
        "template_object_name": "posts",
    })
