from django.urls import path

from user.views import UserView, UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDelView

urlpatterns = [
    path('', UserView.as_view(), name="all_users"),
    path('list/', UserListView.as_view(), name="all_user"),
    path('<int:pk>', UserDetailView.as_view()),
    path('create/', UserCreateView.as_view(), name="user_create"),
    path('<int:pk>/update/', UserUpdateView.as_view()),
    path('<int:pk>/delete/', UserDelView.as_view()),
]