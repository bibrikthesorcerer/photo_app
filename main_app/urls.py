from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('accounts/signup/', views.UserSignupView.as_view(), name="signup"),
    path('accounts/login/', views.UserLoginView.as_view(), name="login"),
    path('accounts/verify_password/<user_idb64>/<token>/', views.VerifyPasswordView.as_view(), name="verify_password"),
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('upload/', views.UploadPhoto.as_view(), name='upload'),
    path('edit_photo/<int:photo_id>', views.EditPhoto.as_view(), name='edit_photo'),
    path('view_photo/<int:photo_id>', views.ViewPhoto.as_view(), name='view_photo'),
    path('view_photo_versions/<int:photo_id>', views.ViewPhotoVersions.as_view(), name='view_photo_versions'),
    path('delete_photo/<int:photo_id>', views.DeletePhoto.as_view(), name='delete_photo'),
    path('recover_photo/<int:photo_id>', views.RecoverPhoto.as_view(), name='recover_photo'),
    path('create_like/', views.CreateLike.as_view(), name='create_like'),
    path('remove_like/', views.RemoveLike.as_view(), name='remove_like'),
    path('view_thread/<int:comment_id>', views.ViewThread.as_view(), name='view_thread'),
    path('leave_comment/', views.LeaveCommentView.as_view(), name='leave_comment'),
    path('delete_comment/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path('edit_comment/', views.EditCommentView.as_view(), name='edit_comment'),
    path('generate_token/', views.GenerateUserAPIToken.as_view(), name='generate_token')
]