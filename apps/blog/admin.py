
from django.contrib import admin
from blog.models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "pub_date")
    list_display_links = ("id", "title")
    search_fields = ("title", "text")
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Post, PostAdmin)
