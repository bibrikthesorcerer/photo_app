from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from models_app.models import Photo
from models_app.admin import PhotoForm
from main_app.serializers import PhotoPageSerializer
from main_app.services import (RetrievePhoto, ListPhotos, 
                               RecoverPhotoBeforeDeletion, SchedulePhotoDeletion,
                               ListComments, CreatePhoto, UpdatePhoto,
                               SendCommentWillBeDeletedNotification)


class DeletePhoto(LoginRequiredMixin, View):
    login_url = '/login/github'

    def get(self, request, *args, **kwargs):
        photo_obj = RetrievePhoto.execute({**self.kwargs})
        sched_result = SchedulePhotoDeletion.execute({'photo': photo_obj})
        if sched_result is True:
            messages.success(request, 'Photo scheduled to be deleted successfully')
            SendCommentWillBeDeletedNotification.execute({"photo": photo_obj})
        else:
            messages.warning(request, "Couldn't schedule deletion of photo")
        return redirect('main_app:profile')


class EditPhoto(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/edit_photo.html'

    def _get_editing_photo(self):
        return RetrievePhoto.execute({**self.kwargs})

    def get(self, request, *args, **kwargs):
        photo_obj = self._get_editing_photo()
        form = PhotoForm(instance=photo_obj)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        photo_obj = self._get_editing_photo()
        is_success = UpdatePhoto.execute(
            {**(request.POST.dict() | {"photo": photo_obj})},
            request.FILES
        )
        if is_success:
            messages.success(request, 'Photo uploaded successfully')
            return redirect('main_app:profile')
        
        return self.get(request, *args, **kwargs)


class IndexView(View):
    template_name = 'main_app/index.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            user = None
        
        photos = ListPhotos.execute({
            **(request.GET.dict() 
               | {"user": user, "status": Photo.APPROVED})
        })

        if request.headers.get('X-Requested-With', None):
            data = PhotoPageSerializer(photos).data
            return JsonResponse(data, safe=False)
        
        context = {
            'photos_page': photos,
            'params': self._get_params(request)
        }
        return render(request, self.template_name, context)
    
    def _get_params(self, request):
        per_page = request.GET.get('per_page','')
        order = request.GET.get('order','')
        entry = request.GET.get('entry','')
        return f"per_page={per_page}&order={order}&entry={entry}"
    

class RecoverPhoto(LoginRequiredMixin, View):
    login_url = '/login/github'

    def get(self, request, *args, **kwargs):
        photo_obj = RetrievePhoto.execute({**self.kwargs})
        recover_result = RecoverPhotoBeforeDeletion.execute({'photo': photo_obj})
        if recover_result is True:
            messages.success(request, 'Photo recovered successfully')
        else:
            messages.warning(request, "Couldn't recover photo. Check if photo status is To Be Deleted")
        return redirect('main_app:profile')


class UploadPhoto(LoginRequiredMixin, View):
    login_url='/login/github'
    template_name = 'main_app/upload_photo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': PhotoForm})
    
    def post(self, request, *args, **kwargs):
        is_success = CreatePhoto.execute(
            {**(request.POST.dict() | {"user": request.user})},
            request.FILES
        )
        if is_success:
            messages.success(request, 'Photo uploaded successfully')
            return redirect('main_app:profile')
        
        return self.get(request, *args, **kwargs)
    

class ViewPhoto(View):
    template_name = 'main_app/view_photo.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            user = None
        
        photo_obj = RetrievePhoto.execute({
            **(self.kwargs | {"user": user})
        })
        comments = ListComments.execute({
            **(self.kwargs | {'roots_only': True,}),
        })

        context = {
            "photo": photo_obj,
            "comments": comments,}
        
        return render(request, self.template_name, context)