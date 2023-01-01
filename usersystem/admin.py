from django.contrib import admin
from django.template.loader import render_to_string
from usersystem.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = (
        'email', ('first_name', 'last_name'), ('is_candidate', 'is_staff', 'is_active', 'is_superuser'), 'function',
        'phone', 'date_joined')

    def save_model(self, request, obj: User, form, change):

        if not change:
            password = User.objects.make_random_password()
            obj.set_password(password)
            html_message = render_to_string("email/register.html",
                                            {"username": obj.get_full_name(), "password": password,
                                             "protocol": request.scheme, "domain": request.get_host})
            obj.email_user("Witamy w NKRSI", None, html_message=html_message)
        else:
            if form.initial['is_candidate'] and not form.cleaned_data['is_candidate']:
                html_message = render_to_string("email/promote.html",
                                                {"username": obj.get_full_name()})
                obj.email_user("Zostajesz członkiem zwyczajnym w NKRSI", None, html_message=html_message)
            if form.initial['is_active'] and not form.cleaned_data['is_active']:
                html_message = render_to_string("email/degredate.html",
                                                {"username": obj.get_full_name()})
                obj.email_user("NKRSI żegna", None, html_message=html_message)
        obj.save()
