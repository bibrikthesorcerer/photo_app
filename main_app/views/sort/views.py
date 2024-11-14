from django.http import JsonResponse
from django.views import View

from main_app.services.photo.read import ReadPhotosAndOrder

class SortView(View):

    def get(self, request):
        order = request.GET['order']
        photos_list = ReadPhotosAndOrder.execute({'order': order})
        return JsonResponse({'photos':photos_list})