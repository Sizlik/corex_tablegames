from rest_framework.routers import DefaultRouter

from message.views import MessageViewSet, ButtonViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'buttons', ButtonViewSet, basename='button')
urlpatterns = router.urls
