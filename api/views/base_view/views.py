from rest_framework.views import APIView
from service_objects.services import ServiceOutcome, ServiceWithResult

from api.authentication import RedisJWTAuth

class BaseView(APIView):
    authentication_classes = [RedisJWTAuth]
    permission_classes = []

    def _get_object_with_permission_check(self, service: ServiceWithResult, additional_inputs: dict = {}):
        outcome = ServiceOutcome(service, (self.kwargs | additional_inputs))
        obj = outcome.result
        self.check_object_permissions(self.request, obj)
        return obj