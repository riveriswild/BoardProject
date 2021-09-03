from django.contrib import admin
from .models import Post, Category, Reaction, Profile

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Reaction)
admin.site.register(Profile)
# Register your models here.
