from django_filters import views
from rest_framework.routers import DefaultRouter

from telegram.views import TelegramCallbackViewSet

router = DefaultRouter()
router.register('telegram_webhook', TelegramCallbackViewSet, basename='telegram_webhook')
urlpatterns = router.urls
