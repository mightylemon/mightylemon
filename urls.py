
from django.conf import settings
from django.conf.urls.defaults import *
from django.http import HttpResponseRedirect

urlpatterns = patterns("",
    (r"^admin/", include("django.contrib.admin.urls")),
    (r"^blog/", include("djog.urls")),
    (r"^$", lambda request: HttpResponseRedirect("/blog/")),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns("django.views.static",
        (r"static/(?P<path>.*)$", "serve", dict(
            document_root = settings.MEDIA_ROOT,
        ))
    )
