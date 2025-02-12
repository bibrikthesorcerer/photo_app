from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('upload/', views.UploadPhoto.as_view(), name='upload'),
    path('edit_photo/<int:id>', views.EditPhoto.as_view(), name='edit_photo'),
    path('view_photo/<int:id>', views.ViewPhoto.as_view(), name='view_photo'),
    path('view_photo_versions/<int:id>', views.ViewPhotoVersions.as_view(), name='view_photo_versions'),
    path('delete_photo/<int:id>', views.DeletePhoto.as_view(), name='delete_photo'),
    path('recover_photo/<int:id>', views.RecoverPhoto.as_view(), name='recover_photo'),
    path('create_like', views.CreateLike.as_view(), name='create_like'),
    path('remove_like', views.RemoveLike.as_view(), name='remove_like'),
    path('view_thread/<int:id>', views.ViewThread.as_view(), name='view_thread'),
    path('leave_comment/', views.LeaveCommentView.as_view(), name='leave_comment'),
    path('delete_comment/<int:id>', views.DeleteCommentView.as_view(), name='delete_comment'),
]