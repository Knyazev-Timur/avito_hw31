from rest_framework import routers
from cat.views import CategoryViewSet

router = routers.SimpleRouter()
router.register('', CategoryViewSet)
urlpatterns = router.urls
