
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Feed(models.Model):
    name = models.CharField(_("name"), max_length=100)
    url = models.URLField(_("url"))
    
    def __unicode__(self):
        return self.name
