from django.contrib import admin

from social_network.models import Post, Like, Comment, Tag, Image

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Image)
