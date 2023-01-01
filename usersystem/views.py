import json

import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordResetConfirmView
from django.shortcuts import render, redirect
from django.contrib import messages

from usersystem.forms import EditProfileForm
from .models import User
from django.utils.translation import ugettext_lazy as _


@login_required
def view_user(request, user_id=None):
    
    if user_id is None:
        return render(request, 'user/profile.html', {'user': request.user})
    else:
        return render(request, 'user/profile.html', {'user': User.objects.get(id=user_id)})


@login_required
def edit_user(request):
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-edit')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, _("Password changed"))
            return redirect('/account/me')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})


@login_required
def all_users(request):
    
    users = User.objects.order_by('id')
    return render(request, 'user/user_list.html', {'users': users})


class MyPasswordResetConfirmView(PasswordResetConfirmView):

    def form_valid(self, form):
        return super().form_valid(form)
