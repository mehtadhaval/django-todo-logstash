from rest_framework.routers import DefaultRouter

from user.views import UserActionsViewSet

router = DefaultRouter()
router.register(r'', UserActionsViewSet)

urlpatterns = router.urls
