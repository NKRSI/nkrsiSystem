from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class ResourceUsage(models.Model):
    server = models.CharField(_('server'), max_length=200)
    timestamp = models.DateTimeField(_('timestamp'), default=timezone.now, editable=True)
    gpu_data = models.CharField(_('gpu_data'), max_length=512)
    ram_data = models.CharField(_('ram_data'), max_length=512)
    cpu_data = models.CharField(_('cpu_data'), max_length=2048)

    class Meta:
        verbose_name = _('resource_usage')
        verbose_name_plural = _('resource_usages')

    def __str__(self):
        return self.server + " " + str(self.timestamp)
