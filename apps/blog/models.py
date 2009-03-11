
from datetime import datetime

from django.db import models
from django.conf import settings
from django.template import Context, loader
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _

from tagging.models import Tag
from tagging.fields import TagField
from mailer import send_mail
from comment_utils.moderation import CommentModerator, moderator

from blog.templatetags.blog_utils import rst_to_html


class PostManager(models.Manager):
    def active(self):
        return self.filter(active=True)
        

class Post(models.Model):
    title = models.CharField(_("title"), max_length=100)
    slug = models.SlugField(_("slug"), unique=True)
    body = models.TextField(_("body"))
    body_html = models.TextField(editable=False)
    markup_type = models.CharField(max_length=10, choices=(
        ("html", "HTML"),
        ("rst", "reStructuredText"),
    ), default="rst") # rst as default for backward compatibilty
    active = models.BooleanField(default=False)
    create_date = models.DateTimeField(_("created"), default=datetime.now)
    pub_date = models.DateTimeField(_("published"), default=datetime.now)
    tags = TagField()
    
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-pub_date",)
    
    @models.permalink
    def get_absolute_url(self):
        return ("blog_post_detail", (), {
            "year": self.pub_date.strftime("%Y"),
            "month": self.pub_date.strftime("%b").lower(),
            "day": self.pub_date.strftime("%d"),
            "slug": self.slug,
        })
    
    def save(self, **kwargs):
        if self.markup_type == "html":
            self.body_html = self.body
        elif self.markup_type == "rst":
            self.body_html = rst_to_html(self.body)
        super(Post, self).save(**kwargs)

class PostModerator(CommentModerator):
    akismet = True
    email_notification = True
    
    def email(self, comment, content_object):
        """
        Use django-mailer for mail delivery.
        """
        if not self.email_notification and not comment.is_public:
            return
        recipient_list = [manager_tuple[1] for manager_tuple in settings.MANAGERS]
        t = loader.get_template("comment_utils/comment_notification_email.txt")
        ctx = Context({
            "comment": comment,
            "content_object": content_object,
            "site": Site.objects.get_current(),
        })
        subject = _('[%s] Comment: "%s"') % (
            Site.objects.get_current().name,
            content_object,
        )
        message = t.render(ctx)
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

moderator.register(Post, PostModerator)
