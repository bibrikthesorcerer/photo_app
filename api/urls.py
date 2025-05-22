from django.urls import path

from api import views

app_name = "api"

urlpatterns = [
    path('users/current', views.CurrentUserView.as_view(), name='current_user'),

    path('comments', views.CommentsView.as_view(), name='comments'),
    path('comments/<int:comment_id>', views.SingleCommentView.as_view(),name='single_comment'),

    path('photos', views.PhotosView.as_view(), name='photos'),
    path('photos/<int:photo_id>', views.SinglePhotoView.as_view(), name='single_photo')
]