
from django.contrib import admin
from blog.models import Blog, BlogSettings, Post
from django.contrib.comments.admin import CommentsAdmin
from django.contrib.comments.models import Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author")


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "pub_date", "active")
    list_filter = ("active",)
    list_display_links = ("id", "title")
    search_fields = ("title", "text")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogSettings)
admin.site.register(Post, PostAdmin)

admin.site.unregister(Comment)

class CommentsDisplayGenericObjectAdmin(CommentsAdmin):
    list_display = ('name', 'commented_object', 'ip_address',
                    'submit_date', 'is_public', 'is_removed')

    def commented_object(self, obj):
        return '<a href="%s">%s</a>' % (self.commented_obj_url(obj.content_object), obj.content_object)
    commented_object.allow_tags=True

    def commented_obj_url(self, obj):
        # hackish, needs to actually do a reverse lookup
        return '/admin/%s/%s/%s/' % (obj._meta.app_label,
                                     obj._meta.module_name,
                                     obj.id)
  
admin.site.register(Comment, CommentsDisplayGenericObjectAdmin)