from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('faq', views.faq, name='faq'),
    path('ajax/door', views.door, name='ajax-door'),
    path('ajax/projector', views.projector, name='ajax-projector'),
]
