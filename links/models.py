
from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Link(models.Model):
    name = models.CharField(_("name"), max_length=100)
    url = models.URLField(_("URL"), verify_exists=False)
    description = models.TextField(_("description"))
    created = models.DateTimeField(editable=False, default=datetime.now)
    
    def __unicode__(self):
        return u"%s (%s)" % (self.name, self.url)
    
    class Admin:
        pass
    
    class Meta:
        ordering = ("-created",)
