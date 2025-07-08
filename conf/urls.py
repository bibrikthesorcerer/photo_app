from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from main_app.views.user_profile.views import UserSignupView, UserLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', UserSignupView.as_view(), name="signup"),
    path('accounts/login/', UserLoginView.as_view(), name="login"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('main_app.urls', namespace='main')),
    path('', include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)