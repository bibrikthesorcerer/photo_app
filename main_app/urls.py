from django.urls import path
from . import views

app_name = 'main_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('upload/', views.UploadPhoto.as_view(), name='upload'),
    path('edit_photo/<int:id>', views.EditPhoto.as_view(), name='edit_photo'),
    path('view_photo_versions/<int:id>', views.ViewPhotoVersions.as_view(), name='view_photo_versions'),
    path('delete_photo/<int:id>', views.DeletePhoto.as_view(), name='delete_photo'),
    path('recover_photo/<int:id>', views.RecoverPhoto.as_view(), name='recover_photo'),
    path('search', views.SearchView.as_view(), name='search'),
    path('sort', views.SortView.as_view(), name='sort'),
    path('create_like', views.CreateLike.as_view(), name='create_like'),
    path('remove_like', views.RemoveLike.as_view(), name='remove_like')
]