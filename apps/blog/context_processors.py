from django.conf import settings

def blog(request):
    return {
        'blog': request.blog,
    }

def stats(request):
    if not settings.DEBUG:
        return {
            'STATS_CODE': settings.STATS_CODE,
            }
    return {
        'STATS_CODE': "<!-- debug mode enabled / no stats tracking -->",
        }

