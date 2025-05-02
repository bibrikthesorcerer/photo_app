from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.serializers import UserProfileSerializer
from api.services import UpdateUserProfile

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):        
        data = UserProfileSerializer(request.user).data
        return Response(data)
    
    def put(self, request):
        new_user_data = UpdateUserProfile.execute({**request.data}|{"user": request.user})
        data = UserProfileSerializer(new_user_data).data
        return Response(data)