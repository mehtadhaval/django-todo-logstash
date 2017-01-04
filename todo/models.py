from django.db import models


class ActiveObjectsManager(models.Manager):
    def get_queryset(self):
        return super(ActiveObjectsManager, self).get_queryset().filter(is_active=True)


class SoftDeleteMixin(models.Model):
    is_active = models.BooleanField(default=True)

    active_objects = ActiveObjectsManager()
    objects = models.Manager()

    class Meta:
        abstract = True
