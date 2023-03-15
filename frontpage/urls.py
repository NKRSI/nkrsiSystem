from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='front-index'),
    path('article/<slug:title>', views.article, name='article')
    ]
