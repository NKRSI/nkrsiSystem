import requests
from nkrsiSystem import settings
from django.http import JsonResponse

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pypjlink import Projector

#TODO
# from usersystem.models import FAQ, DoorOpenLog, FrontLink
from internalsystem.models import FAQ, DoorOpenLog, FrontLink
# Create your views here.


@login_required
def index(request):
    front_link = FrontLink.objects.order_by('order')
    return render(request, 'main.html', {'links': front_link})


@login_required
def faq(request):
    questions = FAQ.objects.all()
    return render(request, 'faq/faq.html', {'questions': questions})


@login_required
def door(request):

    log = DoorOpenLog()
    log.user = request.user
    try:
        response = requests.get(settings.DOOR_ENDPOINT, timeout=3)
    except requests.exceptions.ConnectionError:
        log.succeeded = False
        log.save()
        return JsonResponse({'ok': False})
    if response.status_code == 200:
        log.succeeded = True
        log.save()
        return JsonResponse({'ok': True})
    else:
        log.succeeded = False
        log.save()
        return JsonResponse({'ok': False})


@login_required
def projector(request):

    try:
        p = Projector.from_address(settings.PROJECTOR_IP)
        p.authenticate()
        if p.get_power() == 'on':
            p.set_power('off')
        elif p.get_power() == 'off':
            p.set_power('on')
        return JsonResponse({'ok': True})
    except (Exception, TimeoutError):
        return JsonResponse({'ok': False})