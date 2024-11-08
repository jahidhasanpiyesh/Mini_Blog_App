from django.contrib import admin
from .models import Post
# Register your models here.
@admin.register(Post)
class Post_Register(admin.ModelAdmin):
    list_display=['id','title','description']