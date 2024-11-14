from django.http import JsonResponse
from django.views import View

from main_app.services.photo.read import ReadPhotosIDWithEntry

class SearchView(View):

    def get(self, request):
        entry = request.GET['search_string']
        photos_list = ReadPhotosIDWithEntry.execute({'entry': entry})
        return JsonResponse({'photos':photos_list})