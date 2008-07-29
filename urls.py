
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin

admin.autodiscover()

# override the default handler500 so i can pass MEDIA_URL
handler500 = "oebfare.views.server_error"

urlpatterns = patterns("",
    url(r"^about/$", "django.views.generic.simple.direct_to_template", {
        "template": "about.html",
    }),
    url(r"^admin/(.*)", admin.site.root),
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
