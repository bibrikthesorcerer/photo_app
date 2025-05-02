from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from main_app.views.user_profile.views import UserSignupView, UserLoginView, VerifyPasswordView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', UserSignupView.as_view(), name="signup"),
    path('accounts/login/', UserLoginView.as_view(), name="login"),
    path('accounts/verify_password/<user_idb64>/<token>/', VerifyPasswordView.as_view(), name="verify_password"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main_app.urls', namespace='main')),
    path('', include('social_django.urls', namespace='social')),
    path('api/', include('api.urls', namespace='api')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)