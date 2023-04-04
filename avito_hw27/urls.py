from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from ads.views import index, CatDetailView, CatListView, CatCreateView, CatUpdateView, CatDelView
from user.views import LocationViewSet

router = routers.SimpleRouter()
router.register('location', LocationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('user/', include("user.urls")),
    path('ads/', include("ads.urls")),
    path('selection/', include("ads.selection_urls")),

    path('cat/<int:pk>', CatDetailView.as_view()),
    path('cat/', CatListView.as_view(), name="all_category"),
    path('cat/create/', CatCreateView.as_view(), name="category_create"),
    path('cat/<int:pk>/update/', CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CatDelView.as_view()),
]

urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
