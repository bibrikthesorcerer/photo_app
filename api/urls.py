from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path('users/current', views.CurrentUserView.as_view(), name='current_user'),
    path('comments', views.CommentsView.as_view(), name='comments'),
]