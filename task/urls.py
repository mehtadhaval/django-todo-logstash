from rest_framework.routers import DefaultRouter

from task.views import TaskViewSet

router = DefaultRouter()
router.register(r'', TaskViewSet)

urlpatterns = router.urls
