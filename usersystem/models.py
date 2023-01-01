import requests
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from phonenumber_field.modelfields import PhoneNumberField
from nkrsiSystem import settings
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff'), default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now, null=True, editable=True)
    is_candidate = models.BooleanField(_('candidate'), default=True)
    phone = PhoneNumberField(_('phone'), blank=True, null=True)
    function = models.CharField(_('function'), default="", blank=True, max_length=30,
                                help_text=_('Position in NKRSI. If blank it will be depended on candidate status.'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def invite_to_slack(self, request=None, password=None):
        result_of_login = requests.post(settings.ROCKET_LOGIN_URL,
                                        {"username": settings.ROCKET_USERNAME, "password": settings.ROCKET_PASSWORD})
        if result_of_login.json()["status"] == "error":
            if request is None:
                raise RuntimeError(_("Failed for inviter to login. Error: ") + result_of_login.json()['message'])
            else:
                messages.error(request,
                               _("Failed for inviter to login. Error: ") + result_of_login.json()['message'])
        else:
            headers = {'X-Auth-Token': result_of_login.json()["data"]["authToken"],
                       'X-User-Id': result_of_login.json()["data"]["userId"]}
            username = f"{self.last_name.lower()}{self.first_name[0].lower()}".encode('ascii', 'ignore').decode('utf-8')
            result_of_add_to_rocket = requests.post(settings.ROCKET_ADD_USER_URL,
                                                    json={"email": self.email,
                                                          "name": self.get_full_name(),
                                                          "password": password,
                                                          "username": username,
                                                          "sendWelcomeEmail": True}, headers=headers)
            if not result_of_add_to_rocket.json()["success"]:
                if request is None:
                    raise RuntimeError(
                        _("Failed to send invitation. Error: ") + result_of_add_to_rocket.json()['error'])
                else:
                    messages.error(request,
                                   _("Failed to send invitation. Error: ") + result_of_add_to_rocket.json()['error'])
            elif request is not None:
                messages.info(request, _("Invitation to RocketChat has been sent"))
