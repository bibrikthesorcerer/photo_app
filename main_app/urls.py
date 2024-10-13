from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('upload/', views.UploadPhoto.as_view(), name='upload'),
    path('edit_photo/<int:id>', views.EditPhoto.as_view(), name='edit_photo'),
    path('view_photo_versions/<int:id>', views.ViewPhotoVersions.as_view(), name='view_photo_versions')
]