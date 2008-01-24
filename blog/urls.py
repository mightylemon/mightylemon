
from django.conf.urls.defaults import *
from django.views.generic.date_based import *

from oebfare.blog.models import Post

date_based_dict = {
    "queryset": Post.objects.all(),
    "date_field": "pub_date",
}

urlpatterns = patterns("",
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$",
        object_detail, dict(date_based_dict, **{
            "template_object_name": "post",
        }), name="blog_post_detail"),
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$",
        archive_day, date_based_dict, name="blog_archive_daily"),
    url(r"^(?P<year>\d{4})/(?P<month>[a-z]{3})/$",
        archive_month, date_based_dict, name="blog_archive_month"),
    url(r"^(?P<year>\d{4})/$",
        archive_year, date_based_dict, name="blog_archive_year"),
)