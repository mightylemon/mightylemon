
from django.conf import settings
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect

def redirect(request):
    return HttpResponseRedirect("/blog/")

urlpatterns = patterns("",
    (r"^admin/", include("django.contrib.admin.urls")),
    (r"^blog/", include("oebfare.blog.urls")),
    (r"^$", redirect),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns("django.views.static",
        (r"static/(?P<path>.*)$", "serve", dict(
            document_root = settings.MEDIA_ROOT,
        ))
    )
