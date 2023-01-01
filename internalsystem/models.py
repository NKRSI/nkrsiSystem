from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from usersystem.models import User
# Create your models here.


class FrontLink(models.Model):
    url = models.CharField(_('url'), max_length=200)
    type = models.IntegerField(_('type'), choices=((1, _('withoutAJAX')), (2, _('localWithAJAX'))),
                               help_text=_('"withoutAJAX" means standard link, "localWithAJAX" means local links '
                                           'accessible using AJAX technology'))
    icon = models.CharField(_('icon-name'), null=True, max_length=30, blank=True,
                            help_text=_('Filename of icon from static/icon dir which will be presented on a card.'))
    bgcolor = ColorField(_('bgcolor'), default='#000000')
    textcolor = ColorField(_('textcolor'), default='#FFFFFF')
    order = models.IntegerField(_('order'), default=0,
                                help_text=_('Order in which links will be presented on home page. '
                                            'The lower number the higher position.'))
    title = models.CharField(_('title'), max_length=30, default=None)
    description = models.CharField(_('description'), max_length=100, null=True, default=None, blank=True)

    class Meta:
        verbose_name = _('front link')
        verbose_name_plural = _('front links')

    def __str__(self):
        return 'Link: ' + self.title


class FAQ(models.Model):
    question = models.CharField(_('question'), max_length=200)
    order = models.IntegerField(_('order'), default=0,
                                help_text=_('Order in which links will be presented on home page.'
                                            ' The lower number the higher position.'))
    answer = models.TextField(_('answer'), max_length=1000)

    class Meta:
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.question


class DoorOpenLog(models.Model):

    date = models.DateTimeField(_('request date'), default=timezone.now, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    succeeded = models.BooleanField(_('succeeded'))

    def __str__(self):
        return _('Door open request') + ': ' + self.user.get_full_name()

    class Meta:
        verbose_name = _('door open request')
        verbose_name_plural = _('door open requests')
