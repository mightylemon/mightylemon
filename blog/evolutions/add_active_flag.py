
from django_evolution.mutations import *
from django.db import models

MUTATIONS = [
    AddField("Post", "active", models.BooleanField, initial=True),
]
