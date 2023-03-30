from django.urls import path

from user.views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDestroyView

urlpatterns = [
    path('', UserListView.as_view(), name="all_users"),
    path('list/', UserListView.as_view(), name="all_user"),
    path('<int:pk>', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view(), name="user_create"),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDestroyView.as_view()),
]
