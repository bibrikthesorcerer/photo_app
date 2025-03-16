from django.contrib import admin
from imagekit.admin import AdminThumbnail
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.shortcuts import redirect
from django.utils.html import format_html
from django.contrib import messages

from models_app.models import Photo
from main_app.services import RetrievePhoto, ReadPhotoVersionsByPhotoID
from .flows import PhotoModerationFlow
from notifications.utils import send_message_to_list_of_users


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ["title", "admin_thumbnail", "user", "status", "moderation"]
    search_fields = ["title", "description"]
    admin_thumbnail = AdminThumbnail(image_field="admin_thumbnail")
    readonly_fields = ["status", "pub_date"]
    list_filter = ["status", "user", "pub_date", "updated_at", "created_at"]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("<int:photo_id>/moderate/",
                self.admin_site.admin_view(self.moderating_view),
                name="moderate"),
            path(
                "<int:photo_id>/approve/",
                self.admin_site.admin_view(self.approve_view),
                name="approve",
            ),
            path(
                "<int:photo_id>/deny/",
                self.admin_site.admin_view(self.deny_view),
                name="deny",
            ),]
        return custom_urls + urls
    
    def moderation(self, obj) -> str:
        if obj.status == Photo.ON_MODERATION:
            url = reverse("admin:moderate", args=[obj.id])
            return format_html(f'<a class="button" href="{url}">Moderate</a>')
        else:
            return format_html(f'Already Moderated')

    def moderating_view(self, request, *args, **kwargs):
        photo_obj = RetrievePhoto.execute(kwargs)
        if photo_obj.status != Photo.ON_MODERATION:
            self.message_user(request,
                              f"Photo {photo_obj.id} is not in need of moderation.",
                              level=messages.WARNING)
            return redirect("admin:index")

        photo_versions = ReadPhotoVersionsByPhotoID.execute(kwargs)
        
        context = dict(self.admin_site.each_context(request))
        context.update([("photo", photo_obj),
                        ("versions", photo_versions),
                        ("meta", self.model._meta)])
        return TemplateResponse(request,
                                "admin/models_app/photo/moderate_photo.html",
                                context)

    def approve_view(self, request, *args, **kwargs):        
        photo_obj = RetrievePhoto.execute(kwargs)
        if photo_obj.status != Photo.ON_MODERATION:
            self.message_user(request,
                              f"Photo {photo_obj.id} is not in need of moderation.",
                              level=messages.WARNING)
            return redirect("admin:index")
        
        flow = PhotoModerationFlow(photo_obj)
        flow.approve(moderator=request.user)
        send_message_to_list_of_users(
            [photo_obj.user.id],
            "send_notification",
            f"Your photo titled '{photo_obj.title}' had been approved!"
        )
        self.message_user(request, "Selected photo approved.")
        return redirect("admin:index")

    def deny_view(self, request, *args, **kwargs):
        if request.method != "POST":
            self.message_user(request, "Only POST requests are acceptable.")
            return redirect("admin:index")
        
        photo_obj = RetrievePhoto.execute(kwargs)
        if photo_obj.status != Photo.ON_MODERATION:
            self.message_user(request,
                              f"Photo {photo_obj.id} is not in need of moderation.",
                              level=messages.WARNING)
            return redirect("admin:index")
        
        flow = PhotoModerationFlow(photo_obj)
        flow.deny(**(request.POST.dict() 
                     | {'moderator': request.user}))
        send_message_to_list_of_users(
            [photo_obj.user.id],
            "send_notification",
            f"Your photo titled '{photo_obj.title}' had been denied. Commentary: '{flow.review_ticket.commentary}'"
        )
        self.message_user(request, "Selected photo denied.")
        return redirect("admin:index")