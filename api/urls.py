from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from api import views

app_name = "api"

urlpatterns = [
    path('users/current', views.CurrentUserView.as_view(), name='current_user'),

    path('comments', views.CommentsView.as_view(), name='comments'),
    path('comments/<int:comment_id>', views.SingleCommentView.as_view(),name='single_comment'),

    path('photos', views.PhotosView.as_view(), name='photos'),
    path('photos:import', views.ImportPhotosView.as_view(), name='import_photos'),
    path('photos/<int:photo_id>', views.SinglePhotoView.as_view(), name='single_photo'),
    path('photos/<int:photo_id>:recover', views.RecoverPhotoView.as_view(), name='recover_photo'),
    
    path('photos/<int:photo_id>/versions', views.PhotoVersionView.as_view(), name='photo_versions'),
    
    path('photos/<int:photo_id>/likes', views.LikesView.as_view(), name='photo_likes'),
    
    path('review_tickets/<int:ticket_id>', views.ReviewTicketView.as_view(), name="review_tickets"),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name=f'{app_name}:schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name=f'{app_name}:schema'), name='redoc'),

]