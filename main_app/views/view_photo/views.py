from django.shortcuts import render
from django.views import View

from main_app.services.comment.list import ListComments
from main_app.services.photo.read import ReadPhotos

class ViewPhoto(View):
    template_name = 'main_app/view_photo.html'

    def _get_service_args(self) -> dict:
        return {"photo": self.kwargs["id"],
                "parent__isnull": True,
            }

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            user = None
        
        photo_obj = ReadPhotos.execute({
            "user": user,
            "pk": self.kwargs["id"],
        })
        service_args = self._get_service_args()
        comments = ListComments().execute({
            **service_args
            # "filter":{
            #     "photo": photo_obj.id,
            #     "parent__isnull": True,
            # }
        })
        context = {
            "photo": photo_obj,
            "comments": comments,
        }
        return render(request, self.template_name, context)