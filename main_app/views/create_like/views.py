from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from main_app.services.like.create import CreateLikeFromUserPhotoID
from main_app.services.like.read import CheckIfLikeSoftDeleted
from main_app.services.like.update import UndoSoftDeletionOfLike
from main_app.services.photo.read import ReadPhotoByID

class CreateLike(LoginRequiredMixin, View):
    login_url='/login/github'

    def post(self, request):
        photo_id = request.POST['photo_id']
        is_softdeleted = CheckIfLikeSoftDeleted.execute({
                'photo_id': photo_id, 
                'user_id': request.user.id
                })
        if is_softdeleted:
            like_obj = UndoSoftDeletionOfLike.execute({
                'photo_id': photo_id, 
                'user_id': request.user.id
                })
            return JsonResponse(model_to_dict(like_obj))
        else:
            try:
                photo_obj = ReadPhotoByID.execute({'photo_id': photo_id})
                like_obj = CreateLikeFromUserPhotoID.execute({
                    'photo': photo_obj, 
                    'user': request.user
                    })
                return JsonResponse(model_to_dict(like_obj))
            except IntegrityError:
                return JsonResponse({'status': 'duplicate'})
            except ObjectDoesNotExist:
                return JsonResponse({'status': 'error', 'error': 'Object does not exist'}, status=400)