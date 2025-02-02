from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.model.objects.get(pk=kwargs['id']).user:
            messages.info(request, "Only post's author can edit post.")
            return redirect('main_app:index')
        return super().dispatch(request, *args, **kwargs)