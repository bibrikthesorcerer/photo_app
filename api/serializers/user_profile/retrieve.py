from rest_framework import serializers

from models_app.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        exclude=[
            'password', 'last_login',
            'groups', 'user_permissions',
            'is_superuser', 'is_staff', 'is_active'
        ]