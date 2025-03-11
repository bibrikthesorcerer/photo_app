from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse

class PlainUserOnly(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.role == user.ROLE_USER
    
    def handle_no_permission(self):
        return JsonResponse({
            "error": "Permission denied",
            "message": "Admin and Staff users are not allowed to perform this action"
        }, status=403)