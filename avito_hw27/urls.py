
"""avito_hw27 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

import ads
from ads.views import index, CatView, CatDetailView, CatListView, CatCreateView, CatUpdateView, CatDelView, AdViewSet
from user.views import LocationViewSet


router = routers.SimpleRouter()
router.register('location', LocationViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('user/', include("user.urls")),
    path('ads/', include("ads.urls")),

    path('cat/<int:pk>', CatDetailView.as_view()),
    path('cat/', CatListView.as_view(), name="all_category"),
    path('cat/create/', CatCreateView.as_view(), name="category_create"),
    path('cat/<int:pk>/update/', CatUpdateView.as_view()),
    path('cat/<int:pk>/delete/', CatDelView.as_view()),
]

urlpatterns += router.urls


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
