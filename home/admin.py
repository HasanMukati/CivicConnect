from django.contrib import admin
from .models import Category, Post, Comment, UserProfile, Suggestions, Favorite


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Suggestions)
admin.site.register(Favorite)

# Register your models here.
