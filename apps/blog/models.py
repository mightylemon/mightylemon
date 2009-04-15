from datetime import datetime

from django.utils.translation import ugettext_lazy as _

import settings

if settings.APP_ENGINE:
    from appengine_django.models import db, BaseModel
    Model = BaseModel
    from appengine_django.auth.models import User
else:
    from django.db import models
    Model = models.Model
    from django.contrib.auth.models import User
    #from django.conf import settings
    from django.template import Context, loader
    from django.contrib.sites.models import Site

    from tagging.models import Tag
    from tagging.fields import TagField
    from mailer import send_mail
    from comment_utils.moderation import CommentModerator, moderator

class Blog(Model):
    if settings.APP_ENGINE:
        title = db.StringProperty(required=True)
        author = db.ReferenceProperty(User)
    else:
        title = models.CharField(_("title"), max_length=100)
        author = models.ForeignKey(User, related_name=_("author"))

    def __unicode__(self):
        return self.title

    @property
    def settings(self):
        from settings import APP_ENGINE
        if APP_ENGINE:
            try:
                return self.blogsettings_set[0]
            except IndexError:
                settings = BlogSettings(blog=self)
                settings.put()
                return settings
        else:
            try:
                return self.blogsettings_set.all()[0]
            except IndexError:
                settings = BlogSettings(blog=self)
                settings.save()
                return settings


class BlogSettings(Model):
    # Good enough for now
    if settings.APP_ENGINE:
        blog = db.ReferenceProperty(Blog)
        posts_per_page = db.IntegerProperty(required=True, default=6)
    else:
        blog = models.ForeignKey(Blog)
        posts_per_page = models.PositiveIntegerField(_("posts per page"), default=6)

    class Meta:
        verbose_name_plural = 'Blog Settings'

    def __unicode__(self):
        return "%s settings" % self.blog.title


if not settings.APP_ENGINE:
    class PostManager(models.Manager):
        def active(self):
            return self.filter(active=True)
        

class Post(Model):
    if settings.APP_ENGINE:
        blog = db.ReferenceProperty(Blog)
    else:
        blog = models.ForeignKey(Blog, related_name=_("posts"))
        title = models.CharField(_("title"), max_length=100)
        slug = models.SlugField(_("slug"), unique=True)
        body = models.TextField(_("body"))
        markup_type = models.CharField(max_length=10, choices=(
            ("html", "HTML"),
            ("rst", "reStructuredText"),
            ("markdown", "Markdown"),
        ), default="html")
        active = models.BooleanField(default=False)
        create_date = models.DateTimeField(_("created"), default=datetime.now)
        pub_date = models.DateTimeField(_("published"), default=datetime.now)
        enable_comments = models.BooleanField(default=True)
        tags = TagField()
        
        objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")
        ordering = ("-pub_date",)
    
    #@models.permalink
    def get_absolute_url(self):
        return ("blog_post_detail", (), {
            "year": self.pub_date.strftime("%Y"),
            "month": self.pub_date.strftime("%b").lower(),
            "day": self.pub_date.strftime("%d"),
            "slug": self.slug,
        })


if not settings.APP_ENGINE:
    class PostModerator(CommentModerator):
        akismet = True
        email_notification = True
        enable_field = "enable_comments"
        
        def email(self, comment, content_object):
            """
            Use django-mailer for mail delivery.
            """
            if self.email_notification and not comment.is_public:
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