from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class DeletedAtFilter(admin.SimpleListFilter):
    title = _('Deleted Status')
    parameter_name = 'deleted_at'

    def lookups(self, request, model_admin):
        return (
            ('deleted', _('Deleted')),
            ('not_deleted', _('Not Deleted')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'deleted':
            return queryset.filter(deleted_at__isnull=False)
        if self.value() == 'not_deleted':
            return queryset.filter(deleted_at__isnull=True)
        return queryset
