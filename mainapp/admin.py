from django.contrib import admin
from .models import Profile, Group, Post, Comment

admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(Post)
admin.site.register(Comment)

# Register your models here.
