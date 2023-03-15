from django.shortcuts import render

from frontpage.models import FrontPage


def index(request):
    args = dict()
    args['pages'] = FrontPage.objects.all()
    return render(request, 'front_page/main.html', args)


def article(request, title):
    args = dict()
    args['pages'] = FrontPage.objects.all()
    args['article'] = FrontPage.objects.get(slug=title)
    return render(request, 'front_page/page.html', args)
