from service_objects.views import ServiceView
from ...services import ReadAllPhotos

class IndexView(ServiceView):
    service_class = ReadAllPhotos
    template_name = 'main_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        service_result = self.service_class.execute({})

        context['photos'] = service_result
        
        return context

        