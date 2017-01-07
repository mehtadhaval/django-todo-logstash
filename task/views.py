# Create your views here.
import logging

from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from task.models import Task
from task.serializers import TaskSerializer

logger = logging.getLogger('todo.task')


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.filter(completed=False)
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        task = serializer.save(user=self.request.user)
        logger.info("Created task", extra={"event_type": "TASK_CREATED", "instance_id": task.id})

    def perform_destroy(self, instance):
        instance.is_active=False
        instance.save()
        logger.info("Removed task", extra={"event_type": "TASK_REMOVED", "instance_id": instance.id})

    def perform_update(self, serializer):
        super(TaskViewSet, self).perform_update(serializer)
        logger.info("Task updated", extra={"event_type": "TASK_UPDATED", "instance_id": serializer.instance.id})

    @detail_route(methods=['post'])
    def done(self, request, pk=None):
        instance = self.get_object()
        instance.completed = True
        instance.completed_on = timezone.now()
        instance.save()
        logger.info("Task marked as done", extra={"event_type": "TASK_DONE", "instance_id": instance.id})
        return Response()

    @list_route(queryset=Task.objects.filter(completed=True))
    def completed(self, request):
        return self.list(request)

    @list_route(queryset=Task.objects.all())
    def all(self, request):
        return self.list(request)

    @list_route(permission_classes=[AllowAny])
    def error(self, request):
        try:
            raise Exception("Test exception")
        except Exception as e:
            logger.exception("Exception")
            raise e
