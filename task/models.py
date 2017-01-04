from django.conf import settings
from django.db import models


# Create your models here.
from todo.models import SoftDeleteMixin


class Task(SoftDeleteMixin):

    """This models represents a single entry in a TODO list"""

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title if len(self.title) < 30 else self.title[:30] + "..."
