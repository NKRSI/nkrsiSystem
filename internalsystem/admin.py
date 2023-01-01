from django.contrib import admin
from internalsystem.models import FrontLink, FAQ, DoorOpenLog

admin.register(FrontLink)(admin.ModelAdmin)
admin.register(FAQ)(admin.ModelAdmin)


@admin.register(DoorOpenLog)
class DoorOpenLogAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False