import settings

if settings.APP_ENGINE:
    from appengine_django.models import db, BaseModel
    Model = BaseModel
    from appengine_django.auth.models import User
else:
    from django.db import models
    Model = models.Model
    from django.contrib.auth.models import User


class UserProfile(Model):
    """
    Not everyone is Brian Rosner.
    """
    if settings.APP_ENGINE:
        user = db.ReferenceProperty(User)
        full_name = db.StringProperty(required=False)
        nickname = db.StringProperty(required=False)
        about_me = db.StringProperty(required=False)
    else:
        user = models.ForeignKey(User, unique=True)
        full_name = models.CharField(max_length=60, blank=True)
        nickname = models.CharField(max_length=30, blank=True)
        about_me = models.TextField(blank=True)