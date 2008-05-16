
from django.conf import settings
from django.conf.urls.defaults import *

# override the default handler500 so i can pass MEDIA_URL
handler500 = "oebfare.blog.server_error"

urlpatterns = patterns("",
    url(r"^admin/", include("django.contrib.admin.urls")),
    url(r"^blog/", include("oebfare.blog.urls")),
    url(r"^comments/", include("django.contrib.comments.urls.comments")),
    url(r"^links/", include("oebfare.links.urls")),
    url(r"^$", "oebfare.blog.views.homepage", name="oebfare_home"),
)

if settings.LOCAL_DEV:
    urlpatterns += patterns("django.views",
        url(r"^static/(?P<path>.*)", "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )
