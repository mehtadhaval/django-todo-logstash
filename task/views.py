# Create your views here.
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from task.models import Task
from task.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):

    queryset = Task.objects.filter(completed=False)
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_active=False
        instance.save()

    @detail_route(methods=['post'])
    def done(self, request, pk=None):
        instance = self.get_object()
        instance.completed = True
        instance.completed_on = timezone.now()
        instance.save()
        return Response()

    @list_route(queryset=Task.objects.filter(completed=True))
    def completed(self, request):
        return self.list(request)

    @list_route(queryset=Task.objects.all())
    def all(self, request):
        return self.list(request)
