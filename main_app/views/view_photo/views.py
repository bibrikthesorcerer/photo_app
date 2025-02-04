from django.shortcuts import render
from django.views import View
from django.db.models import Count, Q

#from main_app.services.comment.read import ReadComments
from main_app.services.photo.read import ReadPhotos

class ViewPhoto(View):
    template_name = 'main_app/view_photo.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            user = None
        
        photo_obj = ReadPhotos.execute({
            "user": user,
            "pk": kwargs["id"],
        })
        # comments = ReadComments.execute({
        #     "filter":{
        #         "photo": photo_obj.id,
        #         "parent__isnull": True,
        #     }
        # })
        context = {
            "photo": photo_obj,
            #"comments": comments,
        }
        return render(request, self.template_name, context)