from django.urls import path

from ads.views import AdDetailView, AdListView, AdCreateView, AdUpdateView, AdDelView, AdUploadImg


urlpatterns = [
    path('<int:pk>/', AdDetailView.as_view()),
    path('', AdListView.as_view(), name="all_ads"),
    path('create/', AdCreateView.as_view(), name="ads_create"),
    path('<int:pk>/update/', AdUpdateView.as_view()),
    path('<int:pk>/delete/', AdDelView.as_view()),
    path('<int:pk>/upload_image/', AdUploadImg.as_view()),
]
