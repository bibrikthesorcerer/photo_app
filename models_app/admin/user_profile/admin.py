from django.contrib import admin
from ...models import UserProfile
from forms import UserProfileForm

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'id', 'first_name', 'last_name']
    search_fields = list_display
    form = UserProfileForm 