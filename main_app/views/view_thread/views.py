from django.shortcuts import render
from django.views import View

from main_app.services.comment import ListThread

class ViewThread(View):
    template_name = 'main_app/view_thread.html'

    def get(self, request, *args, **kwargs):
        max_depth = request.GET.get('max_depth', 5)
        thread = ListThread.execute({"root_id": kwargs['id'],"max_depth": max_depth})
        context = {
            "thread": thread,
            "max_depth": max_depth,
        }
        return render(request, self.template_name, context)