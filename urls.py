
from django.conf import settings
from django.conf.urls.defaults import *

def welcome(request):
    from django.http import HttpResponse
    return HttpResponse("coming soon. programming it now ;)")

urlpatterns = patterns("",
    (r"^admin/", include("django.contrib.admin.urls")),
    (r"^blog/", include("djog.urls")),
    (r"^$", welcome),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns("django.views.static",
        (r"static/(?P<path>.*)$", "serve", dict(
            document_root = settings.MEDIA_ROOT,
        ))
    )
