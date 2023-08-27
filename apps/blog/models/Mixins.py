from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return self.update(is_delete=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).exclude(is_deleted=True)
    
    def deleted_objects(self)  -> QuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=True)

    

# class DeletedObjectsManager(models.Manager):
#     def get_queryset(self) -> QuerySet:
#         return super().get_queryset().filter(is_deleted=True)
    

class SoftDeleteMixin(models.Model):
    is_deleted = models.BooleanField(
        default=False, 
        choices=[(True,'Yes'), (False,'No')]
    )
    deleted_on = models.DateTimeField(null=True, blank=True, verbose_name='Deleted on')
    objects = SoftDeleteManager()
    # deleted_objects = DeletedObjectsManager()
    def delete(self):
        self.is_deleted = True
        self.deleted_on = timezone.now()
        if hasattr(self, 'is_active'):
            self.is_active = False
        self.save()

    class Meta:
        abstract = True


class TitleMixin(models.Model):
    title = models.CharField(
        max_length=64, 
        verbose_name=_('Title'), 
        # unique=True
        )

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class DateMixin(models.Model):
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))

    class Meta:
        abstract = True

        
class IsActiveMixin(models.Model):
    is_active = models.BooleanField(
        default=False,
        choices=[(True,_('Yes')), (False,_('No'))]
    )
    class Meta:
        abstract = True
