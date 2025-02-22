from django.contrib import admin

from .forms import UserProfileForm
from models_app.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "id", "first_name", "last_name"]
    search_fields = list_display
    form = UserProfileForm
