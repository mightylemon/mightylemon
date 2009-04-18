from django.views.generic.list_detail import object_list, object_detail
from events.models import Event

def event_list(request):
    return object_list(request,
                       Event.objects.all(),
                       template_object_name='event')

def event_detail(request, slug):
    return object_detail(request,
                         Event.objects.all(),
                         slug=slug,
                         template_object_name='event')
