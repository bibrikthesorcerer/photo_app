from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service_objects.errors import ServiceObjectLogicError, InvalidInputsError

from api.authentication import RedisJWTAuth

class BaseView(APIView):
    authentication_classes = [RedisJWTAuth]
    permission_classes = []

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ServiceObjectLogicError as e:
            self.response = Response(
                {'errors': e.errors_dict, 'info': e.additional_info},
                status=e.response_status
            )
        except InvalidInputsError as e:
            self.response = Response(
                # e.errors.as_data() | e.non_field_errors.as_data(), TODO
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            self.response = Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            return self.finalize_response(request, self.response, *args, **kwargs)
