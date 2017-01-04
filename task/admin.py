from django.contrib import admin

from task.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "completed", "user", "created")


admin.site.register(Task, TaskAdmin)
