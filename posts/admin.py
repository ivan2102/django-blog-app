from django.contrib import admin

from posts.models import Comments, Post, Subscribe, Tags, WebsiteMeta

# Register your models here.
admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(Comments)
admin.site.register(Subscribe)
admin.site.register(WebsiteMeta)
