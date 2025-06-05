from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service_objects.errors import ServiceObjectLogicError, InvalidInputsError

from api.authentication import RedisJWTAuth

class BaseView(APIView):
    authentication_classes = [RedisJWTAuth]
    permission_classes = []
