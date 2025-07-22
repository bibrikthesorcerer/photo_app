from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from service_objects.services import ServiceOutcome

from api.serializers import UserProfileSerializer, ShowAccessTokenSerializer
from api.services import UpdateUserProfile, CreateUserProfile, SetNewUserApiToken
from api.docs import user_profile
from api.views import BaseView


class CurrentUserView(BaseView):
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
    

class UsersView(BaseView):
    
    @extend_schema(**user_profile.create_new_user_docs)
    def post(self, request):
        user = ServiceOutcome(
            CreateUserProfile,
            request.data
        ).result
        token = ServiceOutcome(
            SetNewUserApiToken,
            {"user": user}
        ).result
        data = ShowAccessTokenSerializer(token).data
        return Response(data=data)