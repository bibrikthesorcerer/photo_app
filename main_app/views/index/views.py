from django.shortcuts import render
from django.views import View

from main_app.services.photo.read import ReadAllPhotosWithLikesAndComments

class IndexView(View):
    template_name = 'main_app/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 
                      self.template_name, 
                      {'photos': ReadAllPhotosWithLikesAndComments.execute({})})

        