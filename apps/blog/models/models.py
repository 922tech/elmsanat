from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.urls import reverse
from apps.blog.services import BlogService
from .Mixins import SoftDeleteMixin, TitleMixin, DateMixin, IsActiveMixin


class Category(TitleMixin, IsActiveMixin, DateMixin):

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Blog Post Categories')


class Tag(TitleMixin, IsActiveMixin):

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='blog_tag'
    )
    object_id = models.PositiveBigIntegerField()
    content_objects = GenericForeignKey(
        'content_type',
        'object_id'
    )

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
 

class BlogFile(TitleMixin, SoftDeleteMixin):

    files = models.FileField(
        upload_to='files',
        verbose_name=_('file'),
    )
    
    url = models.CharField(max_length=1024, blank=True)

    def get_absolute_url(self):
        return reverse('view_file', args=[self.url])

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self.files.url
        print(self.url)
        return super().save(*args, **kwargs)

    def __str__(self):
        return "blog".join(self.files.url)

    class Meta:
        verbose_name = _('File')
        verbose_name_plural = _('Files')


class BlogImage(TitleMixin, SoftDeleteMixin):
    image = models.ImageField(upload_to='images/blog', verbose_name=_('تصویر'))
    url = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return "blog"+self.image.url

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self.image.url
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('image')
        verbose_name_plural = _('images')




class Post(TitleMixin, DateMixin, IsActiveMixin, SoftDeleteMixin):

    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE, 
        verbose_name=_('Category'),
        null=True,
        blank=True
    )

    thumbnail = models.ImageField(
        upload_to='./images/blog/thumbnails',
        blank=True, 
        null=True,
        default=None
    )
    
    # comment = models.ForeignKey(
    #     to=Comment, 
    #     on_delete=models.CASCADE, 
    #     null=True, 
    #     blank=True
    # )

    slug = models.SlugField(
        # unique=True,
        max_length=128, 
        null=False, 
        blank=True
    )

    views = models.IntegerField(
        verbose_name=_('Views number'), 
        default=0, 
        blank=True
    ) 

    writer = models.CharField(max_length=32, verbose_name=_('Auther'))
    content = models.TextField(verbose_name=_('Content'))
    # content = RichTextField(verbose_name=_('Content'))
    tags = GenericRelation(Tag)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = BlogService.slugify(self.title)
        return super().save(*args, **kwargs)
    

    def get_absolute_url(self):
        return reverse('view_post', args=[self.slug])

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Blog Posts')


class Comment(IsActiveMixin, DateMixin, SoftDeleteMixin):
    comment = models.TextField(verbose_name=_('Comment'))
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
