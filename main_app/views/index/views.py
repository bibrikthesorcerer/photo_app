from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from main_app.services.photo.read import ReadPhotos
from main_app.serializers.photo import PhotoSerializer

class IndexView(View):
    template_name = 'main_app/index.html'

    def serialize(self, objects):
        serialized = PhotoSerializer(objects.object_list, many=True)

        return {
            'photos_page': serialized.data,
            'total_pages': objects.paginator.num_pages,
            'current_page': objects.number,
            'has_next': objects.has_next(),
            'has_previous': objects.has_previous(),
        }

    def get(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            user = None
        order = request.GET.get('order', '')
        entry = request.GET.get('entry', '')
        per_page = request.GET.get('per_page', '')
        photos = ReadPhotos.execute({
            "order": order,
            "entry": entry,
            "per_page": per_page,
            "user": user,
        })
        photos_page = photos.get_page(request.GET.get('page'))

        context = {'params': f"per_page={per_page}&order={order}&entry={entry}"}

        if request.headers.get('X-Requested-With', None):
            context.update(self.serialize(photos_page))
            return JsonResponse(context, safe=False)
        
        context.update({'photos_page': photos_page})
        return render(request, self.template_name, context)