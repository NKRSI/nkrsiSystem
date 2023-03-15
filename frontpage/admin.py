from django.contrib import admin

from frontpage.models import FrontPage, FrontPageImage

admin.register(FrontPage)(admin.ModelAdmin)
admin.register(FrontPageImage)(admin.ModelAdmin)
