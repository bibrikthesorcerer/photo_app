from django.shortcuts import render
from service_objects.views import ServiceView

from main_app.services.photo.read import ReadAllPhotosWithLikes

class IndexView(ServiceView):
    template_name = 'main_app/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 
                      self.template_name, 
                      {'photos': ReadAllPhotosWithLikes.execute({})})

        