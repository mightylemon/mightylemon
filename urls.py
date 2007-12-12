
from django.conf.urls.defaults import *

def welcome(request):
    from django.http import HttpResponse
    return HttpResponse("coming soon. programming it now ;)")

urlpatterns = patterns("",
    (r"^admin/", include("django.contrib.admin.urls")),
    (r"^blog/", include("djog.urls")),
    (r"^$", welcome),
)
