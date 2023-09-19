from django.contrib import admin
from .models.models import Post, Category, Tag, BlogFile, BlogImage, Comment
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.admin import helpers, utils

@admin.register(Post)
class CommentAdmin(admin.ModelAdmin):
    lookup_fields = ['title','writer']

    def get_manager(self):
        return self.model.objects
    
    def changelist_view(self, request, extra_context=None):
        if not request.POST:
            obj = self.model()
        else:
            kwargs = {i:request.POST[i] for i in self.lookup_fields if request.POST[i]}
            print(kwargs)
            obj = self.model.objects.get(**kwargs)
        fieldsets = self.get_fieldsets(request, obj)
        ModelForm = self.get_form(
            request, obj, change=False, fields=utils.flatten_fieldsets(fieldsets)
        )
        form = ModelForm(instance=obj)
        adminForm = helpers.AdminForm(
            form,
            list(fieldsets),
            # Clear prepopulated fields on a view-only form to avoid a crash.
            self.get_prepopulated_fields(request, obj)
            if  self.has_change_permission(request, obj)
            else {},
            [],
            model_admin=self,
        )
        context = {
            'opts':self.opts,
            'adminform':adminForm
        }

        return render(request, 'changelist.html',context)
    
    
# models = [Post, Category, Tag, BlogFile,  BlogImage]
# admin.site.register(models)
# Register your models here.
