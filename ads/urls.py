from rest_framework import routers
from ads.views import AdViewSet

router = routers.SimpleRouter()
router.register('', AdViewSet)
urlpatterns = router.urls
