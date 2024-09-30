from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include('main_app.urls', namespace='main')),
    path('', include('social_django.urls', namespace='social')),
]
