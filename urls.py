from django.conf import settings
from django.conf.urls.defaults import *


# override the default handler500 so i can pass MEDIA_URL
handler500 = "views.server_error"

urlpatterns = patterns("",
    url(r"^about/$", "django.views.generic.simple.direct_to_template", {
        "template": "about.html",
    }),
    url(r"^hire-me/$", "django.views.generic.simple.direct_to_template", {
    "template": "hire-me.html",
    }),
    url(r"^blog/", include("blog.urls")),
    url(r"^comments/", include("django.contrib.comments.urls")),
    url(r"^links/", include("links.urls")),
    url(r"^$", "blog.views.homepage", name="oebfare_home"),
    # callback for google login
    url(r"^setup/", "blog.views.setup", name="setup"),
)

if settings.LOCAL_DEVELOPMENT:
    urlpatterns += patterns("django.views",
        url(r"^static/(?P<path>.*)", "static.serve", {
            "document_root": settings.MEDIA_ROOT,
        })
    )

if not settings.APP_ENGINE:
    # Admin for non-GAE
    from django.contrib import admin
    admin.autodiscover()

    urlpatterns += patterns("",
        url(r"^admin/doc/", include("django.contrib.admindocs.urls")),
        url(r"^admin/(.*)", admin.site.root),
    )