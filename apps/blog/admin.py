from django.contrib import admin
from .models.models import Post, Category, Tag, BlogFile, BlogImage, Comment


@admin.action(description="Of which post?")
def post(modeladmin, request, queryset):
    return list(Post.objects.all().values_list('slug').all())


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    actions=(post,)
    
models = [Post, Category, Tag, BlogFile,  BlogImage]
admin.site.register(models)
# Register your models here.
