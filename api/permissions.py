from rest_framework import permissions

class IsOwner(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (obj.user == request.user) and super().has_permission(request, view)
 

class PlainUserOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return (super().has_permission(request, view) and request.user.role != request.user.ROLE_ADMIN)
