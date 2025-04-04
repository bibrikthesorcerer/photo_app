from django.contrib import admin
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect


from .forms import UserProfileForm, AdminUserProfileForm
from models_app.models import UserProfile
from notifications.utils import send_message_to_list_of_users


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "role", "id", "email", "first_name", "last_name", "last_login"]
    search_fields = list_display
    list_filter = ["role", "last_login", "updated_at"]
    actions = ['send_notification']
    change_list_template = 'admin/models_app/user_profile/change_list.html'

    @admin.action(description="Send notification to list of users")
    def send_notification(self, request, queryset):
        if 'message' in request.POST:
            message = request.POST['message']
            ids = queryset.values_list('pk', flat=True)
            send_message_to_list_of_users(ids, 'send_notification', message)
            self.message_user(request, f"Message sent to {queryset.count()} users")
        return redirect(request.get_full_path())

    def get_form(self, request, obj=None, **kwargs):
        if (request.user.role == UserProfile.ROLE_ADMIN 
            and obj.role != UserProfile.ROLE_ADMIN):
            self.form = AdminUserProfileForm
            return super().get_form(request, obj, **kwargs)
        else: 
            self.form = UserProfileForm
            return super().get_form(request, obj, **kwargs)
            
    def has_change_permission(self, request, obj=None):
        if (obj
            and request.user != obj
            and obj.role == UserProfile.ROLE_ADMIN
            or request.user.role != UserProfile.ROLE_ADMIN):
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if (obj
            and request.user != obj
            and obj.role == UserProfile.ROLE_ADMIN
            or request.user.role != UserProfile.ROLE_ADMIN):
            return False
        return super().has_change_permission(request, obj)
