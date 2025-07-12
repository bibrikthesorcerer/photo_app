from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from api.serializers import UserProfileSerializer
from api.services import UpdateUserProfile
from api.docs import user_profile


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**user_profile.get_current_user_docs)
    def get(self, request):        
        data = UserProfileSerializer(request.user).data
        return Response(data)
    
    @extend_schema(**user_profile.update_current_user_docs)
    def put(self, request):
        new_user_data = UpdateUserProfile.execute({**request.data}|{"user": request.user})
        data = UserProfileSerializer(new_user_data).data
        return Response(data)