from django.conf import settings

def forum_identity(request):
    return {'forum_name': settings.FORUM_NAME, 'forum_url': settings.FORUM_URL}
