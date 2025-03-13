from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import JsonResponse

class PlainUserOnly(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role == user.ROLE_USER
    
    def handle_no_permission(self):
        return JsonResponse({
            "error": "Permission denied",
            "message": "You are not allowed to perform this action"
        }, status=403)