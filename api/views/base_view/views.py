from rest_framework.views import APIView

from api.authentication import RedisJWTAuth

class BaseView(APIView):
    authentication_classes = [RedisJWTAuth]
    permission_classes = []