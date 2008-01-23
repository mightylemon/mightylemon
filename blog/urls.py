
from django.conf.urls.defaults import *
from django.views.generic.date_based import *

from oebfare.blog.models import Post

datebased_dict = {
    "queryset": Post.objects.all(),
    "date_field": "pub_date",
}

urlpatterns = patterns("",
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$",
        object_detail, dict(datebased_dict, **{
            "template_object_name": "post",
        }), name="blog_post_detail"),
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$",
        archive_day, datebased_dict, name="blog_archive_daily"),
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/$",
        archive_month, datebased_dict, name="blog_archive_month"),
    url(r"^(?P<year>\d{4})/$",
        archive_year, datebased_dict, name="blog_archive_year"),
    url(r"^$",
        archive_index, datebased_dict, name="blog_index"),
)
